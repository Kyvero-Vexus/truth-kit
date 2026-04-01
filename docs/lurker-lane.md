# Lurker lane: live trend monitoring

This document specifies the `truth-kit` live-lurking lane.

Core position: **live lurking should be tooling-first**, with deterministic
pipelines doing ingestion/scoring/filtering and agents/LLMs used mainly for
orchestration, summarization, and escalation.

## Goals

- detect emerging topics and shifts early
- surface high-signal trend alerts with evidence links
- route candidate claims into provenance workflows
- preserve uncertainty and avoid hype
- operate with infrastructure courtesy (cache, backoff, bounded concurrency)

## Non-goals

- replacing provenance workflows with trend chatter
- unbounded scraping of public systems
- high-volume alert spam
- opaque black-box "this trend is real" claims

## Lane architecture (funnel model)

1. **Source adapters**
   - RSS/Atom feeds
   - social/API streams (where permitted)
   - curated news and wire sources
   - forum/blog feeds

2. **Ingest scheduler**
   - source-specific poll intervals
   - ETag/If-Modified-Since support
   - jittered scheduling
   - retry/backoff with host caps

3. **Normalizer**
   - emit canonical `TrendEvent` records
   - map source-specific metadata into shared schema

4. **Dedup + clustering**
   - canonical URL normalization
   - content hash and near-duplicate grouping
   - topic-cluster assignment

5. **Trend scoring**
   - velocity score (change rate)
   - novelty score (distance from recent baseline)
   - corroboration score (cross-source support)
   - confidence score (data quality + source diversity)

6. **Alert gate**
   - thresholding + cooldown windows
   - suppress low-confidence noise
   - emit canonical `TrendAlert` records

7. **Escalation routing**
   - route selected alerts into:
     - claim tracing
     - archive recovery
     - provenance analysis
   - include evidence package and uncertainty notes

## Shared schemas

Machine-readable formats:

- `tools/common/schemas/trend-event.schema.json`
- `tools/common/schemas/trend-alert.schema.json`

These should be treated as canonical for tooling interchange.

## Implemented phase-2 artifacts

- RSS adapter contract:
  - `tools/common/RSS-ADAPTER-CONTRACT.md`
- baseline source profile:
  - `tools/common/sources/lurker-baseline-sources.json`
- scoring defaults:
  - `tools/common/TREND-SCORING.md`
- TrendAlert -> investigation adapter:
  - `tools/common/TRENDALERT-INVESTIGATION-ADAPTER.md`
- seeded trend benchmark fixtures:
  - `benchmarks/datasets/trend-fixture-001-single-source-noise.json`
  - `benchmarks/datasets/trend-fixture-002-multi-source-breakout.json`
  - `benchmarks/datasets/trend-fixture-003-high-impact-manual-review.json`

## Ingestion policy (operational)

Default policy:

- prefer feed/API access over brittle scraping where possible
- cache responses and use conditional requests (`ETag`, `Last-Modified`)
- cap per-host concurrency and request rate
- use exponential-jitter backoff on transient failures
- honor `Retry-After` and explicit provider limits
- track source health and reduce pressure on degraded sources
- optionally support profile-level quiet hours for alert delivery

## Evidence and uncertainty policy

Every trend alert should contain:

- representative source links
- supporting snippets/signals
- confidence label
- explicit uncertainty notes (what is missing/ambiguous)

Confidence levels:

- `high`
- `medium`
- `low`
- `unresolved`

## Escalation rule

A trend alert should be escalated into provenance workflows when at least one is
true:

- confidence is `high`
- confidence is `medium` **and** corroboration score passes threshold
- confidence is `low` but topic is high-impact and requires human review

Escalation payload should include:

- alert id + topic
- triggering evidence
- candidate claim(s)
- suggested workflow (`claim-tracing`, `archive-recovery`, `provenance`)

## Role split: tooling vs agents/LLMs

### Tooling (default)

- ingestion
- normalization
- dedup/clustering
- scoring
- alert generation
- policy enforcement (rate limits, backoff, cache)

### Agents / LLMs (narrow, bounded)

- summarize top alerts
- propose next investigative step
- route to appropriate workflow
- generate human-readable briefings from structured records

Agents should not replace deterministic ingestion/scoring logic.

## Metrics

Track at minimum:

- alert precision proxy (human acceptance/rejection)
- time-to-alert for known events
- false-positive volume
- source diversity in alerts
- escalation success rate (how often escalated alerts produce useful provenance findings)

## Open implementation tasks

- implement executable RSS adapter from contract (with persistent state + conditional requests)
- define persistent storage model for event/cluster history
- tune scoring thresholds against benchmark precision/recall results
- implement executable TrendAlert -> investigation request adapter
- add social/API adapters after RSS baseline is stable
