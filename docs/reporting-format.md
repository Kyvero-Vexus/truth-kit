# truth-kit reporting format (draft)

This document defines the expected structure for investigation reports produced
by tools, workflows, or agents in `truth-kit`.

The goal is consistency, inspectability, and honest uncertainty.

## Minimum report sections

A complete report should include the following sections in order.

## 1. Research question

- What is being investigated?
- What exact claim, artifact, or provenance question is in scope?

## 2. Scope and inputs

- Inputs provided (URLs, quotes, images, documents, claims)
- Scope constraints (time window, language, domains, exclusions)

## 3. Method summary

- Workflow/method used
- Key assumptions
- Major limitations known at start

## 4. Evidence trail

For each key evidence item:

- source URI/location
- acquisition method (direct, archive, mirror, etc.)
- retrieval timestamp
- relevant extracted content or metadata
- provenance confidence level (if inferred)

## 5. Findings

- Primary findings (supported by strongest evidence)
- Secondary findings (useful but weaker)
- Counterevidence or conflicting signals

## 6. Provenance assessment

When applicable, classify relationships clearly:

- explicit citation
- direct quote/reuse
- strong probable dependence
- weak candidate dependence
- unresolved/insufficient evidence

## 7. Uncertainty and limitations

- what remains unknown
- what evidence was missing or inaccessible
- likely failure modes for this result
- confidence calibration per major conclusion

## 8. Next steps

- concrete follow-up actions
- what new evidence would most reduce uncertainty

---

## Optional machine-readable artifacts

Where available, include references to artifacts such as:

- provenance graphs
- source ledgers
- snapshot diffs
- similarity matrices
- extraction logs

## Output style constraints

- distinguish facts from inferences explicitly
- avoid rhetorical certainty unsupported by evidence
- avoid collapsing uncertainty into a single confidence score when nuance is needed
- avoid claims like "definitively AI-generated" unless supported by decisive evidence

## Suggested confidence labels

Use calibrated language for conclusions:

- high confidence
- moderate confidence
- low confidence
- unresolved

Include a one-line reason for each confidence label.

---

This is a draft standard and may evolve alongside benchmark and workflow
development.
