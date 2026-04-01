# TrendAlert -> investigation adapter spec (draft)

This spec defines how a `TrendAlert` record maps to the shared
retrieval/provenance investigation request envelope.

Schemas involved:

- input: `tools/common/schemas/trend-alert.schema.json`
- output: `tools/common/schemas/retrieval-provenance-request.schema.json`

## Purpose

Convert live trend alerts into deterministic investigation requests that can run
through truth-kit retrieval/provenance workflows.

## Mapping rules

### Envelope

- `request.schemaVersion` = `0.1.0`
- `request.requestId` = `trend-alert:{alertId}`
- `request.question` = composed from topic + summary

Suggested question template:

`Assess provenance and earliest reliable sources for trend '{topic.label}'.`

### Query type routing

Choose `queryType` by `nextStep.workflow`:

- `claim-tracing` -> `reverse.text`
- `archive-recovery` -> `archive.lookup`
- `provenance-analysis` -> `reverse.document`
- `manual-review` -> `reverse.text` (low-depth defaults)
- `none` -> do not create request

### Inputs

Build `request.inputs[]` from alert evidence and topic context:

1. For each `evidence[].url` add:
   - `{ "kind": "url", "value": "..." }`
2. For each non-empty `evidence[].snippet` add:
   - `{ "kind": "text", "value": "..." }`
3. Add topic label as optional text seed:
   - `{ "kind": "text", "value": "{topic.label}" }`

### Constraints defaults

Derived from alert confidence/severity:

- base:
  - `maxSources = 20`
  - `maxDepth = 3`
- if confidence is `high`: `maxSources = 35`, `maxDepth = 4`
- if confidence is `low` or workflow is `manual-review`: `maxDepth = 2`

### Retrieval policy defaults

- `cacheMode = "prefer-cache"`
- `cacheTtlSeconds = 21600`
- `maxConcurrentRequests = 4`
- `maxRequestsPerHostPerMinute = 20`
- `retry.maxAttempts = 3`
- `retry.backoff = "exponential-jitter"`
- `respectRetryAfter = true`
- `respectRobotsTxt = true`

### Provenance policy defaults

- `labelEvidenceStrength = true`
- `captureHashes = true`
- `captureTimestamps = true`
- `captureAccessPath = true`

### Tool hints

- `allowDelegationToDork = true` when:
  - workflow is `claim-tracing` or `provenance-analysis`, and
  - confidence is `low` or corroboration score is weak
- otherwise prefer `truth-kit-native`

Include `preferredProviders` heuristics:

- archive workflow: `["wayback", "dorxng", "searxng"]`
- reverse/provenance workflow: `["dorxng", "searxng", "wayback"]`

## Reference transformation example

Input (simplified):

```json
{
  "schemaVersion": "0.1.0",
  "alertId": "alert-42",
  "topic": { "label": "Port inspection delays" },
  "confidence": "medium",
  "summary": "Mentions of delays are rising across multiple sources.",
  "scores": { "corroboration": 0.61 },
  "evidence": [
    {
      "eventId": "ev-1",
      "sourceId": "bbc-world",
      "url": "https://example.org/a",
      "snippet": "Inspections exceeded legal limits in Q2"
    }
  ],
  "nextStep": {
    "workflow": "claim-tracing",
    "priority": "p1",
    "delegateTo": "truth-kit-native"
  }
}
```

Output (simplified):

```json
{
  "schemaVersion": "0.1.0",
  "requestId": "trend-alert:alert-42",
  "queryType": "reverse.text",
  "question": "Assess provenance and earliest reliable sources for trend 'Port inspection delays'.",
  "inputs": [
    { "kind": "url", "value": "https://example.org/a" },
    { "kind": "text", "value": "Inspections exceeded legal limits in Q2" },
    { "kind": "text", "value": "Port inspection delays" }
  ],
  "constraints": {
    "maxSources": 20,
    "maxDepth": 3
  },
  "retrievalPolicy": {
    "cacheMode": "prefer-cache",
    "cacheTtlSeconds": 21600,
    "maxConcurrentRequests": 4,
    "maxRequestsPerHostPerMinute": 20,
    "retry": { "maxAttempts": 3, "backoff": "exponential-jitter" },
    "respectRetryAfter": true,
    "respectRobotsTxt": true
  },
  "provenancePolicy": {
    "labelEvidenceStrength": true,
    "captureHashes": true,
    "captureTimestamps": true,
    "captureAccessPath": true
  },
  "toolHints": {
    "allowDelegationToDork": false,
    "preferredProviders": ["dorxng", "searxng", "wayback"]
  }
}
```
