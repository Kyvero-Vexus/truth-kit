# Contributing to truth-kit

Thanks for contributing.

`truth-kit` is an attempt to build tools, methods, and workflows that help
people seek truth more rigorously. That means contributions should optimize for
**evidence, provenance, reproducibility, and honest uncertainty** rather than
mere fluency or apparent cleverness.

## Read first

Before contributing, read:

- [README.md](README.md)
- [ROADMAP.md](ROADMAP.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/design-principles.md](docs/design-principles.md)
- [docs/reporting-format.md](docs/reporting-format.md)
- [AGENTS.md](AGENTS.md) if you are contributing through an AI agent or agent-assisted workflow

## What kinds of contributions fit here

We welcome contributions in several categories:

- **methods** — source criticism, provenance reconstruction, research protocols, uncertainty handling
- **tools** — archive recovery, reverse search, provenance analysis, metadata extraction, diffing, forensics
- **workflows/skills** — reusable investigative procedures built on explicit methods and tools
- **benchmarks** — datasets, tasks, scoring, regression suites
- **reports/examples** — worked investigations, failure analyses, comparisons of methods
- **documentation** — architecture, methodology, usage guides, caveats

## Domain-expert contributions (journalism + research methods)

Non-code contributions are first-class here.

If you are a journalist, researcher, professor, fact-checker, or editor, your
methodological input is especially valuable.

High-impact contribution paths:

- **method review** — critique inference rules, evidence thresholds, and failure modes
- **source-criticism guidance** — strengthen provenance and attribution methodology
- **benchmark curation** — propose realistic cases, edge cases, and adversarial scenarios
- **annotation/rubric design** — improve confidence labels and uncertainty language
- **worked case studies** — provide example investigations and postmortems
- **red-team review** — identify where outputs overstate confidence or miss ambiguity

Suggested workflow for domain experts:

1. Open a GitHub issue titled `Method review: <topic>` or `Benchmark proposal: <topic>`.
2. Include concrete examples (links, excerpts, or synthetic mini-cases).
3. State what should change and how to measure improvement.
4. If helpful, submit a docs-only PR (no code required).

You do **not** need to write code to make meaningful contributions.

## Low-friction external contributor path

If you have useful tools, methods, skills, or writeups, you can contribute them
without spending time adapting to full repo structure first.

**Rule:** substance first, structure second.

Maintainers can normalize structure after review. Contributors should focus on
clarity and utility.

### Minimum contribution package (fast path)

Please include only:

1. **What this is** (2-4 sentences)
2. **How to run/use it** (basic invocation)
3. **What it is good for** (and limits)
4. **Dependencies/license notes** (if any)

That is enough for an initial PR.

### Suggested drop zones (not strict)

- tools/scripts: `contrib/tools/<name>/`
- writeups/specs/RFC-like docs: `contrib/writeups/`
- skills/procedures: `contrib/skills/<name>/`

If your files land elsewhere in a clear way, that is also fine.

### Copy/paste PR template (fast path)

```markdown
## What this contributes
<2-4 sentence summary>

## How to use it
- <command or steps>

## Why it helps
- <primary use case>
- <known limits>

## Dependencies / licensing
- <deps>
- <license or source terms>

## Optional follow-up ideas
- <future improvements>
```

## Core standards

### 1. Truth over fluency

A polished output is not enough. Prefer work that makes evidence more visible,
more traceable, and easier to challenge.

### 2. Preserve provenance

If your contribution extracts, transforms, compares, or summarizes information,
it should preserve source lineage whenever practical.

### 3. Keep uncertainty visible

Do not flatten uncertainty into fake confidence. If a method produces only weak
indicators, say so.

### 4. Prefer inspectable components

Whenever possible, core capabilities should exist as reusable tools or
libraries, not only as prompts or opaque agent behaviors.

### 5. Benchmark what matters

If you add a new capability, think about how it could be evaluated. A tool or
workflow that cannot be checked tends to drift into theater.

### 6. Be courteous to shared infrastructure

When building retrieval-heavy tools/workflows, avoid hammering upstream
systems.

Prefer caching, bounded concurrency, backoff, and rate-limit-aware behavior.
If a source appears degraded or asks you to slow down, slow down.

## Architecture expectations

`truth-kit` is intentionally **toolkit-first**.

That means:

- methods should not depend on a specific agent runtime
- tools should ideally be usable directly via CLI, library API, or batch mode
- workflows should document inputs, steps, outputs, and failure modes
- the user-facing agent should be a thin orchestration layer over those lower layers

If you are adding a new feature, please place it at the right architectural
layer.

## Guidelines by contribution type

### Methods

Method documents should explain:

- the problem being addressed
- the evidence model
- the allowed inference steps
- known failure modes
- reporting expectations

### Tools

Tools should ideally provide at least one of:

- a CLI interface
- a library API
- a reproducible notebook or scriptable batch interface

Tools should avoid hiding crucial logic entirely inside prompts.

### Workflows / skills

If you add a workflow or skill, document:

- required inputs
- ordered steps
- branching conditions
- output format
- how evidence is captured
- what uncertainty means in its results

### Benchmarks

Benchmarks are especially valuable here. Good benchmark additions include:

- known-source recovery tasks
- archived-page reconstruction tasks
- derivative-vs-primary reporting tasks
- uncited paraphrase/upstream inference tasks
- media origin tracing tasks

## Special caution areas

### Authorship / "AI detection"

Contributions in this area must be careful.

Do **not** present weak heuristics as decisive proof that text or media is human
or machine-generated. Prefer language like:

- indicators
- anomaly analysis
- stylometric evidence
- calibrated confidence
- unresolved uncertainty

### Provenance inference

Similarity is not provenance. If a tool infers likely upstream relationships,
make sure it distinguishes:

- explicit citation
- strong evidence of copying or paraphrase
- weaker candidate dependence
- speculation

## Pull request guidance

A good pull request should usually include:

- a concise explanation of the problem
- the architectural layer affected
- why this approach was chosen
- relevant caveats or failure modes
- tests, examples, benchmarks, or worked outputs where appropriate

## Commit guidance

Use clear, structured commits. A `type(scope): Subject` style is preferred.
Explain **why** in the body when the reason is not obvious from the diff.

## Licensing

By contributing to this repository, you agree that your contributions are
licensed under the terms of the GNU Affero General Public License, version 3 or
later.

## Practical north star

The best contributions make it easier to answer questions like:

- Where did this claim come from?
- What is primary and what is derivative?
- What changed across versions?
- What evidence actually supports this conclusion?
- What remains uncertain?

If your contribution helps with that, it is probably a good fit.
