# truth-kit design principles

This document distills the design constraints that govern `truth-kit`.

It is intentionally brief and should remain stable even as implementations
change.

## 1) Truth over fluency

Polished language is not the goal. Evidence quality, provenance clarity, and
methodological rigor are the goal.

## 2) Provenance is first-class

Where information comes from is part of what it means.

The system should preserve source lineage through retrieval, transformation,
comparison, and reporting.

## 3) Toolkit-first architecture

Build bottom-up:

1. methods
2. tools
3. workflows / skills
4. agent interfaces
5. multi-agent orchestration only when benchmarked value is clear

The agent should orchestrate; it should not be the only place where core
capabilities exist.

## 4) Inspectability over theater

Users should be able to inspect:

- steps performed
- sources checked
- artifacts produced
- inferences made
- unresolved uncertainty

If outputs are not inspectable, trust should remain low.

## 5) Uncertainty stays visible

Do not convert weak evidence into strong prose.

Reports should distinguish clearly between:

- observed facts
- high-confidence inferences
- low-confidence hypotheses
- unresolved unknowns

## 6) Reproducibility as a default

Methods and tooling should support reruns, comparisons, and benchmarkable
outputs wherever practical.

## 7) Similarity is not provenance

Textual or visual similarity alone does not prove dependence.

Provenance claims should be calibrated and explicitly labeled by evidence
strength.

## 8) No fake-certainty AI detection

Authorship/machine-generation analysis is a forensic signal space, not an
oracle.

Use indicator language and confidence calibration. Avoid decisive claims without
decisive evidence.

## 9) Benchmark before complexity

Do not add orchestration complexity (especially multi-agent workflows) without
demonstrated gains on relevant tasks.

## 10) Public-by-default discipline

This is a public repository. Keep outputs safe for publication:

- no secrets
- no private corpora without permission
- no unverifiable claims presented as fact

---

For architecture details, see [architecture.md](architecture.md).
For output expectations, see [reporting-format.md](reporting-format.md).
