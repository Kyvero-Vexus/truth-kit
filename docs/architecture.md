# truth-kit architecture

## Executive summary

The end goal of `truth-kit` is an **easy-to-use truth-seeking agent or agent
system**.

However, the repository should be built **bottom-up as a toolkit first**.
That means the agent is not the foundation; it is the top layer.

This architecture is designed to avoid the common failure mode where an
impressive-seeming agent sits on vague, untestable, non-reusable prompt logic.
Instead, `truth-kit` should grow from:

1. explicit methods,
2. inspectable tools,
3. benchmarked workflows,
4. then user-facing agents.

In short:

- **user-facing form:** truth agent / truth-workbench
- **engineering form:** modular toolkit for discovery, provenance, and epistemic method

## Core architecture principle

The agent should be a **thin orchestration layer** over explicit methods,
inspectable tools, and benchmarked workflows.

The user should be able to ask for an investigation in natural language, but the
system must remain able to show:

- what steps it took,
- what sources it consulted,
- what evidence it found,
- what inference rules it applied,
- what uncertainty remains,
- where the workflow failed or became speculative.

If the system cannot expose those things, it is not yet trustworthy.

## Why toolkit-first

A toolkit-first design has several benefits:

- tools can be tested without the agent
- methods can be critiqued without code changes
- workflows can be benchmarked without chat orchestration
- the same components can be reused from CLI, library, notebook, or agent
- the agent remains replaceable instead of becoming the whole product

This also lets the project produce value before the full agent exists.

## Layered system model

`truth-kit` should be organized into five layers.

### Layer 1: methods

This is the epistemic foundation.

The methods layer defines:

- what kinds of questions the system can answer
- what counts as evidence
- which inference steps are allowed
- how uncertainty should be reported
- what common failure modes to watch for
- how findings should be documented

Examples:

- source-criticism protocols
- provenance reconstruction methods
- archive-recovery procedures
- authorship-forensics guidance and cautions
- evidence-ledger formats
- benchmark task definitions and scoring rules

This layer should be understandable by a researcher even without running code.

### Layer 2: tools

These are concrete programs, libraries, and adapters that perform specific
operations.

Examples:

- archive search and recovery tooling
- reverse image / quote / paragraph search wrappers
- citation extraction utilities
- provenance graph construction
- document similarity and fragment matching
- snapshot diffing
- metadata extraction
- stylometric and anomaly-analysis utilities
- benchmark runners

A key rule: tools should be usable directly, without requiring the agent.

That means every serious tool should ideally support one or more of:

- CLI invocation
- library API
- batch mode for benchmarks

### Layer 3: workflows and skills

This layer packages tools and methods into reusable procedures.

Examples:

- trace the origin of a claim
- recover a deleted or edited page
- locate the earliest reachable source of a quote
- compare primary reporting against derivative reporting
- build a provenance graph from a set of sources
- assess authorship indicators with calibrated uncertainty

A workflow is more than a tool call. It specifies:

- required inputs
- ordered steps
- branching conditions
- validation checks
- evidence capture requirements
- output format

Some workflows may be represented as skills. Others may be implemented as
scripts, notebooks, or reproducible pipelines. They should not all be reduced to
prompt instructions.

### Layer 4: agent

This is the primary user-facing interface.

The agent's job is to:

- understand the user's research question
- choose the appropriate workflow
- gather missing inputs when necessary
- invoke tools in the right order
- maintain an evidence trail
- produce a structured output with uncertainty preserved

The agent should not silently make strong claims unsupported by evidence.

Instead of acting like an oracle, it should act like a disciplined research
operator.

### Layer 5: multi-agent orchestration

This is a later-stage optimization, not the starting point.

A multi-agent system may become useful when the system benefits from genuinely
distinct investigative roles.

Possible specialized roles:

- **Retriever** — discovers sources, mirrors, caches, and archives
- **Archivist** — reconstructs historical states and snapshot deltas
- **Tracer** — follows citations, paraphrases, and provenance webs
- **Forensics** — handles media clues, metadata, and authorship indicators
- **Critic** — challenges weak inferences and searches for counterevidence
- **Synthesizer** — composes the final report without erasing uncertainty

Important rule: do **not** begin with multi-agent architecture unless the
single-agent system proves insufficient. Multi-agent designs often add more
ceremony than capability.

## Development strategy

### Recommendation: single-agent first

The first end-to-end product should be a **single-agent truth-workbench** built
on top of modular tools and workflows.

Reasons:

- simpler to reason about
- easier to benchmark
- fewer moving parts
- easier to expose evidence and failure points
- avoids fake sophistication

The project should only move to multi-agent orchestration when there is evidence
that specialization improves outcomes on benchmarked tasks.

## Repository structure

A recommended layout:

