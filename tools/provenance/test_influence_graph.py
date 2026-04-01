import json
import unittest
from pathlib import Path

from tools.provenance.influence_graph import build_influence_graph


class InfluenceGraphTests(unittest.TestCase):
    def setUp(self):
        fixture_path = (
            Path(__file__).resolve().parents[2]
            / "benchmarks"
            / "datasets"
            / "influence-fixture-001-repeated-amplification.json"
        )
        with fixture_path.open("r", encoding="utf-8") as f:
            self.fixture = json.load(f)

    def _run_fixture(self):
        return build_influence_graph(
            self.fixture["events"],
            state_seed_accounts=self.fixture["state_seed_accounts"],
            influencer_seed_accounts=self.fixture["influencer_seed_accounts"],
        )

    def test_mvp5_tc01_tc02_tc03_tc04_tc05(self):
        result = self._run_fixture()
        self.assertIn("graph", result)
        self.assertIn("nodes", result["graph"])
        self.assertIn("edges", result["graph"])
        self.assertGreaterEqual(len(result["graph"]["nodes"]), 1)
        self.assertGreaterEqual(len(result["graph"]["edges"]), 1)

        nodes = {node["id"]: node for node in result["graph"]["nodes"]}
        self.assertIn("state_affiliated_seed", nodes["state_media_alpha"]["seed_tags"])
        self.assertIn("influencer_seed", nodes["influencer_echo"]["seed_tags"])

        repeated = result["pathways"]["repeated_pathways"]
        matching = [
            item
            for item in repeated
            if item["path"]
            == ["state_media_alpha", "influencer_echo", "community_forum_1"]
        ]
        self.assertEqual(len(matching), 1)

        pathway = matching[0]
        self.assertEqual(pathway["frequency"], 2)
        self.assertEqual(pathway["direct_occurrences"], 0)
        self.assertEqual(pathway["indirect_occurrences"], 2)
        self.assertGreater(pathway["avg_lag_seconds"], 0)
        self.assertIn("verified", pathway["uncertainty_labels"])
        self.assertIn("likely", pathway["uncertainty_labels"])

    def test_mvp5_tc06_rank_stability(self):
        first = self._run_fixture()
        second = self._run_fixture()
        self.assertEqual(
            first["pathways"]["repeated_pathways"],
            second["pathways"]["repeated_pathways"],
        )

    def test_mvp5_tc09_cyclic_graph_does_not_loop(self):
        cycle_events = [
            {
                "id": "c1",
                "content_id": "cc1",
                "account": "a",
                "timestamp": "2026-03-30T12:00:00Z",
                "amplified_from_event_id": "c2",
                "uncertainty": "likely",
            },
            {
                "id": "c2",
                "content_id": "cc1",
                "account": "b",
                "timestamp": "2026-03-30T12:01:00Z",
                "amplified_from_event_id": "c1",
                "uncertainty": "likely",
            },
        ]

        result = build_influence_graph(cycle_events)
        self.assertIn("repeated_pathways", result["pathways"])
        self.assertEqual(result["pathways"]["repeated_pathways"], [])

    def test_duplicate_event_ids_rejected_deterministically(self):
        events = [
            {"id": "evt-1", "account": "alpha", "timestamp": "2024-01-01T00:00:00Z"},
            {
                "id": "evt-1",
                "account": "beta",
                "timestamp": "2024-01-01T00:05:00Z",
                "amplified_from_event_id": "evt-1",
            },
            {"id": "evt-2", "account": "gamma", "timestamp": "2024-01-01T00:06:00Z"},
            {"id": "evt-2", "account": "delta", "timestamp": "2024-01-01T00:07:00Z"},
        ]

        result = build_influence_graph(events)
        self.assertEqual(result["uncertainty"]["status"], "error")
        self.assertEqual(result["uncertainty"]["code"], "duplicate_event_ids")
        self.assertEqual(result["uncertainty"]["duplicate_event_ids"], ["evt-1", "evt-2"])
        self.assertEqual(result["graph"]["nodes"], [])
        self.assertEqual(result["graph"]["edges"], [])

    def test_malformed_timestamp_marks_uncertainty_without_exception(self):
        events = [
            {"id": "root", "account": "origin", "timestamp": "2024-01-01T00:00:00Z"},
            {
                "id": "child-bad-ts",
                "account": "amplifier",
                "timestamp": "definitely-not-an-iso-timestamp",
                "amplified_from_event_id": "root",
            },
        ]

        result = build_influence_graph(events)
        self.assertEqual(result["uncertainty"]["status"], "uncertain")
        self.assertEqual(result["uncertainty"]["code"], "invalid_timestamps")
        self.assertEqual(result["uncertainty"]["invalid_timestamp_event_ids"], ["child-bad-ts"])
        self.assertEqual(result["graph"]["edges"], [])


if __name__ == "__main__":
    unittest.main()
