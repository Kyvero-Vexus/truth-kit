# RSS adapter contract (lurker lane, draft)

This contract defines a baseline RSS/Atom ingestion adapter for the live trend
lurk pipeline.

Status:

- version: `0.1-draft`
- output schema: `tools/common/schemas/trend-event.schema.json`
- baseline source profile: `tools/common/sources/lurker-baseline-sources.json`

## Purpose

Provide a deterministic, rate-limit-aware ingest layer for feed sources before
higher-cost social/API expansion.

## Input configuration

Adapter expects a source profile with entries including:

- `sourceId`
- `feedUrl`
- `sourceType` (`rss` or `atom`)
- `pollIntervalSeconds`
- `trustTier`
- optional category/region/language tags

Source profile format is JSON in this repo for reproducibility.

## Required adapter behavior

### 1) Conditional fetch

For each feed poll:

- send `If-None-Match` when previous ETag exists
- send `If-Modified-Since` when previous last-modified exists
- treat `304 Not Modified` as success (no new records)

### 2) Load discipline

Must enforce:

- bounded concurrency per host
- host-level request caps per minute
- exponential-jitter backoff on transient errors
- honor `Retry-After` when present
- temporary cool-down for repeatedly failing sources

### 3) Normalization

Each new entry must be emitted as a `TrendEvent` with:

- `source` metadata
- canonical URL if resolvable
- title/text snippet
- `ingest.accessPath` (`cache` or `network`)
- retrieval timestamp and status fields

### 4) Dedup hinting

Adapter should emit deterministic hints for clustering stage:

- canonical URL
- normalized title hash
- content hash (when available)

### 5) Idempotency

Repeated polls must not re-emit unchanged items as new events.

Preferred strategy:

- persistent key on `sourceId + entryId/url + publishedAt`
- content-hash fallback when IDs are missing

## Failure semantics

Feed poll outcome should be classified as:

- `ok`: fetched and parsed successfully (new items optional)
- `partial`: fetched with parse issues or incomplete field extraction
- `error`: cannot fetch or parse feed

Errors should include machine-readable reason codes.

## Caching expectations

- cache raw feed response with timestamp and response headers
- cache parser-normalized entry records for replay/testing
- configurable TTL and cache mode (`prefer-cache`, `refresh-if-stale`, etc.)

## Baseline source list

This repo provides a starter source profile in:

- `tools/common/sources/lurker-baseline-sources.json`

The list is intentionally conservative and should be reviewed before production
use.

## Security and compliance notes

- respect robots/publisher terms where applicable
- avoid bypassing source controls
- do not fetch private/auth-only feeds without explicit authorization
- keep credentials out of repository configs
