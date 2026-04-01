# AGENTS.md

Agent-specific guidance for contributing to `truth-kit`.

This file is intentionally a **delta** from [CONTRIBUTING.md](CONTRIBUTING.md).
If a rule is general (human + agent), prefer CONTRIBUTING as the source of
truth. This file focuses on agent-specific operating discipline.

## Read order for agents

1. [README.md](README.md)
2. [ROADMAP.md](ROADMAP.md)
3. [docs/architecture.md](docs/architecture.md)
4. [docs/design-principles.md](docs/design-principles.md)
5. [docs/reporting-format.md](docs/reporting-format.md)
6. [CONTRIBUTING.md](CONTRIBUTING.md)

## Agent mandate

When implementing work in this repo:

- treat yourself as an orchestrator of explicit methods and tools
- preserve evidence trails and source lineage
- keep uncertainty visible in outputs
- avoid confident prose that outruns evidence
- practice infrastructure courtesy: cache when practical and avoid hammering sources

## Architecture constraints (agent-specific)

Use this stack order unless explicitly justified otherwise:

1. methods
2. tools
3. workflows/skills
4. agent interface
5. multi-agent orchestration (only after benchmark evidence)

### Practical rule

Do not hide core capability inside prompt-only behavior if that capability
should exist as a reusable tool.

Bad:
- provenance logic only exists in an agent prompt

Good:
- provenance logic exists as a tool/library; agent invokes it

## Provenance discipline

When making lineage claims, label evidence strength explicitly:

- explicit citation
- direct reuse
- strong probable dependence
- weaker candidate dependence
- unresolved/insufficient evidence

Similarity by itself is not provenance.

## Authorship / machine-generation caution

Do not produce binary "human vs AI" verdict theater.

Prefer:

- indicators
- anomaly descriptions
- confidence calibration
- failure-mode notes
- unresolved uncertainty where applicable

## Output discipline for agent runs

Agent-produced reports should conform to
[docs/reporting-format.md](docs/reporting-format.md), including:

- question + scope
- method summary
- evidence trail
- findings + counterevidence
- uncertainty + limitations
- next steps

## Repo hygiene for agents

- keep commits coherent and scoped
- update docs when behavior changes
- never commit secrets or private data
- avoid introducing duplicated doctrine when a canonical doc already exists

## Decision heuristic

If multiple implementations are possible, prefer the one that is:

- more inspectable
- easier to reproduce
- easier to benchmark
- less likely to overstate conclusions
- more reusable outside agent runtime
