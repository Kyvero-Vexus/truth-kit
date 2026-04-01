# MVP test cases

This document defines concrete test cases for MVP issues #1-#5.

Related:
- `docs/mvp-use-cases-and-issue-specs.md`
- Issues: #1, #2, #3, #4, #5

Conventions:
- **P0** = merge-gating tests (must pass)
- **P1** = important robustness tests
- **P2** = stretch/edge behavior tests

---

## MVP #1 — Claim origin tracer

### P0
- **MVP1-TC01 (fixture happy path):** Using `dork-fixture-001-known-source-recovery.json`, returns expected earliest reachable source candidate and required relationship labels.
- **MVP1-TC02 (input kind coverage):** Supports all intended input kinds (`text`, `quote`, `url`) in one suite.
- **MVP1-TC03 (output contract minimum):** Response includes `results[]`, `provenance.relationship`, `provenance.confidence`, and `uncertainty[]` fields.
- **MVP1-TC04 (confidence floor):** Enforces minimum confidence behavior expected by fixture assertions.

### P1
- **MVP1-TC05 (no candidates):** When corpus has no plausible source, returns empty/partial result with explicit uncertainty code.
- **MVP1-TC06 (conflicting candidates):** If two sources have similar evidence strength, output includes unresolved/low-confidence handling.
- **MVP1-TC07 (evidence traceability):** Every non-unresolved claim has rationale + evidence refs.

### P2
- **MVP1-TC08 (determinism):** Same input corpus/request returns stable candidate ordering.
- **MVP1-TC09 (malformed input):** Missing required request fields yields explicit structured error behavior.

---

## MVP #2 — Silent edit detector

### P0
- **MVP2-TC01 (fixture change detection):** Using `dork-fixture-002-archive-reconstruction.json`, detects expected change events.
- **MVP2-TC02 (claim reversal):** Correctly emits `claim-reversal` event for negative->positive or opposite claim transitions.
- **MVP2-TC03 (scope expansion):** Detects additive claim expansion in later snapshot.
- **MVP2-TC04 (coverage uncertainty):** Incomplete snapshot coverage sets uncertainty/coverage flags.

### P1
- **MVP2-TC05 (single snapshot):** One-snapshot input returns unresolved/insufficient-coverage note, not false change events.
- **MVP2-TC06 (out-of-order snapshots):** Snapshot ordering normalized by timestamp before diffing.
- **MVP2-TC07 (no-change case):** Near-identical snapshots produce zero meaningful change events.

### P2
- **MVP2-TC08 (partial corruption):** One corrupted snapshot still yields partial status + usable uncertainty metadata.
- **MVP2-TC09 (network/cache annotation):** Retrieval access path metadata preserved in output.

---

## MVP #3 — TrendAlert -> investigation request bridge

### P0
- **MVP3-TC01 (workflow routing):** `nextStep.workflow` maps to correct `queryType` (`claim-tracing`, `archive-recovery`, `provenance-analysis`, `manual-review`, `none`).
- **MVP3-TC02 (none behavior):** `workflow=none` returns no request (or explicit no-op), not malformed request.
- **MVP3-TC03 (evidence preservation):** Alert evidence URLs/snippets become request `inputs[]`.
- **MVP3-TC04 (policy defaults):** Output request includes load-discipline defaults (cache mode, concurrency cap, retry/backoff, retry-after, robots).
- **MVP3-TC05 (fixture routing):** Trend fixtures 001/002/003 route to expected outcomes.

### P1
- **MVP3-TC06 (confidence-depth policy):** Low-confidence/manual-review produces reduced depth constraints.
- **MVP3-TC07 (provider hints):** Preferred providers adapt by workflow type.
- **MVP3-TC08 (idempotent transform):** Same alert input produces stable deterministic request payload.

### P2
- **MVP3-TC09 (invalid workflow):** Unsupported workflow yields structured error/validation failure.
- **MVP3-TC10 (sparse alert):** Minimal but valid alert still transforms successfully with defaults.

---

## MVP #4 — Primary-vs-derivative classifier

### P0
- **MVP4-TC01 (fixture expected labels):** `dork-fixture-003-derivative-vs-primary.json` returns expected primary and derivative relationships.
- **MVP4-TC02 (confidence + rationale presence):** Every classified relationship includes confidence and rationale text.
- **MVP4-TC03 (unresolved handling):** Weak evidence paths are labeled unresolved, not over-asserted.

### P1
- **MVP4-TC04 (explicit citation preference):** Explicit citations outrank weak lexical similarity.
- **MVP4-TC05 (time-order sanity):** Earliest high-evidence source receives higher primary probability unless contradictory evidence exists.
- **MVP4-TC06 (multi-primary tie):** Tie case returns multiple plausible primaries with reduced confidence.

### P2
- **MVP4-TC07 (citation loop):** Circular citation graph does not crash; outputs unresolved where necessary.
- **MVP4-TC08 (paraphrase-heavy set):** Low lexical overlap but citation support still classifies correctly.

---

## MVP #5 — Influence cluster graphing

### P0
- **MVP5-TC01 (graph artifact emission):** Emits valid node/edge graph artifact with required fields.
- **MVP5-TC02 (repeated path detection):** Detects repeated amplification pathway(s) in fixture data.
- **MVP5-TC03 (metric computation):** Computes pathway frequency, lag, and direct/indirect counts.
- **MVP5-TC04 (seed tagging):** Correctly tags seed-listed state-affiliated sources and influencer nodes.
- **MVP5-TC05 (uncertainty propagation):** Edge/path uncertainty labels are preserved in output.

### P1
- **MVP5-TC06 (rank stability):** Top-N pathway ranking is stable for deterministic fixture input.
- **MVP5-TC07 (disconnected clusters):** Handles multiple disconnected subgraphs without cross-contamination.
- **MVP5-TC08 (sparse graph):** Gracefully handles graphs with too few edges for strong inference.

### P2
- **MVP5-TC09 (cyclic graph):** Cycles do not cause infinite traversal; pathway limits enforced.
- **MVP5-TC10 (conflicting timestamps):** Outlier timestamps reduce confidence / increase uncertainty instead of breaking metrics.

---

## Cross-MVP integration tests

### P0
- **INT-TC01 (trend -> bridge -> origin):** Trend fixture emits alert, adapter produces request, claim origin tracer processes request-compatible inputs.
- **INT-TC02 (trend -> bridge -> archive):** Archive-oriented alert routes to archive lookup request shape correctly.
- **INT-TC03 (report schema compatibility):** Outputs from MVP tools can be assembled into `docs/reporting-format.md` sections without missing required fields.

### P1
- **INT-TC04 (load-discipline invariants):** No integration path strips retrieval policy defaults.
- **INT-TC05 (uncertainty continuity):** Uncertainty tags survive across adapter/tool boundaries.

## Suggested merge gates

Require at least these before marking MVP lanes merge-ready:
- MVP1: TC01-04
- MVP2: TC01-04
- MVP3: TC01-05
- MVP4: TC01-03
- MVP5: TC01-05
- Integration: INT-TC01-03
