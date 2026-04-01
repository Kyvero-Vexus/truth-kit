import copy
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
    # MVP3-TC01
    def test_workflow_routing_maps_each_supported_workflow(self):
        query_type_by_workflow = {
            "claim-tracing": "reverse.text",
            "archive-recovery": "archive.lookup",
            "provenance-analysis": "reverse.document",
            "manual-review": "reverse.text",
        }
        base_alert = _alert_from_fixture("trend-fixture-002-multi-source-breakout.json")

        for workflow, expected_query_type in query_type_by_workflow.items():
            with self.subTest(workflow=workflow):
                alert = copy.deepcopy(base_alert)
                alert["nextStep"]["workflow"] = workflow
                request = adapt_trend_alert(alert)
                self.assertIsNotNone(request)
                assert request is not None
                self.assertEqual(request["queryType"], expected_query_type)

        none_alert = copy.deepcopy(base_alert)
        none_alert["nextStep"]["workflow"] = "none"
        self.assertIsNone(adapt_trend_alert(none_alert))

    # MVP3-TC02
    def test_none_workflow_returns_none(self):
        alert = _alert_from_fixture("trend-fixture-001-single-source-noise.json")
        self.assertIsNone(adapt_trend_alert(alert))

    # MVP3-TC03
    def test_evidence_urls_and_snippets_are_preserved_in_inputs(self):
        alert = _alert_from_fixture("trend-fixture-002-multi-source-breakout.json")
        request = adapt_trend_alert(alert)
        self.assertIsNotNone(request)
        assert request is not None

        urls = [x["value"] for x in request["inputs"] if x["kind"] == "url"]
        snippets = [x["value"] for x in request["inputs"] if x["kind"] == "text"]
        self.assertEqual(len(urls), len(alert["evidence"]))
        self.assertTrue(all(ev["url"] in urls for ev in alert["evidence"]))
        self.assertTrue(all(ev["snippet"] in snippets for ev in alert["evidence"]))
        self.assertIn(alert["topic"]["label"], snippets)

    # MVP3-TC04
    def test_policy_defaults_are_present(self):
        alert = _alert_from_fixture("trend-fixture-002-multi-source-breakout.json")
        request = adapt_trend_alert(alert)
        self.assertIsNotNone(request)
        assert request is not None

        policy = request["retrievalPolicy"]
        self.assertEqual(policy["cacheMode"], "prefer-cache")
        self.assertEqual(policy["maxConcurrentRequests"], 4)
        self.assertEqual(policy["maxRequestsPerHostPerMinute"], 20)
        self.assertEqual(policy["retry"]["maxAttempts"], 3)
        self.assertEqual(policy["retry"]["backoff"], "exponential-jitter")
        self.assertTrue(policy["respectRetryAfter"])
        self.assertTrue(policy["respectRobotsTxt"])

    # MVP3-TC05
    def test_fixture_routing_001_002_003_matches_expected_outcomes(self):
        fixture_expectations = {
            "trend-fixture-001-single-source-noise.json": None,
            "trend-fixture-002-multi-source-breakout.json": "reverse.text",
            "trend-fixture-003-high-impact-manual-review.json": "reverse.text",
        }

        for fixture_name, expected_query_type in fixture_expectations.items():
            with self.subTest(fixture=fixture_name):
                alert = _alert_from_fixture(fixture_name)
                request = adapt_trend_alert(alert)
                if expected_query_type is None:
                    self.assertIsNone(request)
                else:
                    self.assertIsNotNone(request)
                    assert request is not None
                    self.assertEqual(request["queryType"], expected_query_type)

    # MVP3-TC08 (P1)
    def test_same_alert_input_produces_identical_request(self):
        alert = _alert_from_fixture("trend-fixture-002-multi-source-breakout.json")
        request_a = adapt_trend_alert(alert)
        request_b = adapt_trend_alert(copy.deepcopy(alert))
        self.assertEqual(request_a, request_b)

    # MVP3-TC09 (P1)
    def test_malformed_next_step_type_returns_noop(self):
        alert = _alert_from_fixture("trend-fixture-002-multi-source-breakout.json")
        alert["nextStep"] = ["claim-tracing"]
        self.assertIsNone(adapt_trend_alert(alert))

    # MVP3-TC11 (P1)
    def test_mapped_workflow_with_empty_inputs_returns_noop(self):
        alert = {
            "schemaVersion": "0.1.0",
            "alertId": "empty-input-001",
            "generatedAt": "2026-01-01T00:00:00Z",
            "status": "new",
            "topic": {"label": "   "},
            "confidence": "medium",
            "summary": "No usable evidence",
            "scores": {"corroboration": 0.7},
            "evidence": [{"url": "", "snippet": "   "}],
            "nextStep": {"workflow": "claim-tracing", "priority": "p2", "delegateTo": "truth-kit-native"},
        }

        self.assertIsNone(adapt_trend_alert(alert))

    # MVP3-TC10 (P2)
    def test_sparse_but_valid_alert_transforms_with_defaults(self):
        alert = {
            "schemaVersion": "0.1.0",
            "alertId": "sparse-001",
            "generatedAt": "2026-01-01T00:00:00Z",
            "status": "new",
            "topic": {"label": "Sparse alert"},
            "confidence": "medium",
            "summary": "Minimal alert",
            "scores": {"corroboration": 0.6},
            "evidence": [],
            "nextStep": {"workflow": "claim-tracing", "priority": "p2", "delegateTo": "truth-kit-native"},
        }

        request = adapt_trend_alert(alert)
        self.assertIsNotNone(request)
        assert request is not None
        self.assertEqual(request["requestId"], "trend-alert:sparse-001")
        self.assertEqual(request["queryType"], "reverse.text")
        self.assertEqual(request["retrievalPolicy"]["cacheMode"], "prefer-cache")
        self.assertEqual(request["constraints"], {"maxSources": 20, "maxDepth": 3})


if __name__ == "__main__":
    unittest.main()
