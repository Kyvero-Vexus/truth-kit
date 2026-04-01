"""Influence cluster graph + repeated amplification path detection.

Stdlib-only implementation for MVP #5.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


def _parse_ts(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _safe_parse_ts(value: str) -> Optional[datetime]:
    try:
        return _parse_ts(value)
    except (TypeError, ValueError):
        return None


def _duplicate_event_ids(events: Sequence[Dict[str, Any]]) -> List[str]:
    counts = Counter(event.get("id") for event in events if event.get("id"))
    return sorted(event_id for event_id, count in counts.items() if count > 1)


def build_influence_graph(
    events: Iterable[Dict[str, Any]],
    state_seed_accounts: Optional[Sequence[str]] = None,
    influencer_seed_accounts: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """Build node/edge artifacts and repeated amplification pathway metrics."""

    events_list = list(events)
    duplicate_ids = _duplicate_event_ids(events_list)
    if duplicate_ids:
        return {
            "graph": {"nodes": [], "edges": []},
            "pathways": {"repeated_pathways": []},
            "uncertainty": {
                "status": "error",
                "code": "duplicate_event_ids",
                "message": "Duplicate event IDs detected; influence graph not constructed.",
                "duplicate_event_ids": duplicate_ids,
            },
        }

    events_by_id: Dict[str, Dict[str, Any]] = {}
    ordered_events: List[Dict[str, Any]] = []

    for event in events_list:
        event_copy = dict(event)
        event_copy.setdefault("uncertainty", "unknown")
        ordered_events.append(event_copy)
        events_by_id[event_copy["id"]] = event_copy

    state_seeds = set(state_seed_accounts or [])
    influencer_seeds = set(influencer_seed_accounts or [])

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, Any]] = []
    invalid_timestamp_event_ids: set[str] = set()

    def ensure_node(account: str) -> Dict[str, Any]:
        if account not in nodes:
            tags = []
            if account in state_seeds:
                tags.append("state_affiliated_seed")
            if account in influencer_seeds:
                tags.append("influencer_seed")
            nodes[account] = {
                "id": account,
                "account": account,
                "seed_tags": tags,
                "event_count": 0,
            }
        return nodes[account]

    for event in ordered_events:
        account = event["account"]
        ensure_node(account)["event_count"] += 1

    for event in ordered_events:
        parent_id = event.get("amplified_from_event_id")
        if not parent_id:
            continue
        parent = events_by_id.get(parent_id)
        if not parent:
            continue

        child_ts = _safe_parse_ts(event["timestamp"])
        parent_ts = _safe_parse_ts(parent["timestamp"])
        if child_ts is None:
            invalid_timestamp_event_ids.add(event["id"])
            event["uncertainty"] = "invalid-timestamp"
            continue
        if parent_ts is None:
            invalid_timestamp_event_ids.add(parent["id"])
            parent["uncertainty"] = "invalid-timestamp"
            continue

        lag_seconds = max(0.0, (child_ts - parent_ts).total_seconds())

        parent_account = parent["account"]
        child_account = event["account"]
        ensure_node(parent_account)
        ensure_node(child_account)

        edges.append(
            {
                "from": parent_account,
                "to": child_account,
                "parent_event_id": parent_id,
                "child_event_id": event["id"],
                "content_id": event.get("content_id") or parent.get("content_id"),
                "lag_seconds": lag_seconds,
                "direct": True,
                "uncertainty": {
                    "parent": parent.get("uncertainty", "unknown"),
                    "child": event.get("uncertainty", "unknown"),
                },
            }
        )

    pathways = detect_repeated_amplification_pathways(ordered_events, events_by_id)

    uncertainty: Dict[str, Any]
    if invalid_timestamp_event_ids:
        uncertainty = {
            "status": "uncertain",
            "code": "invalid_timestamps",
            "message": "One or more events had malformed timestamps; related edges/pathways were skipped.",
            "invalid_timestamp_event_ids": sorted(invalid_timestamp_event_ids),
        }
    else:
        uncertainty = {"status": "ok"}

    return {
        "graph": {
            "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
            "edges": edges,
        },
        "pathways": pathways,
        "uncertainty": uncertainty,
    }


def detect_repeated_amplification_pathways(
    ordered_events: Sequence[Dict[str, Any]],
    events_by_id: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """Detect repeated account-to-account amplification pathways + basic metrics."""

    path_counter: Counter[Tuple[str, ...]] = Counter()
    path_metrics: Dict[Tuple[str, ...], Dict[str, Any]] = defaultdict(
        lambda: {
            "frequency": 0,
            "direct_occurrences": 0,
            "indirect_occurrences": 0,
            "lags": [],
            "uncertainty_labels": Counter(),
            "content_ids": Counter(),
        }
    )

    for event in ordered_events:
        chain_events: List[Dict[str, Any]] = [event]
        current = event
        visited_event_ids = {event.get("id")}

        while current.get("amplified_from_event_id"):
            parent_id = current["amplified_from_event_id"]
            parent = events_by_id.get(parent_id)
            if not parent:
                break
            if parent_id in visited_event_ids:
                chain_events.append(
                    {
                        "id": parent_id,
                        "account": parent.get("account", "unknown"),
                        "timestamp": parent.get("timestamp", event.get("timestamp", "")),
                        "uncertainty": "cycle-detected",
                    }
                )
                break
            chain_events.append(parent)
            visited_event_ids.add(parent_id)
            current = parent

        chain_events.reverse()
        account_path = tuple(item["account"] for item in chain_events)
        if len(account_path) < 2:
            continue

        root_ts = _safe_parse_ts(chain_events[0]["timestamp"])
        leaf_ts = _safe_parse_ts(chain_events[-1]["timestamp"])
        if root_ts is None or leaf_ts is None:
            for item in chain_events:
                item.setdefault("uncertainty", "invalid-timestamp")
            continue

        total_lag = max(0.0, (leaf_ts - root_ts).total_seconds())

        path_counter[account_path] += 1
        metrics = path_metrics[account_path]
        metrics["frequency"] += 1
        if len(account_path) == 2:
            metrics["direct_occurrences"] += 1
        else:
            metrics["indirect_occurrences"] += 1
        metrics["lags"].append(total_lag)

        for item in chain_events:
            metrics["uncertainty_labels"][item.get("uncertainty", "unknown")] += 1
        content_id = event.get("content_id")
        if content_id:
            metrics["content_ids"][content_id] += 1

    repeated = []
    for path, frequency in path_counter.items():
        if frequency < 2:
            continue
        m = path_metrics[path]
        avg_lag_seconds = (sum(m["lags"]) / len(m["lags"])) if m["lags"] else 0.0
        repeated.append(
            {
                "path": list(path),
                "frequency": m["frequency"],
                "avg_lag_seconds": avg_lag_seconds,
                "direct_occurrences": m["direct_occurrences"],
                "indirect_occurrences": m["indirect_occurrences"],
                "content_ids": dict(m["content_ids"]),
                "uncertainty_labels": dict(m["uncertainty_labels"]),
            }
        )

    repeated.sort(key=lambda item: (-item["frequency"], item["path"]))
    return {"repeated_pathways": repeated}
