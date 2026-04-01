# TODO

This file is the working task tracker for `truth-kit`.

How we use it:

- keep tasks small, concrete, and testable
- move items between sections (`Backlog` → `In progress` → `Done`)
- prefer checkboxes over vague notes
- include links to docs/issues/PRs when available

---

## In progress

- [ ] Define the first canonical report template instance in `reports/worked-examples/` using `docs/reporting-format.md`

## Backlog

### Methods

- [ ] Add `methods/provenance/README.md` with evidence model + inference labels
- [ ] Add `methods/source-criticism/README.md` with workflow boundaries and failure modes
- [ ] Add `methods/archive-recovery/README.md` with retrieval and cache policy
- [ ] Add `methods/authorship-forensics/README.md` with strict uncertainty framing
- [ ] Add `methods/uncertainty/README.md` with confidence language conventions

### Tools

- [x] Define interface contract for `tools/archive/` (inputs, outputs, caching behavior, rate-limit behavior)
- [x] Define interface contract for `tools/reverse-search/`
- [ ] Define interface contract for `tools/provenance/`
- [ ] Define interface contract for `tools/forensics/`
- [x] Add shared utility conventions in `tools/common/`

### Benchmarks

- [ ] Create first benchmark task spec in `benchmarks/tasks/`
- [ ] Create first scoring rubric in `benchmarks/scoring/`
- [x] Seed minimal benchmark fixture set in `benchmarks/datasets/`
- [ ] Define first regression run format in `benchmarks/regressions/`

### Workflows / skills

- [ ] Draft `skills/claim-tracing/README.md` for explicit citation-chain tracing
- [ ] Draft `skills/archive-recovery/README.md` for archive-first retrieval
- [ ] Draft `skills/origin-finding/README.md` for quote/image/text origin tasks

### Agents

- [ ] Draft `agents/single-agent/README.md` with orchestration contract
- [ ] Define promotion criteria for when multi-agent is justified (benchmark thresholds)

### Dork integration (phase 2)

- [ ] Define `tools/provenance/CONTRACT.md` from dork source-chain patterns
- [ ] Draft adapter spec for translating `the-dork` outputs into truth-kit shared schema
- [ ] Create benchmark task + scoring docs for the 3 seeded dork fixtures
- [ ] Draft orchestration notes for hybrid mode (delegate discovery, native reporting)

### Lurker integration (phase 1)

- [x] Add `docs/lurker-lane.md` with live-monitoring scope, sources, and alert contract
- [x] Define trend-event schema (topic, confidence, why-it-matters, evidence links, next step)
- [x] Define trend-alert schema for gated escalation output
- [x] Draft ingestion policy for live sources (poll cadence, caching, backoff, quiet hours)
- [x] Define escalation rule from trend alert → provenance investigation workflow

### Lurker integration (phase 2)

- [ ] Add RSS-first source adapter contract and baseline source list
- [ ] Define trend scoring formula + threshold defaults (velocity/novelty/corroboration)
- [ ] Add adapter spec from `TrendAlert` -> retrieval/provenance investigation request
- [ ] Add benchmark fixtures for trend-detection precision/recall evaluation

### Documentation / project ops

- [ ] Add `docs/glossary.md` for key terms (provenance, dependence, lineage, confidence labels)
- [ ] Add first issue batch from this TODO into GitHub Issues

## Done

- [x] Initial repository scaffold and mission docs
- [x] Roadmap and architecture docs
- [x] AGPL license + contributing + agent guidance
- [x] Directory skeleton aligned with architecture
- [x] Dedupe pass to reduce repetitive doctrine
- [x] Infrastructure courtesy/load-discipline guidance
- [x] Added `docs/dork-capability-map.md` (the-dork → truth-kit layer mapping)
- [x] Defined shared retrieval/provenance schema in `tools/common/SCHEMA.md` (+ JSON schemas)
- [x] Drafted `tools/archive/CONTRACT.md` and `tools/reverse-search/CONTRACT.md`
- [x] Added `docs/dork-migration-notes.md` (delegate vs native execution strategy)
- [x] Seeded first 3 dork-derived benchmark fixtures in `benchmarks/datasets/`
- [x] Added `docs/lurker-lane.md` (tooling-first live trend lane design)
- [x] Added `trend-event` + `trend-alert` schemas in `tools/common/schemas/`
