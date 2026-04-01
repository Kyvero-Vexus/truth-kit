import json
import unittest
from pathlib import Path

from tools.common.trendalert_investigation_adapter import adapt_trend_alert


REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = REPO_ROOT / "benchmarks" / "datasets"


def _load_fixture(name: str):
    return json.loads((DATASET_DIR / name).read_text(encoding="utf-8"))


def _alert_from_fixture(fixture_name: str):
    fixture = _load_fixture(fixture_name)
    events = fixture["events"]
    expected = fixture.get("expected", {})
    workflow = expected.get("expectedWorkflow", "none")
    confidence = expected.get("expectedConfidence") or expected.get("minimumConfidence", "low")

    evidence = [
        {
            "eventId": event["eventId"],
            "sourceId": event["sourceId"],
            "url": f"https://example.test/{event['eventId']}",
            "snippet": event["title"],
            "publishedAt": event["capturedAt"],
        }
        for event in events
    ]

    return {
        "schemaVersion": "0.1.0",
        "alertId": fixture["fixtureId"],
        "generatedAt": events[-1]["capturedAt"],
        "status": "new",
        "topic": {"label": events[0]["title"]},
        "confidence": confidence,
        "summary": fixture["description"],
        "scores": {
            "corroboration": expected.get("minimumCorroborationScore", expected.get("maximumCorroborationScore", 0.4))
        },
        "evidence": evidence,
        "nextStep": {"workflow": workflow, "priority": "p1", "delegateTo": "truth-kit-native"},
    }


class TrendAlertInvestigationAdapterTests(unittest.TestCase):
    def test_single_source_noise_none_workflow_skips_request(self):
        alert = _alert_from_fixture("trend-fixture-001-single-source-noise.json")
        self.assertIsNone(adapt_trend_alert(alert))

    def test_multi_source_breakout_claim_tracing_routing_and_inputs(self):
        alert = _alert_from_fixture("trend-fixture-002-multi-source-breakout.json")
        request = adapt_trend_alert(alert)
        self.assertIsNotNone(request)
        assert request is not None
        self.assertEqual(request["queryType"], "reverse.text")
        self.assertEqual(request["requestId"], f"trend-alert:{alert['alertId']}")
        self.assertEqual(request["constraints"], {"maxSources": 20, "maxDepth": 3})

        urls = [x["value"] for x in request["inputs"] if x["kind"] == "url"]
        snippets = [x["value"] for x in request["inputs"] if x["kind"] == "text"]
        self.assertEqual(len(urls), len(alert["evidence"]))
        self.assertTrue(all(ev["snippet"] in snippets for ev in alert["evidence"]))
        self.assertIn(alert["topic"]["label"], snippets)
        self.assertFalse(request["toolHints"]["allowDelegationToDork"])

    def test_high_impact_manual_review_uses_low_depth_defaults(self):
        alert = _alert_from_fixture("trend-fixture-003-high-impact-manual-review.json")
        request = adapt_trend_alert(alert)
        self.assertIsNotNone(request)
        assert request is not None
        self.assertEqual(request["queryType"], "reverse.text")
        self.assertEqual(request["constraints"]["maxDepth"], 2)
        self.assertEqual(request["retrievalPolicy"]["cacheMode"], "prefer-cache")
        self.assertEqual(request["retrievalPolicy"]["maxConcurrentRequests"], 4)
        self.assertEqual(request["retrievalPolicy"]["maxRequestsPerHostPerMinute"], 20)
        self.assertFalse(request["toolHints"]["allowDelegationToDork"])


if __name__ == "__main__":
    unittest.main()
