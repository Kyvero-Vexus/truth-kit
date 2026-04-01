# Archive tool contract (draft)

This contract defines the expected behavior for archive-oriented retrieval tools
in `tools/archive/`.

It is derived from proven patterns in `the-dork`:

- archive discovery
- multi-pass retrieval
- provider fallback
- rate-limit-aware behavior

## Contract status

- version: `0.1-draft`
- request schema: `tools/common/schemas/retrieval-provenance-request.schema.json`
- response schema: `tools/common/schemas/retrieval-provenance-response.schema.json`

## Supported operations

### 1) `archive.lookup`

Purpose: find available historical snapshots/copies for a target URL or claim.

Expected inputs:

- at least one `inputs[]` item of kind `url` or `text`
- optional time constraints (`constraints.timeRange`)

Expected outputs:

- ordered candidate snapshots/sources in `results[]`
- provider/source metadata in `source`
- provenance relation labels where inferable

### 2) `archive.fetch`

Purpose: retrieve one specific snapshot copy.

Expected inputs:

- snapshot locator (archive URL, provider id + timestamp, or equivalent)

Expected outputs:

- retrieved content metadata (hash, title/snippet when available)
- access path (`cache` or `network`)
- uncertainty notes if content is partial/corrupt

### 3) `archive.diff`

Purpose: compare two archived versions and summarize meaningful deltas.

Expected inputs:

- two snapshot locators
- optional comparison mode (`text`, `dom`, `metadata`)

Expected outputs:

- structured delta artifact in `results[]` + `evidence[]`
- clear notes for unavailable sections

## Provider strategy

Default provider order should be configurable but generally follow:

1. local/fast archive index (if available)
2. Internet Archive / Wayback
3. other archive mirrors or snapshot services
4. fallback search discovery pass

Rules:

- annotate provider attempts in summary/errors
- degrade gracefully when providers fail
- never silently drop failed providers

## Caching and load discipline

Archive tools must support:

- `cacheMode` and `cacheTtlSeconds`
- bounded concurrency (`maxConcurrentRequests`)
- host-level request cap (`maxRequestsPerHostPerMinute`)
- backoff retry policy
- `Retry-After` compliance

Every result should indicate `source.accessPath` (`cache` or `network`).

## Provenance labeling

When archive results are used for lineage claims, label relation strength using
canonical values:

- `explicit-citation`
- `direct-reuse`
- `strong-probable-dependence`
- `weak-candidate-dependence`
- `unresolved`

Do not infer stronger relations than evidence supports.

## Error handling

Use structured `errors[]` entries with:

- machine code
- human message
- provider (when relevant)
- retryability

Status semantics:

- `ok`: operation completed with expected result coverage
- `partial`: operation completed with gaps/failures
- `error`: operation failed to produce usable result

## Non-goals (for this contract stage)

- guaranteeing permanence of external archive providers
- proving historical authenticity beyond available evidence
- claim-verification logic beyond retrieval/provenance support
