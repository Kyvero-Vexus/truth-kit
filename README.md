# truth-kit

`truth-kit` is a Kyvero Vexus project for building practical infrastructure for
truth-seeking research.

This repo focuses on three things:

- finding and recovering information (including hard-to-find and archived material)
- tracing information lineage (who sourced what from where)
- keeping reasoning disciplined under uncertainty

LLMs are part of the toolkit, not the authority. The project treats model output
as assistive and requires evidence trails, provenance tracking, and reproducible
workflows.

## What this repository builds

`truth-kit` is intentionally a mixed-format toolkit, not just a prompt collection.

Expected components include:

- method docs and research protocols
- CLI tools and reusable libraries
- workflow/skill wrappers over those tools
- benchmark datasets and scoring tasks
- reports and worked investigations
- agent interfaces that orchestrate the above

## Scope map

Current workstreams (summarized):

- discovery and retrieval
- archives and recovery
- reverse search
- provenance graphs and lineage tracing
- source criticism and textual lineage
- media/authorship forensics
- research protocol design
- benchmark and evaluation systems

For detailed scope, priorities, and phases, see [ROADMAP.md](ROADMAP.md).

## Architecture direction

Long-term UX goal: a simple truth-seeking agent (or agent system).

Implementation strategy: build bottom-up and keep the core inspectable.

Layering model:

1. methods
2. tools
3. workflows/skills
4. agent interface
5. multi-agent orchestration only if benchmarks show clear gains

Architecture details are in [docs/architecture.md](docs/architecture.md).

## Design stance

The project prioritizes:

- evidence quality over rhetorical polish
- provenance visibility over black-box conclusions
- calibrated uncertainty over fake certainty
- reproducibility over one-off demos

Canonical principles live in
[docs/design-principles.md](docs/design-principles.md).

Reporting expectations live in
[docs/reporting-format.md](docs/reporting-format.md).

## Current status

The repository is in early design + scaffold mode.

Completed so far:

- scope and roadmap
- architecture document
- contribution guidance (human + agent)
- AGPL licensing
- initial directory skeleton aligned with architecture
- baseline design-principles and reporting-format docs

## Read next

- [ROADMAP.md](ROADMAP.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/design-principles.md](docs/design-principles.md)
- [docs/reporting-format.md](docs/reporting-format.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [AGENTS.md](AGENTS.md)

## License

GNU Affero General Public License, version 3 or later.
See [LICENSE](LICENSE).