```text
truth-kit/
  README.md
  ROADMAP.md
  docs/
    architecture.md
    design-principles.md
    reporting-format.md
  methods/
    source-criticism/
    provenance/
    archive-recovery/
    authorship-forensics/
    uncertainty/
  tools/
    archive/
    reverse-search/
    provenance/
    forensics/
    benchmarks/
    common/
  skills/
    claim-tracing/
    archive-recovery/
    origin-finding/
    provenance-graphing/
    authorship-forensics/
  agents/
    single-agent/
    multi-agent/
  benchmarks/
    datasets/
    tasks/
    scoring/
    regressions/
  reports/
    worked-examples/
    failure-analyses/
    benchmark-reports/
  examples/
    notebooks/
    sample-investigations/
```

This is a conceptual layout, not a commandment. The key idea is separation of
concerns.

## Package boundary rules

To keep the system sane, each layer needs boundaries.

### Methods must not depend on the agent

Methods are conceptual and procedural. They should be valid regardless of which
runtime, model, or orchestrator is used.

### Tools must not require a chat runtime

A tool should be runnable independently whenever possible.

Bad outcome:
- the only way to use provenance analysis is by prompting an agent

Better outcome:
- provenance analysis exists as a library and/or CLI, and the agent calls it

### Skills and workflows may depend on tools and methods

They are the first layer where orchestration is expected.

### Agents may depend on all lower layers

But they should not become the only entry point to core functionality.

## Investigation object model

The architecture will likely benefit from a common investigation data model.

A future implementation should probably represent an investigation in terms of:

- **question** — what is being investigated
- **inputs** — URLs, quotes, images, claims, corpora, documents
- **artifacts** — snapshots, hashes, extracted metadata, matches, candidate sources
- **claims** — statements under investigation
- **evidence items** — each with provenance and confidence annotations
- **inferences** — explicit reasoning steps derived from evidence
- **uncertainties** — unresolved ambiguity, missing data, weak links
- **report** — human-readable output generated from the above

This matters because the system should accumulate structured research state,
not just conversation text.

## Output model

The agent should prefer structured outputs that can be inspected later.

A good investigation result should include:

- research question
- scope and inputs
- steps performed
- sources checked
- archived copies found
- strongest findings
- strongest counterpoints
- confidence/uncertainty notes
- next recommended steps

Where appropriate, outputs should also include machine-readable artifacts such
as:

- provenance graphs
- source lists
- similarity matrices
- snapshot diffs
- evidence ledgers

## UX philosophy

The user experience should feel simple even if the internals are rigorous.

Desired user-facing modes:

1. **Quick question mode**
   - "Where did this quote likely come from?"
   - "Find the earliest source of this image."

2. **Investigation mode**
   - deeper multi-step workflow
   - evidence capture
   - archived source recovery
   - explicit uncertainty reporting

3. **Workbench mode**
   - user directly invokes tools, workflows, or reports
   - useful for power users and benchmark work

The same system should support all three by exposing the same underlying
components at different levels of abstraction.

## First implementation targets

The architecture suggests a practical build order.

### Phase A: foundations

Build:

- reporting format
- evidence ledger format
- benchmark task skeletons
- a few core method documents

### Phase B: foundational tools

Build a small number of high-leverage tools first:

- archive search/recovery wrapper
- quote/text reverse-search wrapper
- citation extractor
- snapshot differ
- provenance graph prototype

### Phase C: first workflows

Implement a few benchmarkable workflows:

- trace explicit citation chains
- recover archived versions of a page
- locate earliest reachable source of a quote or phrase
- compare primary and derivative reporting

### Phase D: first agent

Create a single-agent interface that can:

- route questions to the right workflow
- ask for missing inputs
- collect artifacts
- output structured reports

### Phase E: specialization only if earned

Introduce multi-agent orchestration only if benchmarks show that specialized
roles improve either:

- retrieval quality
- provenance accuracy
- robustness under adversarial noise
- researcher time saved

## Evaluation and guardrails

This architecture only makes sense if the system is evaluated honestly.

The project should prefer tasks where success can be checked, including:

- known-source recovery tasks
- derivative-report detection tasks
- paraphrase-upstream inference tasks
- archived-page reconstruction tasks
- quote/image origin tasks

Guardrails:

- do not claim certainty where only indicators exist
- do not collapse provenance into mere similarity
- do not present citation count as evidence of truth
- do not obscure missing data in polished summaries
- do not make "AI detection" claims stronger than the evidence supports

## Anti-patterns to avoid

### 1. Agent all the way down

If every capability is hidden behind prompts, the system becomes hard to test,
hard to inspect, and easy to fool.

### 2. Prompt-only methodology

If the core method exists only as a vibe in an LLM prompt, it is not yet a real
method.

### 3. False certainty UX

A clean answer is not the same as a justified answer.

### 4. Tool sprawl without benchmarks

A pile of clever utilities is not a coherent truth-seeking system.

### 5. Multi-agent theater

Do not add many agents just because it looks advanced.

## Long-term vision

The mature form of `truth-kit` should be:

- approachable for ordinary users,
- rigorous enough for serious investigations,
- inspectable enough for skeptical users,
- modular enough for reuse outside the main agent interface.

The ideal end state is a system where the user can ask a natural-language
question, receive a structured and honest investigation report, and inspect the
underlying evidence trail rather than merely trusting the prose.

That is the right kind of agentic system for truth-seeking.
