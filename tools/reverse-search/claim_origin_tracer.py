#!/usr/bin/env python3
"""Minimal claim origin tracer for reverse-search MVP #1.

Stdlib-only implementation that consumes a retrieval/provenance-style request and
optional in-memory corpus docs (via input metadata), then emits a
retrieval-provenance response envelope.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

CONFIDENCE_ORDER = {"unresolved": 0, "low": 1, "medium": 2, "high": 3}
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "was",
    "were",
    "is",
    "are",
    "after",
    "as",
    "now",
    "that",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9']+", text.lower()) if t and t not in STOPWORDS]


def _jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    aset = set(a)
    bset = set(b)
    if not aset or not bset:
        return 0.0
    return len(aset & bset) / len(aset | bset)


def _provider_from_url(url: str) -> str:
    host = urlparse(url).netloc or "unknown"
    return host.lower()


def _extract_query_from_inputs(inputs: Sequence[Dict[str, Any]]) -> Tuple[str, str]:
    for item in inputs:
        kind = item.get("kind")
        value = (item.get("value") or "").strip()
        if kind in {"text", "quote", "url"} and value:
            return kind, value
    return "text", ""


def _extract_documents(inputs: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []
    for item in inputs:
        meta = item.get("metadata") or {}
        embedded = meta.get("documents")
        if isinstance(embedded, list):
            for doc in embedded:
                if isinstance(doc, dict) and doc.get("url") and doc.get("text"):
                    docs.append(doc)
    return docs


def _relationship_for_doc(doc: Dict[str, Any], earliest_url: str, overlap: float) -> str:
    citations = set(doc.get("citations") or [])
    if citations or earliest_url in citations:
        return "explicit-citation"

    host = _provider_from_url(doc.get("url", ""))
    if "social." in host or host.startswith("social"):
        return "weak-candidate-dependence"

    if overlap >= 0.66:
        return "direct-reuse"
    if overlap >= 0.45:
        return "strong-probable-dependence"
    if overlap > 0.0:
        return "weak-candidate-dependence"
    return "unresolved"


def _confidence_for_doc(overlap: float, relationship: str, has_citation: bool) -> str:
    if relationship == "explicit-citation":
        return "high" if has_citation else "medium"
    if relationship == "direct-reuse":
        return "high"
    if relationship == "strong-probable-dependence":
        return "medium"
    if relationship == "weak-candidate-dependence":
        return "medium" if overlap >= 0.20 else "low"
    return "unresolved"


def trace_claim_origin(request: Dict[str, Any]) -> Dict[str, Any]:
    request_id = request.get("requestId", "unknown-request")
    query_type = request.get("queryType", "reverse.text")
    inputs = request.get("inputs") or []

    input_kind, query_text = _extract_query_from_inputs(inputs)
    documents = _extract_documents(inputs)

    started_at = _now_iso()
    response: Dict[str, Any] = {
        "schemaVersion": "0.1.0",
        "requestId": request_id,
        "status": "ok",
        "queryType": query_type,
        "summary": {
            "attemptedProviders": 1 if documents else 0,
            "successfulProviders": 1 if documents else 0,
            "cacheHits": 0,
            "networkRequests": 0,
            "durationMs": 0,
        },
        "results": [],
        "evidence": [],
        "uncertainty": [],
    }

    if not query_text:
        response["status"] = "error"
        response["errors"] = [{"code": "missing-query", "message": "No text/quote/url input provided."}]
        return response

    if not documents:
        response["status"] = "partial"
        response["uncertainty"].append(
            {
                "code": "missing-corpus",
                "message": "No candidate document corpus provided in inputs[].metadata.documents.",
            }
        )
        return response

    query_tokens = _tokenize(query_text)
    ranked: List[Tuple[Dict[str, Any], float]] = []
    for doc in documents:
        overlap = _jaccard(query_tokens, _tokenize(doc.get("text", "")))
        ranked.append((doc, overlap))

    ranked.sort(key=lambda x: (_parse_time(x[0].get("publishedAt", "9999-12-31T00:00:00Z")), -x[1]))
    earliest = ranked[0][0]
    earliest_url = earliest["url"]

    for idx, (doc, overlap) in enumerate(ranked, start=1):
        relationship = _relationship_for_doc(doc, earliest_url, overlap)
        has_citation = bool(doc.get("citations")) or earliest_url in set(doc.get("citations") or [])
        confidence = _confidence_for_doc(overlap, relationship, has_citation)

        evidence_id = f"ev-{idx}"
        response["evidence"].append(
            {
                "evidenceId": evidence_id,
                "kind": "text-overlap",
                "description": f"Overlap={overlap:.2f}; inputKind={input_kind}; docId={doc.get('docId', f'doc-{idx}')}",
            }
        )

        response["results"].append(
            {
                "resultId": doc.get("docId", f"doc-{idx}"),
                "kind": "candidate-source",
                "source": {
                    "provider": _provider_from_url(doc["url"]),
                    "url": doc["url"],
                    "retrievedAt": started_at,
                    "accessPath": "cache",
                },
                "content": {
                    "title": doc.get("docId", ""),
                    "snippet": doc.get("text", "")[:220],
                    "mediaType": "text/plain",
                },
                "provenance": {
                    "relationship": relationship,
                    "confidence": confidence,
                    "rationale": [
                        f"Token overlap score: {overlap:.2f}",
                        f"Published at: {doc.get('publishedAt', 'unknown')}",
                    ],
                    "evidenceRefs": [evidence_id],
                },
            }
        )

    if any(item[1] < 0.2 for item in ranked):
        response["uncertainty"].append(
            {
                "code": "low-overlap-candidates",
                "message": "Some downstream candidates have weak lexical overlap; earlier unseen sources remain possible.",
            }
        )

    if response["uncertainty"]:
        response["status"] = "partial"

    return response


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _build_request_from_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    claim = fixture.get("input", {}).get("claim", "")
    docs = fixture.get("input", {}).get("documents", [])
    return {
        "schemaVersion": "0.1.0",
        "requestId": fixture.get("fixtureId", "fixture-request"),
        "queryType": "reverse.text",
        "inputs": [
            {
                "kind": "text",
                "value": claim,
                "metadata": {"documents": docs},
            }
        ],
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run minimal claim origin tracer")
    parser.add_argument("--request", help="Path to request JSON")
    parser.add_argument("--fixture", help="Path to benchmark fixture JSON")
    args = parser.parse_args(argv)

    if bool(args.request) == bool(args.fixture):
        parser.error("Provide exactly one of --request or --fixture")

    if args.request:
        request = _load_json(args.request)
    else:
        request = _build_request_from_fixture(_load_json(args.fixture))

    response = trace_claim_origin(request)
    json.dump(response, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
