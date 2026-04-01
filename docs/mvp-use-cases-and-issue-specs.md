# MVP use cases and issue-ready specs

This document turns the current `truth-kit` vision into concrete MVP targets
focused on countering real misinformation pipelines.

Design constraints:

- tooling-first (deterministic pipeline before LLM narration)
- evidence/provenance first
- uncertainty visible by default
- non-commercial dependency policy for core lane

## MVP north star (v0.1)

In one command-flow, we should be able to:

1. take a claim or URL,
2. trace likely origin and propagation,
3. detect meaningful revisions over time,
4. produce an evidence-backed report with uncertainty labels.

## Low-hanging use cases (prioritized)

1. Claim origin tracer (text + URL)
2. Silent edit detector (archive diffs)
3. Derivative/laundered reporting detector
4. Trend alert -> provenance escalation
5. Influence cluster graphing (including state-affiliated -> influencer pathways)

---

## Issue-ready spec 1: Claim origin tracer (MVP core)

**Title:** MVP: Claim origin tracer for text/URL inputs

**Problem:** Claims often circulate detached from primary sources.

**Goal:** Given a claim/quote/headline/URL, return earliest reachable source
candidates and a provenance-labeled chain.

**Scope:**
- inputs: free text quote, headline, URL
- operations: reverse lookup + source ranking + evidence packaging
- outputs: structured report + machine-readable provenance entries

**Out of scope (v0.1):**
- multimedia forensics beyond basic URL/image reference support
- definitive authorship attribution

**Acceptance criteria:**
- accepts all three input types (text, quote, URL)
- returns at least 1 candidate source with provenance label
- outputs confidence + uncertainty notes (`high|medium|low|unresolved`)
- writes result in `docs/reporting-format.md` compatible structure

**Dependencies:**
- `tools/reverse-search/CONTRACT.md`
- `tools/common/SCHEMA.md`
- dork fixtures in `benchmarks/datasets/`

**Benchmark target:**
- pass `dork-fixture-001-known-source-recovery.json` with minimum medium confidence on expected chain.

---

## Issue-ready spec 2: Silent edit detector

**Title:** MVP: Archived revision diff and claim-change detector

**Problem:** Narrative edits happen silently after publication.

**Goal:** Given a URL, detect and summarize meaningful claim-level changes across
archived snapshots.

**Scope:**
- archive lookup and fetch
- snapshot selection (at least 2)
- structured diff output with change types

**Out of scope (v0.1):**
- full semantic truth judgment of changed statements
- OCR-heavy screenshot-only page diffing

**Acceptance criteria:**
- finds >=2 snapshots when available
- emits machine-readable change events (claim reversal/scope expansion/etc.)
- includes uncertainty when snapshot coverage is incomplete
- identifies access path (`cache` vs `network`) for retrievals

**Dependencies:**
- `tools/archive/CONTRACT.md`
- retrieval/provenance schemas

**Benchmark target:**
- pass `dork-fixture-002-archive-reconstruction.json` change-event expectations.

---

## Issue-ready spec 3: Derivative/laundered reporting detector

**Title:** MVP: Primary-vs-derivative source chain classifier

**Problem:** Weak origins get laundered through many derivative publications.

**Goal:** Distinguish likely primary source(s) from derivatives and label
relationship strength.

**Scope:**
- ingest source set around one topic
- classify candidate primary docs
- label dependence (`explicit-citation`, `direct-reuse`, `strong-probable-dependence`, etc.)

**Out of scope (v0.1):**
- legal/plagiarism adjudication
- cross-lingual deep translation inference

**Acceptance criteria:**
- outputs at least one primary candidate when evidence supports it
- labels derivative relationships with confidence and rationale
- flags unresolved links instead of forcing certainty

**Dependencies:**
- `tools/provenance/` contract (to be added)
- reverse + archive tool outputs

**Benchmark target:**
- pass `dork-fixture-003-derivative-vs-primary.json` expectations.

---

## Issue-ready spec 4: Trend alert escalation adapter

**Title:** MVP: TrendAlert -> provenance investigation request bridge

**Problem:** Live trend detection produces signals, but not actionable
investigations.

**Goal:** Convert trend alerts into deterministic investigation requests for
claim tracing/archive/provenance workflows.

**Scope:**
- consume `trend-alert.schema.json`
- map to `retrieval-provenance-request.schema.json`
- choose workflow by alert profile and next-step policy

**Out of scope (v0.1):**
- autonomous multi-step investigation execution loop
- social source expansion beyond configured adapters

**Acceptance criteria:**
- valid transform for all supported `nextStep.workflow` values
- preserves evidence URLs/snippets in request inputs
- enforces load-discipline defaults in retrieval policy
- deterministic mapping documented and testable

**Dependencies:**
- `tools/common/TRENDALERT-INVESTIGATION-ADAPTER.md`
- trend schemas + retrieval/provenance schemas

**Benchmark target:**
- evaluate against 3 trend fixtures with expected workflow routing behavior.

---

## Issue-ready spec 5: Influence cluster graphing (state-affiliated -> influencer)

**Title:** MVP: Influence cluster graph and repeated amplification path detection

**Problem:** Coordinated narratives often move through repeatable source
pathways (including state-affiliated media to influencer ecosystems).

**Goal:** Build a graph of source/account clusters and detect frequent
amplification pathways with uncertainty labels.

**Scope:**
- nodes: sources/accounts/domains
- edges: citation, repost, linkage, temporal dependence hints
- metrics: frequency, lag, citation depth, direct vs indirect dependence
- output: cluster graph + top repeated pathways report

**Out of scope (v0.1):**
- definitive motive/intent attribution
- hidden/private-channel inference

**Acceptance criteria:**
- emits graph artifact (JSON edge list at minimum)
- computes pathway ranking by repeat frequency + lag
- marks low-confidence inferences explicitly
- supports seed lists (state-affiliated domains, influencer accounts)

**Dependencies:**
- provenance extraction outputs
- trend alerts for candidate topic windows
- benchmark fixture for propagation chain (to be added)

**Benchmark target:**
- pass first propagation fixture with expected path ranking in top-N.

---

## Suggested MVP execution order

1. Spec 1 (Claim origin tracer)
2. Spec 2 (Silent edit detector)
3. Spec 4 (Trend escalation bridge)
4. Spec 3 (Derivative/laundering detector)
5. Spec 5 (Influence graphing)

This sequence maximizes early utility while reusing already-landed contracts and
fixtures.

## Definition of MVP done (v0.1)

MVP is considered done when:

- specs 1, 2, and 4 are implemented and benchmarked,
- at least one end-to-end report is produced from live trend -> escalation -> provenance output,
- uncertainty and provenance labels are present in all outputs,
- load-discipline controls are active in retrieval components.
