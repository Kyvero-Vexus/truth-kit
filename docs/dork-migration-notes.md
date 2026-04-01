# Dork migration notes

This document records how `truth-kit` should use `the-dork` during migration
from delegated retrieval toward truth-kit-native tooling.

Related:

- [dork-capability-map.md](dork-capability-map.md)
- [architecture.md](architecture.md)

## Decision matrix: delegate vs native

## Delegate to `the-dork` when

Use delegation for high-variance exploratory retrieval where adaptive search is
more important than deterministic replay.

Typical cases:

- broad discovery with sparse initial clues
- multi-pass dorking over unknown/unstable source surface
- archive hunting where likely sources are unclear
- ad-hoc investigation requiring iterative query mutation

## Prefer truth-kit-native execution when

Use native tools for repeatable, benchmarked, or policy-sensitive tasks.

Typical cases:

- benchmark tasks and regression runs
- reproducible workflows with fixed inputs/outputs
- investigations requiring strict report-shape compliance
- tasks where cache/load policy must be audited centrally

## Hybrid pattern (default transition mode)

Most near-term work should use a hybrid path:

1. delegate discovery sweep to `the-dork`
2. ingest candidate sources into truth-kit tool chain
3. run truth-kit-native provenance labeling + reporting
4. persist benchmark artifacts where applicable

This preserves current retrieval strength while building native capability.

## Integration contract (minimum)

When delegating to `the-dork`, truth-kit should request:

- provider-attempt summary
- ranked candidate sources
- retrieval timestamps
- evidence snippets/notes
- uncertainty notes

Then transform results into the shared retrieval/provenance schema used in
`tools/common/`.

## Promotion criteria (delegate -> native)

A dork-derived capability can move to truth-kit-native default when:

- equivalent benchmark quality is demonstrated on seeded fixtures
- provenance output meets reporting format requirements
- load-discipline behavior is implemented and validated
- failure modes are documented

Until then, delegation remains acceptable.

## Risks to monitor

- prompt-only logic leaks into core retrieval behavior
- divergence between delegated output and truth-kit schema
- silent source-provider failures without explicit error entries
- hidden load spikes from retry loops or unbounded concurrency

## Open follow-ups

- define adapter spec for ingesting `the-dork` outputs into shared schema
- define benchmark thresholds for promotion of each tool family
- decide where hybrid orchestration state is persisted
