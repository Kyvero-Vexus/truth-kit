# AGENTS.md

Guidance for AI agents contributing to `truth-kit`.

This repository exists to build **truth-seeking infrastructure**: methods,
tools, workflows, benchmarks, and eventually agentic interfaces for discovery,
provenance tracing, and disciplined research.

If you are an agent working here, read these first:

- [README.md](README.md)
- [ROADMAP.md](ROADMAP.md)
- [docs/architecture.md](docs/architecture.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

## The short version

- Build the **toolkit first**; do not bury core logic inside an agent.
- Prefer **inspectable tools** over prompt-only magic.
- Preserve **evidence trails** and **source lineage**.
- Keep **uncertainty visible**.
- Do not overclaim on authorship or "AI detection."
- Favor **benchmarkable** and **reproducible** contributions.

## Architectural rule

The intended stack is:

1. methods
2. tools
3. workflows / skills
4. agent
5. multi-agent orchestration only if earned

Do not invert this stack.

Bad pattern:
- start with a chatty agent and improvise all capabilities in prompts

Better pattern:
- define the method
- build or expose the tool
- wrap it in a workflow
- let an agent orchestrate it

## What to optimize for

### 1. Truth over fluency

A smooth answer is not enough. Optimize for evidence quality, provenance, and
inspectability.

### 2. Reusability

If you build a serious capability, it should ideally be usable outside the main
agent interface.

Examples:

- CLI tool
- library module
- reproducible notebook
- batch benchmark runner

### 3. Honest uncertainty

If the evidence is weak, say it is weak.

Do not convert tentative signals into confident prose. The system should surface:

- what is known
- what is likely
- what is plausible but weak
- what remains unknown

### 4. Benchmarkability

Whenever possible, new capabilities should be testable on benchmark tasks or at
least demonstrated with worked examples.

## Provenance discipline

When handling claims, quotes, images, or documents, distinguish carefully among:

- explicit citation
- direct quotation
- near-duplicate reproduction
- probable paraphrase or dependence
- weaker resemblance
- unsupported speculation

Similarity alone is not provenance.

## Authorship / AI-detection caution

This repository should not become a factory for bogus certainty.

If you work on authorship or machine-generation analysis:

- present indicators, not oracles
- prefer calibrated language
- document failure modes
- avoid claiming decisive detection without decisive evidence

## Contribution preferences by layer

### Methods

Method docs should define:

- the question type
- evidence model
- inference rules
- reporting format
- failure modes

### Tools

Tools should be explicit about:

- inputs
- outputs
- dependencies
- what is deterministic vs heuristic
- what evidence they emit for later inspection

### Workflows / skills

Workflows should specify:

- required inputs
- ordered steps
- branch points
- validation checks
- evidence capture
- output structure

### Agents

Agents should be thin orchestrators.

They should:

- choose workflows
- gather missing inputs
- execute tools in order
- preserve artifacts
- report uncertainty honestly

They should not hide crucial reasoning or evidence in uninspectable prose.

## Repo hygiene

- Keep documentation aligned with actual behavior.
- If you add a major new capability, update relevant docs.
- Prefer small, coherent commits.
- Do not commit secrets, tokens, or private corpora.
- Treat public examples as truly public.

## Decision heuristic

When unsure between two implementations, prefer the one that is:

- more inspectable
- more reproducible
- easier to benchmark
- less likely to overstate conclusions
- more reusable outside an agent runtime

That is usually the right choice for `truth-kit`.
