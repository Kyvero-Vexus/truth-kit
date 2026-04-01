import json
import unittest
from pathlib import Path

from tools.archive.change_detector import analyze_archive_input


class ArchiveChangeDetectorTests(unittest.TestCase):
    def _fixture(self):
        fixture_path = (
            Path(__file__).resolve().parents[1]
            / "benchmarks"
            / "datasets"
            / "dork-fixture-002-archive-reconstruction.json"
        )
        return json.loads(fixture_path.read_text(encoding="utf-8"))

    def test_mvp2_tc01_tc02_tc03_fixture_expected_changes(self):
        fixture = self._fixture()
        result = analyze_archive_input(fixture["input"])

        self.assertEqual(result["snapshotCount"], 3)
        self.assertGreaterEqual(len(result["changeEvents"]), 2)

        first = result["changeEvents"][0]
        self.assertEqual(first["fromSnapshotId"], "s1")
        self.assertEqual(first["toSnapshotId"], "s2")
        self.assertEqual(first["changeType"], "claim-reversal")
        self.assertIn("no contamination -> low-level contamination", first["summary"])

        second = result["changeEvents"][1]
        self.assertEqual(second["fromSnapshotId"], "s2")
        self.assertEqual(second["toSnapshotId"], "s3")
        self.assertEqual(second["changeType"], "scope-expansion")
        self.assertIn("mitigation underway", second["summary"])

    def test_mvp2_tc04_incomplete_coverage_reports_uncertainty(self):
        payload = {
            "targetUrl": "https://publisher.example/release/river-study",
            "snapshots": [
                {
                    "snapshotId": "s1",
                    "capturedAt": "2022-02-11T12:00:00Z",
                    "archiveProvider": "wayback",
                    "text": "Initial release: no contamination detected.",
                },
                {
                    "snapshotId": "s2",
                    "capturedAt": "2022-02-18T12:00:00Z",
                    "archiveProvider": "wayback",
                    "text": "Updated release: low-level contamination detected.",
                },
            ],
        }

        result = analyze_archive_input(payload)

        self.assertFalse(result["uncertainty"]["coverageComplete"])
        self.assertIn("Low snapshot count", " ".join(result["uncertainty"]["notes"]))
        self.assertEqual(result["uncertainty"]["overallProvenanceConfidence"], "low")

    def test_mvp2_tc05_single_snapshot_returns_no_false_change_events(self):
        payload = {
            "targetUrl": "https://publisher.example/release/river-study",
            "snapshots": [
                {
                    "snapshotId": "s1",
                    "capturedAt": "2022-02-11T12:00:00Z",
                    "archiveProvider": "wayback",
                    "text": "Initial release: no contamination detected.",
                }
            ],
        }

        result = analyze_archive_input(payload)

        self.assertEqual(result["changeEvents"], [])
        self.assertFalse(result["uncertainty"]["coverageComplete"])
        self.assertIn("Low snapshot count", " ".join(result["uncertainty"]["notes"]))

    def test_mvp2_tc06_out_of_order_snapshots_are_normalized(self):
        fixture = self._fixture()
        snapshots = fixture["input"]["snapshots"]
        payload = {
            "targetUrl": fixture["input"]["targetUrl"],
            "snapshots": [snapshots[2], snapshots[0], snapshots[1]],
        }

        result = analyze_archive_input(payload)

        self.assertGreaterEqual(len(result["changeEvents"]), 2)
        self.assertEqual(result["changeEvents"][0]["fromSnapshotId"], "s1")
        self.assertEqual(result["changeEvents"][0]["toSnapshotId"], "s2")
        self.assertEqual(result["changeEvents"][1]["fromSnapshotId"], "s2")
        self.assertEqual(result["changeEvents"][1]["toSnapshotId"], "s3")

    def test_preserves_access_path_metadata(self):
        payload = {
            "targetUrl": "https://publisher.example/release/river-study",
            "snapshots": [
                {
                    "snapshotId": "s1",
                    "capturedAt": "2022-02-11T12:00:00Z",
                    "archiveProvider": "wayback",
                    "accessPath": "cache://wayback/s1",
                    "text": "Initial release: no contamination detected.",
                },
                {
                    "snapshotId": "s2",
                    "capturedAt": "2022-02-18T12:00:00Z",
                    "archiveProvider": "wayback",
                    "retrieval": {"accessPath": "https://web.archive.org/web/s2"},
                    "text": "Updated release: low-level contamination detected.",
                },
            ],
        }

        result = analyze_archive_input(payload)

        self.assertEqual(result["snapshotProvenance"][0]["accessPath"], "cache://wayback/s1")
        self.assertEqual(result["snapshotProvenance"][1]["accessPath"], "https://web.archive.org/web/s2")
        self.assertEqual(result["changeEvents"][0]["fromAccessPath"], "cache://wayback/s1")
        self.assertEqual(result["changeEvents"][0]["toAccessPath"], "https://web.archive.org/web/s2")

    def test_invalid_timestamps_emit_uncertainty_without_directional_reversal(self):
        payload = {
            "targetUrl": "https://publisher.example/release/river-study",
            "snapshots": [
                {
                    "snapshotId": "s_new",
                    "capturedAt": "2022-02-18T12:00:00Z",
                    "archiveProvider": "wayback",
                    "text": "Updated release: low-level contamination detected.",
                },
                {
                    "snapshotId": "s_old",
                    "capturedAt": "not-a-timestamp",
                    "archiveProvider": "mirror-archive",
                    "text": "Initial release: no contamination detected.",
                },
            ],
        }

        result = analyze_archive_input(payload)

        self.assertTrue(result["uncertainty"]["temporalOrderingUncertain"])
        self.assertIn("invalid", " ".join(result["uncertainty"]["notes"]).lower())
        self.assertFalse(any(e["changeType"] == "claim-reversal" for e in result["changeEvents"]))


if __name__ == "__main__":
    unittest.main()
