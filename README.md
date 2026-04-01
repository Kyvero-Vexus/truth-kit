# truth-kit

**truth-kit** is a Kyvero Vexus project for building tools, methods, and
workflows that help people seek truth more rigorously.

The project is not just about finding information. It is about helping people:

- recover hard-to-find or lost material
- trace where claims, images, quotes, and narratives come from
- detect when information has been copied, mutated, laundered, or decontextualized
- reason under uncertainty without collapsing into either gullibility or cynicism

Large language models can assist with this work, but they are **not** truth
machines. In `truth-kit`, they are useful only when constrained by evidence,
provenance, adversarial checking, and reproducible workflows.

## Thesis

`truth-kit` is for **discovery, provenance, and epistemic discipline**.

The long-term ambition is to help users reconstruct **information lineage under
uncertainty**.

If it succeeds at that, it will be more than a search repo and more than a
fact-checking repo. It will be infrastructure for disciplined truth-seeking.

## Project shape

Not everything here should be a prompt skill.

The repository is intended to include a mix of:

- methods and research protocols
- CLI tools and reusable libraries
- workflows and skills
- datasets and benchmark packs
- notebooks and reproducible pipelines
- reports and worked investigations
- agent interfaces built on top of the above

The standard is practical truth-seeking, not prompt cleverness.

## Core workstreams

### Discovery

Find hard-to-find, obscure, forgotten, or deliberately buried material.

### Archives and recovery

Treat archives as a first-class research surface: Wayback, archive mirrors,
snapshots, deleted-page recovery, and historical comparison.

### Reverse search

Trace origins of images, quotes, phrases, paragraphs, code fragments, and other
reused artifacts.

### Provenance graphs and lineage tracing

Follow both explicit citations and likely implicit upstream sources.

### Source criticism and textual lineage

Adapt rigorous scholarly methods for reconstructing dependence, transmission,
and lost intermediates.

### Media and authorship forensics

Analyze authenticity and authorship indicators without pretending to deliver
impossible certainty.

### Research protocols and epistemic method

Build evidence-ledger, uncertainty-reporting, and adversarial-verification
workflows that keep investigation disciplined.

### Benchmarks and evaluation

Measure whether tools and workflows actually improve truth-seeking rather than
merely sounding impressive.

## Architecture

The end goal is an **easy-to-use truth-seeking agent or agent system**.

But the repository is being built **toolkit-first**.

That means the agent is not the foundation. The intended stack is:

1. methods
2. tools
3. workflows / skills
4. agent
5. multi-agent orchestration only if benchmarks show it is justified

The agent should be a **thin orchestration layer** over explicit methods,
inspectable tools, and benchmarked workflows.

A user-facing system built from this repo should be able to show:

- what it did
- what sources it checked
- what evidence it found
- what inferences it made
- what uncertainty remains
- where it failed or became speculative

## Principles

1. **Truth over fluency.** A polished answer is not enough.
2. **Sources over vibes.** Claims should point somewhere.
3. **Lineage matters.** Where information came from is part of what it is.
4. **Uncertainty stays visible.** Confidence is not certainty.
5. **Reproducibility matters.** Others should be able to inspect the path.
6. **Humans remain responsible.** LLMs assist; they do not absolve.
7. **Methods should survive adversarial pressure.** If a method breaks under mild challenge, it is not good enough.

## Important cautions

- This project is **not** an excuse to market weak heuristics as decisive “AI detection.”
- Citation presence is **not** proof of truth.
- Similarity is **not** the same thing as provenance.
- LLM fluency must **not** replace source access.
- Missing data and weak links should remain visible in outputs.

## Current status

The repository is in its early design and scaffolding phase.

Current work so far:

- thesis and scope definition
- roadmap for major workstreams
- architecture for toolkit-first, agent-second development
- contribution guidance for humans and agents
- AGPL licensing
- repository directory skeleton aligned with the architecture doc

## License

GNU Affero General Public License, version 3 or later.

## Read next

- [ROADMAP.md](ROADMAP.md)
- [docs/architecture.md](docs/architecture.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [AGENTS.md](AGENTS.md)
- [LICENSE](LICENSE)
