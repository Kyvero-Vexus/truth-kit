"""Archived revision diff and claim-change detector.

Minimal vertical slice for MVP #2:
- consume archived snapshots for a URL/topic
- produce structured change events
- report uncertainty when snapshot coverage is incomplete

Python stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
import json
import re
from typing import Any, Dict, List, Optional


@dataclass
class ChangeEvent:
    fromSnapshotId: str
    toSnapshotId: str
    changeType: str
    summary: str
    fromAccessPath: Optional[str] = None
    toAccessPath: Optional[str] = None


@dataclass
class SnapshotProvenance:
    snapshotId: str
    archiveProvider: Optional[str]
    accessPath: Optional[str]


def _parse_ts(value: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def _clean(text: str) -> str:
    return " ".join(text.lower().split())


def _extract_no_claim_subject(text: str) -> Optional[str]:
    # Example: "no contamination detected"
    m = re.search(r"\bno\s+([a-z][a-z\-\s]{1,60}?)\s+detected\b", text)
    return m.group(1).strip() if m else None


def _extract_positive_claim(text: str, subject: str) -> Optional[str]:
    # Matches phrases such as "low-level contamination detected" or
    # "contamination detected" for a given subject.
    pattern = rf"\b((?:[a-z\-]+\s+){{0,3}}{re.escape(subject)}\s+detected)\b"
    m = re.search(pattern, text)
    if not m:
        return None
    phrase = m.group(1).strip()
    if phrase.startswith("no "):
        return None
    return phrase


def _split_clauses(text: str) -> List[str]:
    parts = re.split(r"[;\.]", text)
    return [p.strip() for p in parts if p.strip()]


def _detect_change_event(a: Dict[str, Any], b: Dict[str, Any]) -> Optional[ChangeEvent]:
    a_text = _clean(a.get("text", ""))
    b_text = _clean(b.get("text", ""))

    no_subject = _extract_no_claim_subject(a_text)
    if no_subject:
        positive = _extract_positive_claim(b_text, no_subject)
        if positive:
            return ChangeEvent(
                fromSnapshotId=a.get("snapshotId", "unknown"),
                toSnapshotId=b.get("snapshotId", "unknown"),
                changeType="claim-reversal",
                summary=f"no {no_subject} -> {positive}",
            )

    a_clauses = set(_split_clauses(a_text))
    b_clauses = _split_clauses(b_text)
    added = [cl for cl in b_clauses if cl not in a_clauses]
    if added:
        return ChangeEvent(
            fromSnapshotId=a.get("snapshotId", "unknown"),
            toSnapshotId=b.get("snapshotId", "unknown"),
            changeType="scope-expansion",
            summary=f"added clause: {added[0]}",
        )

    return None


def _extract_access_path(snapshot: Dict[str, Any]) -> Optional[str]:
    nested = [
        snapshot.get("retrieval"),
        snapshot.get("provenance"),
        snapshot.get("meta"),
    ]
    for obj in nested:
        if isinstance(obj, dict):
            for k in ("accessPath", "retrievalPath", "retrievedVia"):
                value = obj.get(k)
                if value:
                    return str(value)

    for k in ("accessPath", "retrievalPath", "retrievedVia"):
        value = snapshot.get(k)
        if value:
            return str(value)
    return None


def _coverage_uncertainty(snapshots: List[Dict[str, Any]], has_invalid_timestamps: bool) -> Dict[str, Any]:
    notes: List[str] = []

    if len(snapshots) < 3:
        notes.append("Low snapshot count (<3) limits temporal coverage.")

    missing_text = [s.get("snapshotId", "unknown") for s in snapshots if not s.get("text")]
    if missing_text:
        notes.append(f"Missing snapshot text for: {', '.join(missing_text)}.")

    if has_invalid_timestamps:
        notes.append(
            "One or more snapshot timestamps are invalid; temporal direction claims are downgraded."
        )

    providers = {s.get("archiveProvider") for s in snapshots if s.get("archiveProvider")}
    if len(providers) <= 1:
        notes.append("Single-provider archive coverage may be incomplete.")

    coverage_complete = len(notes) == 0
    confidence = "high" if coverage_complete else ("low" if len(snapshots) < 3 else "medium")

    return {
        "coverageComplete": coverage_complete,
        "overallProvenanceConfidence": confidence,
        "temporalOrderingUncertain": has_invalid_timestamps,
        "notes": notes,
    }


def analyze_archive_input(payload: Dict[str, Any]) -> Dict[str, Any]:
    target = payload.get("targetUrl") or payload.get("topic") or "unknown-target"
    snapshots = list(payload.get("snapshots", []))

    enriched: List[Dict[str, Any]] = []
    for idx, snapshot in enumerate(snapshots):
        parsed = _parse_ts(snapshot.get("capturedAt", ""))
        enriched.append({
            **snapshot,
            "_parsedCapturedAt": parsed,
            "_inputOrder": idx,
        })

    enriched.sort(
        key=lambda s: (
            s.get("_parsedCapturedAt") is None,
            s.get("_parsedCapturedAt") or datetime.max,
            s.get("_inputOrder", 0),
        )
    )

    has_invalid_timestamps = any(s.get("_parsedCapturedAt") is None for s in enriched)

    events: List[ChangeEvent] = []
    for i in range(len(enriched) - 1):
        a, b = enriched[i], enriched[i + 1]
        event = _detect_change_event(a, b)
        if event:
            if has_invalid_timestamps and event.changeType == "claim-reversal":
                continue
            event.fromAccessPath = _extract_access_path(a)
            event.toAccessPath = _extract_access_path(b)
            events.append(event)

    uncertainty = _coverage_uncertainty(enriched, has_invalid_timestamps)
    snapshot_provenance = [
        asdict(
            SnapshotProvenance(
                snapshotId=s.get("snapshotId", "unknown"),
                archiveProvider=s.get("archiveProvider"),
                accessPath=_extract_access_path(s),
            )
        )
        for s in enriched
    ]

    return {
        "target": target,
        "snapshotCount": len(enriched),
        "changeEvents": [asdict(e) for e in events],
        "snapshotProvenance": snapshot_provenance,
        "uncertainty": uncertainty,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Archived claim-change detector")
    parser.add_argument("--input", required=True, help="Path to JSON input payload")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Allow fixture shape ({input: {...}}) and raw payload shape.
    payload = data.get("input", data)
    result = analyze_archive_input(payload)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
