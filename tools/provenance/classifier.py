"""Primary-vs-derivative source chain classifier.

MVP vertical slice for classifying likely primary sources and derivative
relationships from a topic document set.

Python stdlib only.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
import re
from typing import Any, Dict, List, Optional, Tuple

WORD_RE = re.compile(r"[a-z0-9]+")


def _parse_timestamp(raw: Any) -> Optional[datetime]:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _tokenize(text: str) -> List[str]:
    return WORD_RE.findall((text or "").lower())


def _token_overlap_score(a: str, b: str) -> float:
    ta = set(_tokenize(a))
    tb = set(_tokenize(b))
    if not ta or not tb:
        return 0.0
    overlap = len(ta & tb)
    base = max(1, min(len(ta), len(tb)))
    return overlap / base


def _text_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _score_primary_candidate(doc: Dict[str, Any]) -> float:
    score = 0.0
    if doc.get("originalData"):
        score += 2.0
    citations = doc.get("citations") or []
    if not citations:
        score += 0.75
    score += 0.25
    return score


def _url_to_doc(documents: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {d.get("url", ""): d for d in documents}


def classify_topic_documents(topic: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Classify likely primary sources and derivative relationships."""

    doc_meta = {d["docId"]: {"timestamp": _parse_timestamp(d.get("publishedAt"))} for d in documents}

    ordered_docs = sorted(
        documents,
        key=lambda d: (
            doc_meta[d["docId"]]["timestamp"] is None,
            doc_meta[d["docId"]]["timestamp"] or datetime.max.replace(tzinfo=timezone.utc),
        ),
    )
    url_map = _url_to_doc(ordered_docs)

    primary_scores = {d["docId"]: _score_primary_candidate(d) for d in ordered_docs}
    max_score = max(primary_scores.values()) if primary_scores else 0.0
    primary_docs = [doc_id for doc_id, score in primary_scores.items() if score == max_score and score >= 1.5]

    relationships: List[Dict[str, Any]] = []
    provenance_confidences: List[float] = []

    for doc in ordered_docs:
        doc_id = doc["docId"]
        if doc_id in primary_docs:
            relationships.append(
                {
                    "docId": doc_id,
                    "relationship": "primary-source",
                    "confidence": "high",
                    "confidenceScore": 0.95,
                    "rationale": "Earliest/strongest original reporting indicators (originalData and/or low dependence evidence).",
                    "dependsOn": [],
                }
            )
            provenance_confidences.append(0.95)
            continue

        citations = doc.get("citations") or []
        doc_ts = doc_meta[doc_id]["timestamp"]
        explicit_targets = [url_map[u] for u in citations if u in url_map]
        explicit_targets_in_past = []
        for target in explicit_targets:
            target_ts = doc_meta[target["docId"]]["timestamp"]
            if doc_ts is None or target_ts is None:
                continue
            if target_ts <= doc_ts:
                explicit_targets_in_past.append(target)

        if explicit_targets_in_past:
            target = explicit_targets_in_past[0]
            relationships.append(
                {
                    "docId": doc_id,
                    "relationship": "explicit-citation",
                    "confidence": "high",
                    "confidenceScore": 0.98,
                    "rationale": f"Directly cites {target['docId']} ({target['url']}).",
                    "dependsOn": [target["docId"]],
                }
            )
            provenance_confidences.append(0.98)
            continue

        if explicit_targets and not explicit_targets_in_past:
            relationships.append(
                {
                    "docId": doc_id,
                    "relationship": "unresolved",
                    "confidence": "low",
                    "confidenceScore": 0.25,
                    "rationale": "Citation timing cannot be validated (future or malformed publishedAt); cannot assign explicit dependence confidently.",
                    "dependsOn": [],
                }
            )
            provenance_confidences.append(0.25)
            continue

        if doc_ts is None:
            relationships.append(
                {
                    "docId": doc_id,
                    "relationship": "unresolved",
                    "confidence": "low",
                    "confidenceScore": 0.25,
                    "rationale": "Malformed publishedAt timestamp; temporal ordering is uncertain, so dependence inference is unresolved.",
                    "dependsOn": [],
                }
            )
            provenance_confidences.append(0.25)
            continue

        candidates: List[Tuple[float, Dict[str, Any], str]] = []
        for prior in ordered_docs:
            if prior["docId"] == doc_id:
                continue
            prior_ts = doc_meta[prior["docId"]]["timestamp"]
            if prior_ts is None:
                continue
            if prior_ts > doc_ts:
                continue

            doc_text = doc.get("text", "")
            prior_text = prior.get("text", "")
            token_score = _token_overlap_score(doc_text, prior_text)
            seq_score = _text_similarity(doc_text, prior_text)

            doc_tokens = set(_tokenize(doc_text))
            prior_tokens = set(_tokenize(prior_text))
            numeric_overlap = [t for t in (doc_tokens & prior_tokens) if any(ch.isdigit() for ch in t)]
            shared_tokens = doc_tokens & prior_tokens

            anchor_bonus = 0.0
            if numeric_overlap and len(shared_tokens) >= 4:
                anchor_bonus = 0.30

            combined = min(1.0, (0.6 * token_score) + (0.4 * seq_score) + anchor_bonus)

            if combined > 0:
                candidates.append((combined, prior, f"Lexical overlap with {prior['docId']} (token={token_score:.2f}, sequence={seq_score:.2f}, anchor_bonus={anchor_bonus:.2f})."))

        if not candidates:
            relationships.append(
                {
                    "docId": doc_id,
                    "relationship": "unresolved",
                    "confidence": "low",
                    "confidenceScore": 0.25,
                    "rationale": "No citation and no meaningful overlap with prior docs; cannot infer source chain confidently.",
                    "dependsOn": [],
                }
            )
            provenance_confidences.append(0.25)
            continue

        best_score, best_prior, rationale = max(candidates, key=lambda item: item[0])
        if best_score >= 0.62:
            label = "strong-probable-dependence"
            conf_score = min(0.9, 0.58 + best_score / 2)
            conf_text = "high" if conf_score >= 0.8 else "medium"
        elif best_score >= 0.5:
            label = "possible-dependence"
            conf_score = 0.55
            conf_text = "medium"
        else:
            label = "unresolved"
            conf_score = 0.35
            conf_text = "low"

        relationships.append(
            {
                "docId": doc_id,
                "relationship": label,
                "confidence": conf_text,
                "confidenceScore": round(conf_score, 3),
                "rationale": rationale if label != "unresolved" else "Evidence too weak for dependence label despite some overlap.",
                "dependsOn": [best_prior["docId"]] if label != "unresolved" else [],
            }
        )
        provenance_confidences.append(conf_score)

    bucket_counts = Counter(item["confidence"] for item in relationships)
    avg_conf = (sum(provenance_confidences) / len(provenance_confidences)) if provenance_confidences else 0.0
    if avg_conf >= 0.8:
        minimum_confidence = "high"
    elif avg_conf >= 0.5:
        minimum_confidence = "medium"
    else:
        minimum_confidence = "low"

    return {
        "topic": topic,
        "primaryDocIds": primary_docs,
        "derivativeDocIds": [r["docId"] for r in relationships if r["relationship"] not in {"primary-source", "unresolved"}],
        "relationships": relationships,
        "minimumProvenanceConfidence": minimum_confidence,
        "confidenceDistribution": dict(bucket_counts),
    }
