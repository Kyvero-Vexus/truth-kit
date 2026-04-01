# truth-kit roadmap

## Thesis

`truth-kit` exists to build methods and tools for **discovery, provenance,
and epistemic discipline**.

The aim is not merely to find information, but to help people:

- recover hard-to-find material
- trace where claims, images, and narratives come from
- detect when information has been copied, mutated, laundered, or decontextualized
- reason under uncertainty without collapsing into either gullibility or cynicism

Large language models can assist with this work, but they are not truth
machines. They are useful only when embedded inside evidence-first,
provenance-first, and reproducible workflows.

## Project shape

Not everything here should be a prompt skill.

`truth-kit` should include a mix of:

- skills
- CLI tools
- reusable libraries
- datasets and benchmark packs
- notebooks and reproducible pipelines
- method documents and research protocols

The standard is practical truth-seeking, not prompt cleverness.

## Core workstreams

### 1. Discovery

Build tools for finding hard-to-find, forgotten, or deliberately obscured
material on the public internet.

Examples:

- dorking and advanced search workflows
- obscure web retrieval
- open-directory discovery
- mirror discovery
- hard-to-find file and page recovery
- fragment-based search from partial clues

### 2. Archives and recovery

Treat archives as a first-class research surface, not an afterthought.

Examples:

- Internet Archive / Wayback Machine discovery workflows
- archive.today and similar snapshot services
- deleted-page recovery
- historical URL reconstruction
- comparison of page revisions across snapshots
- recovery of removed or edited claims from public archives

### 3. Reverse search

Build reverse search workflows for more than just images.

Examples:

- image origin tracing
- reverse quote search
- paragraph and phrase origin search
- code fragment origin tracing
- document fingerprinting and near-duplicate detection
- first-observed and earliest-reachable-source recovery

### 4. Provenance graphs and lineage tracing

This is a central lane of the project.

Build tools that follow both:

- **explicit sources**: citations, links, references, quoted material
- **implicit sources**: likely upstreams that were paraphrased, copied, or silently inherited

Examples:

- claim-to-source mapping
- citation-chain inspection
- derivative-report detection
- web-of-republication tracing
- claim mutation tracking across reposts and summaries
- provenance graph construction and visualization

### 5. Source criticism and textual lineage

Import rigorous methods from scholarship, especially fields that deal with
fragmentary, layered, derivative, or partially lost source traditions.

Relevant methods include:

- source criticism
- textual criticism
- stemmatics
- redaction analysis
- transmission-history reconstruction
- provenance inference from downstream traces

Biblical scholarship is a particularly useful reference class here because it
has developed serious methods for reconstructing dependence, lost intermediates,
and uncredited borrowing. The point is not confessional; it is methodological.

### 6. Media and authorship forensics

Build tools for authenticity analysis without pretending to deliver impossible
certainty.

Examples:

- image metadata extraction and comparison
- repost-chain reconstruction
- edit and recompression clue detection
- stylometric anomaly analysis
- machine-generation indicators
- authorship forensics with explicit uncertainty

**Important constraint:** avoid overclaiming on "AI detection." The goal is not
a bogus oracle that declares text human or machine with false precision. The
goal is evidence, indicators, and calibrated uncertainty.

### 7. Research protocols and epistemic method

Codify explicit methods for disciplined research.

Examples:

- evidence ledgers
- claim tracking templates
- reproducible investigation notebooks
- adversarial verification checklists
- source reliability heuristics with failure modes documented
- workflows for comparing primary, secondary, and derivative material
- protocols for handling conflicting evidence and unresolved uncertainty

### 8. Benchmarks and evaluation

Do not let the project become a bag of untested tricks.

Build benchmark tasks that measure whether tools actually help.

Example evaluation targets:

- recover the earliest reachable source of a claim
- distinguish primary from derivative reporting
- identify when a citation chain launders a single weak origin
- find the likely upstream of an uncited paraphrase
- reconstruct the spread of an image or quote
- preserve uncertainty honestly instead of faking certainty

## Principles

1. **Truth over fluency.** A polished answer is not enough.
2. **Sources over vibes.** Claims should point somewhere.
3. **Lineage matters.** Where information came from is part of what it is.
4. **Uncertainty stays visible.** Confidence is not certainty.
5. **Reproducibility matters.** Others should be able to inspect the path.
6. **Humans remain responsible.** LLMs assist; they do not absolve.
7. **Methods should survive adversarial pressure.** If a method breaks under mild challenge, it is not good enough.

## Early deliverables

### Phase 1 — foundation

- initial archive-search and recovery toolkit
- reverse-search wrappers for images, quotes, and text fragments
- provenance-tracing prototype for explicit citation chains
- benchmark pack for source recovery and derivative-report detection
- research protocol templates for evidence logging and uncertainty tracking

### Phase 2 — lineage analysis

- uncredited-source inference experiments
- provenance graph generation
- claim-mutation comparison tools
- snapshot diffing across archived versions of a page
- early authorship-forensics experiments with calibrated reporting

### Phase 3 — rigorous method packs

- explicit source-criticism workflows
- textual-lineage reconstruction experiments
- public benchmark corpus for provenance and source-dependence tasks
- comparative evaluation of human-only, LLM-assisted, and hybrid workflows

## Non-goals and cautions

- Do not market weak authorship heuristics as decisive AI detectors.
- Do not treat citation presence as proof of truth.
- Do not let LLM fluency replace source access.
- Do not optimize for black-box scores that users cannot inspect.
- Do not hide uncertainty to make outputs feel stronger.

## Working ambition

`truth-kit` should help people reconstruct **information lineage under
uncertainty**.

If it does that well, it will be more than a search repo and more than a
fact-checking repo. It will be infrastructure for disciplined truth-seeking.
