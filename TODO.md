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

- [ ] Define interface contract for `tools/archive/` (inputs, outputs, caching behavior, rate-limit behavior)
- [ ] Define interface contract for `tools/reverse-search/`
- [ ] Define interface contract for `tools/provenance/`
- [ ] Define interface contract for `tools/forensics/`
- [ ] Add shared utility conventions in `tools/common/`

### Benchmarks

- [ ] Create first benchmark task spec in `benchmarks/tasks/`
- [ ] Create first scoring rubric in `benchmarks/scoring/`
- [ ] Seed minimal benchmark fixture set in `benchmarks/datasets/`
- [ ] Define first regression run format in `benchmarks/regressions/`

### Workflows / skills

- [ ] Draft `skills/claim-tracing/README.md` for explicit citation-chain tracing
- [ ] Draft `skills/archive-recovery/README.md` for archive-first retrieval
- [ ] Draft `skills/origin-finding/README.md` for quote/image/text origin tasks

### Agents

- [ ] Draft `agents/single-agent/README.md` with orchestration contract
- [ ] Define promotion criteria for when multi-agent is justified (benchmark thresholds)

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
