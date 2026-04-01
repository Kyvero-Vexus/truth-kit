# Reverse-search tool contract (draft)

This contract defines expected behavior for origin-finding and reverse-search
capabilities in `tools/reverse-search/`.

It captures dork-derived search patterns while enforcing truth-kit requirements
for provenance and uncertainty reporting.

## Contract status

- version: `0.1-draft`
- request schema: `tools/common/schemas/retrieval-provenance-request.schema.json`
- response schema: `tools/common/schemas/retrieval-provenance-response.schema.json`

## Supported operations

### 1) `reverse.text`

Purpose: find likely upstream sources for a paragraph/text fragment.

Input expectations:

- at least one `inputs[]` item with `kind: text`
- optional language/domain constraints

Output expectations:

- ranked candidate sources
- match rationale (phrase overlap, uncommon token alignment, structure)
- provenance relationship labels + confidence

### 2) `reverse.quote`

Purpose: find earliest reachable source(s) of a quote.

Input expectations:

- quote text
- optional attribution hint and time bound

Output expectations:

- candidate timeline of appearances
- earliest reachable candidate(s)
- uncertainty if earlier source cannot be ruled out

### 3) `reverse.image`

Purpose: locate likely origin or early circulation nodes for an image.

Input expectations:

- image URL, hash, or local reference id
- optional perceptual hash/metadata hints

Output expectations:

- candidate occurrences with source metadata
- reuse/edit clues where available
- uncertainty and failure-mode notes

### 4) `reverse.document`

Purpose: identify prior versions, mirrors, or derivative reuse of a document.

Input expectations:

- document URL/hash/fragment

Output expectations:

- candidate upstream and derivative nodes
- artifact-level hashes and retrieval timestamps

## Match scoring and confidence

Reverse-search tools may score similarity internally, but they must not confuse
similarity with provenance.

Required output distinction:

- similarity evidence
- provenance assessment
- uncertainty statement

Confidence labels must use canonical values:

- `high`
- `medium`
- `low`
- `unresolved`

## Provider and fallback behavior

Reverse-search implementations should:

- support a provider chain/fallback strategy
- report attempted vs successful providers
- expose partial results instead of failing hard when possible

## Caching + load discipline

Reverse-search tools must honor shared retrieval policy controls:

- cache preference and TTL
- bounded concurrency
- host-level request caps
- backoff and retry discipline
- respect for `Retry-After`

## Output constraints

Results must include enough detail for auditability:

- source URL/provider
- retrieval timestamp
- access path (`cache`/`network`)
- rationale snippets
- evidence refs

If origin cannot be determined confidently, status should be `partial` with
explicit uncertainty entries.

## Non-goals (for this contract stage)

- decisive authorship classification from weak signals
- single-number certainty claims without rationale
- opaque ranking without evidence metadata
