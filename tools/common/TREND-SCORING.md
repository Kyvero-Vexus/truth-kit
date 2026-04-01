# Trend scoring defaults (lurker lane, draft)

This document defines baseline scoring formulas and thresholds for trend
candidate gating.

Status:

- version: `0.1-draft`
- intended output field mapping: `TrendAlert.scores.*`

## Overview

Each cluster/window gets four normalized component scores in `[0, 1]`:

- `velocity`
- `novelty`
- `corroboration`
- `sourceDiversity`

Overall score:

`overall = 0.35*velocity + 0.25*novelty + 0.25*corroboration + 0.15*sourceDiversity`

These weights are defaults, not doctrine. Tune with benchmark feedback.

## Component defaults

### Velocity

Measures how quickly a cluster is growing.

Default approximation:

`velocity = min(1, log1p(eventsInWindow) / log1p(30))`

Window default: 30 minutes.

### Novelty

Measures distance from recent baseline clusters.

Default approximation:

`novelty = 1 - maxSimilarityToRecentBaseline`

Baseline horizon default: trailing 72 hours.

### Corroboration

Measures cross-source confirmation.

Default approximation:

`corroboration = min(1, uniqueSourceCount / 5) * crossSourceAgreement`

Where `crossSourceAgreement` is a `[0,1]` signal from phrase/entity overlap
across distinct sources.

### Source diversity

Measures source spread quality.

Default approximation:

`sourceDiversity = normalizedShannonEntropy(sourceDistribution)`

Entropy normalization should map to `[0,1]`.

## Gating thresholds (defaults)

- `watch` candidate: `overall >= 0.45`
- emit `TrendAlert`: `overall >= 0.62`
- high-priority alert: `overall >= 0.78`

Hard floor rule:

- if `uniqueSourceCount < 2` and `corroboration < 0.25`, do not emit alert
  unless explicitly marked high-impact for manual review.

## Confidence mapping defaults

Confidence label selection:

- `high` when:
  - `overall >= 0.78`
  - `corroboration >= 0.65`
  - `sourceDiversity >= 0.50`
- `medium` when:
  - `overall >= 0.62`
  - `corroboration >= 0.40`
- `low` when:
  - `overall >= 0.45` but medium criteria not met
- `unresolved` when:
  - score computation is incomplete or conflicting inputs dominate

## Cooldown and re-alert defaults

Per dedupe key:

- default cooldown: 30 minutes
- allow bypass when:
  - `overall` rises by `>= 0.15`, or
  - confidence tier increases, or
  - severity increases to `high/critical`

## Escalation defaults

Map alerts to next workflow by score profile:

- high corroboration + medium/high confidence -> `claim-tracing`
- strong historical change signal -> `archive-recovery`
- broad derivative spread -> `provenance-analysis`
- low confidence, high impact -> `manual-review`

## Notes

- These are deliberately conservative defaults to reduce false positives.
- Tune by benchmark precision/recall and human acceptance feedback.
- Keep all formulas transparent and inspectable; avoid opaque black-box scoring.
