#!/usr/bin/env python3
"""TrendAlert -> RetrievalProvenanceRequest adapter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

QUERY_TYPE_BY_WORKFLOW = {
    "claim-tracing": "reverse.text",
    "archive-recovery": "archive.lookup",
    "provenance-analysis": "reverse.document",
    "manual-review": "reverse.text",
}

ARCHIVE_PROVIDERS = ["wayback", "dorxng", "searxng"]
REVERSE_PROVIDERS = ["dorxng", "searxng", "wayback"]


def _compute_constraints(alert: Dict[str, Any], workflow: str) -> Dict[str, int]:
    max_sources = 20
    max_depth = 3
    if alert.get("confidence") == "high":
        max_sources = 35
        max_depth = 4
    if alert.get("confidence") == "low" or workflow == "manual-review":
        max_depth = 2
    return {"maxSources": max_sources, "maxDepth": max_depth}


def _build_inputs(alert: Dict[str, Any]) -> List[Dict[str, str]]:
    inputs: List[Dict[str, str]] = []
    for evidence in alert.get("evidence", []):
        url = evidence.get("url")
        if isinstance(url, str) and url.strip():
            inputs.append({"kind": "url", "value": url})
        snippet = evidence.get("snippet")
        if isinstance(snippet, str) and snippet.strip():
            inputs.append({"kind": "text", "value": snippet})
    topic = alert.get("topic", {})
    topic_label = topic.get("label") if isinstance(topic, dict) else None
    if isinstance(topic_label, str) and topic_label.strip():
        inputs.append({"kind": "text", "value": topic_label})
    return inputs


def adapt_trend_alert(alert: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    workflow = ((alert.get("nextStep") or {}).get("workflow") or "none").strip()
    if workflow == "none":
        return None
    query_type = QUERY_TYPE_BY_WORKFLOW.get(workflow)
    if query_type is None:
        raise ValueError(f"Unsupported nextStep.workflow: {workflow!r}")

    topic_label = ((alert.get("topic") or {}).get("label") or "").strip()
    return {
        "schemaVersion": "0.1.0",
        "requestId": f"trend-alert:{alert.get('alertId', '')}",
        "queryType": query_type,
        "question": f"Assess provenance and earliest reliable sources for trend '{topic_label}'.",
        "inputs": _build_inputs(alert),
        "constraints": _compute_constraints(alert, workflow),
        "retrievalPolicy": {
            "cacheMode": "prefer-cache",
            "cacheTtlSeconds": 21600,
            "maxConcurrentRequests": 4,
            "maxRequestsPerHostPerMinute": 20,
            "retry": {"maxAttempts": 3, "backoff": "exponential-jitter"},
            "respectRetryAfter": True,
            "respectRobotsTxt": True,
        },
        "provenancePolicy": {
            "labelEvidenceStrength": True,
            "captureHashes": True,
            "captureTimestamps": True,
            "captureAccessPath": True,
        },
        "toolHints": {
            "allowDelegationToDork": (
                workflow in {"claim-tracing", "provenance-analysis"}
                and (
                    alert.get("confidence") == "low"
                    or float((alert.get("scores") or {}).get("corroboration") or 0.0) < 0.5
                )
            ),
            "preferredProviders": ARCHIVE_PROVIDERS if workflow == "archive-recovery" else REVERSE_PROVIDERS,
        },
    }


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Path to TrendAlert JSON file")
    parser.add_argument("--output", "-o", help="Output path for request JSON (default: stdout)")
    args = parser.parse_args()

    alert = _load_json(Path(args.input))
    request = adapt_trend_alert(alert)
    if request is None:
        return 0

    encoded = json.dumps(request, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
