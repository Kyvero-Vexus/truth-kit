# Shared retrieval/provenance schema (v0.1)

This document defines the baseline request/response envelopes used by dork-derived
retrieval tools in `truth-kit`.

Scope:

- `tools/archive/*`
- `tools/reverse-search/*`
- future provenance/forensics retrieval tools

Machine-readable schema files:

- `tools/common/schemas/retrieval-provenance-request.schema.json`
- `tools/common/schemas/retrieval-provenance-response.schema.json`

## Design goals

- one stable envelope across retrieval tools
- explicit provenance + uncertainty fields
- built-in cache and load-discipline controls
- benchmark-friendly, machine-readable outputs

## Request envelope

Minimal required fields:

- `schemaVersion`
- `requestId`
- `queryType`
- `inputs`

Recommended shape:

```json
{
  "schemaVersion": "0.1.0",
  "requestId": "req-123",
  "queryType": "archive.lookup",
  "question": "Find earliest reachable source for this claim.",
  "inputs": [
    {
      "kind": "text",
      "value": "quoted claim text",
      "contentHash": "sha256:..."
    }
  ],
  "constraints": {
    "maxSources": 25,
    "maxDepth": 3,
    "languages": ["en"]
  },
  "retrievalPolicy": {
    "cacheMode": "prefer-cache",
    "cacheTtlSeconds": 86400,
    "maxConcurrentRequests": 4,
    "maxRequestsPerHostPerMinute": 30,
    "retry": {
      "maxAttempts": 3,
      "backoff": "exponential-jitter"
    },
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
    "allowDelegationToDork": true,
    "preferredProviders": ["dorxng", "wayback", "searxng"]
  }
}
```

### `queryType` conventions

Current baseline values:

- `archive.lookup`
- `archive.fetch`
- `archive.diff`
- `reverse.text`
- `reverse.quote`
- `reverse.image`
- `reverse.document`

## Response envelope

Minimal required fields:

- `schemaVersion`
- `requestId`
- `status`
- `queryType`
- `results`

Recommended shape:

```json
{
  "schemaVersion": "0.1.0",
  "requestId": "req-123",
  "status": "partial",
  "queryType": "archive.lookup",
  "summary": {
    "attemptedProviders": 3,
    "successfulProviders": 2,
    "cacheHits": 4,
    "networkRequests": 6,
    "durationMs": 1250
  },
  "results": [
    {
      "resultId": "r1",
      "kind": "candidate-source",
      "source": {
        "provider": "wayback",
        "url": "https://example.org/post",
        "retrievedAt": "2026-04-01T01:00:00Z",
        "accessPath": "cache",
        "httpStatus": 200
      },
      "content": {
        "title": "Example Post",
        "snippet": "...",
        "contentHash": "sha256:..."
      },
      "provenance": {
        "relationship": "strong-probable-dependence",
        "confidence": "medium",
        "rationale": ["Shared unique phrase cluster"],
        "evidenceRefs": ["ev-1"]
      }
    }
  ],
  "evidence": [
    {
      "evidenceId": "ev-1",
      "kind": "text-match",
      "description": "Unique phrase overlap in paragraph 3"
    }
  ],
  "uncertainty": [
    {
      "code": "MISSING_EARLIER_SNAPSHOT",
      "message": "No snapshots found before 2018-03-01"
    }
  ],
  "errors": [],
  "rateLimitObservations": [],
  "cacheWrites": []
}
```

## Canonical provenance labels

`results[].provenance.relationship` must use one of:

- `explicit-citation`
- `direct-reuse`
- `strong-probable-dependence`
- `weak-candidate-dependence`
- `unresolved`

`results[].provenance.confidence` must use one of:

- `high`
- `medium`
- `low`
- `unresolved`

## Load-discipline expectations

All tools implementing this schema should:

- prefer cache when freshness allows
- avoid burst traffic
- respect `Retry-After` and declared rate limits
- cap concurrency and use backoff retries
- annotate whether each retrieval came from cache or network

## Lurker lane schemas (trend monitoring)

For live-trend monitoring and alert routing, use:

- `tools/common/schemas/trend-event.schema.json`
- `tools/common/schemas/trend-alert.schema.json`

Design notes for this lane are in:

- `docs/lurker-lane.md`

Companion specs:

- `tools/common/RSS-ADAPTER-CONTRACT.md`
- `tools/common/TREND-SCORING.md`
- `tools/common/TRENDALERT-INVESTIGATION-ADAPTER.md`
- `tools/common/sources/lurker-baseline-sources.json`
