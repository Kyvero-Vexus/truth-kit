# Dork capability map

This document maps reusable knowledge from `the-dork` into `truth-kit`'s
architecture.

Goal: preserve what already works, but integrate it in a toolkit-first,
benchmarkable form.

## Why this exists

`the-dork` already demonstrates practical strength in:

- search intelligence and dorking
- archive discovery and retrieval
- persistent multi-pass search
- source fallback strategies
- retrieval rate-limit/courtesy behavior

`truth-kit` should absorb those strengths as explicit methods, tool contracts,
and testable workflows.

## Capability inventory (from the-dork)

### Retrieval and search

- basic search (quick lookup)
- dork search (targeted retrieval via advanced operators)
- open-directory hunting
- archive discovery for historical material

### Search process

- multi-pass persistent search
- search session accumulation across iterations
- query refinement loops

### Source strategy

- prioritized provider chain (primary, local fallback, public fallback)
- graceful degradation when a source is unavailable

### Operational discipline

- rate limiting and source courtesy on public infrastructure
- sanitization/public-safety hygiene

## Mapping to truth-kit layers

## 1) Methods layer

Extract and formalize:

- query decomposition and refinement method
- source selection and fallback policy
- evidence capture and provenance labeling during retrieval
- stopping rules for diminishing returns
- uncertainty notes for missing/unavailable sources

Target files:

- `methods/provenance/README.md`
- `methods/archive-recovery/README.md`
- `methods/uncertainty/README.md`

## 2) Tools layer

Implement reusable contracts (tool-first, not prompt-first):

- `tools/archive/` for archived snapshot retrieval and revision lookup
- `tools/reverse-search/` for origin search wrappers
- `tools/provenance/` for source graph construction support
- `tools/common/` for shared request/response schema and caching helpers

Each tool contract should define:

- input schema
- output schema
- cache behavior
- rate-limit/backoff behavior
- provenance artifact format

## 3) Workflows / skills layer

Port dork-style procedures into explicit workflows:

- claim tracing (source chain first)
- archive recovery (retrieve historical versions)
- origin finding (quote/image/text fragment)

These should call tool interfaces, not bury logic in prompts.

## 4) Agent layer

Agent behavior should orchestrate, not improvise:

- choose workflow based on question type
- maintain evidence trail
- preserve uncertainty
- show source/fallback path used

## 5) Benchmarks layer

Convert real retrieval patterns into benchmark tasks:

- known-source recovery
- earliest-reachable-source retrieval
- derivative-vs-primary source identification
- archive reconstruction tasks

Success criteria should include both correctness and provenance quality.

## Immediate migration plan

### Phase A — Document extraction

- codify dork-derived retrieval methods
- document fallback and cache policy

### Phase B — Interface contracts

- define tool contracts for archive/reverse-search/provenance/common

### Phase C — Workflow ports

- implement first 2–3 workflow wrappers on those contracts

### Phase D — Benchmark seeding

- add initial fixtures/tasks derived from known dork patterns

### Phase E — Agent integration

- wire single-agent orchestration to these workflows
- delay multi-agent complexity unless benchmarks justify it

## Guardrails during migration

- no prompt-only reimplementation of core retrieval logic
- no fake-certainty language for weak provenance inferences
- no aggressive source hammering; honor cache + backoff discipline
- no opaque outputs without inspectable evidence trail

## Open decisions

- when to delegate directly to `the-dork` vs run truth-kit-native tools
- canonical provenance artifact format (JSON schema)
- benchmark threshold required before multi-agent promotion
