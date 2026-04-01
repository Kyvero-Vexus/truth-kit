from __future__ import annotations

import json
from pathlib import Path
import unittest

from tools.provenance.classifier import classify_topic_documents

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "benchmarks" / "datasets" / "dork-fixture-003-derivative-vs-primary.json"


class DerivativeSourceClassifierTests(unittest.TestCase):
    def test_fixture_expectations_match(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        result = classify_topic_documents(topic=payload["input"]["topic"], documents=payload["input"]["documents"])
        expected = payload["expected"]

        self.assertEqual(result["primaryDocIds"], expected["primaryDocIds"])
        for doc_id in expected["derivativeDocIds"]:
            self.assertIn(doc_id, {r["docId"] for r in result["relationships"]})

        rel_by_doc = {r["docId"]: r for r in result["relationships"]}
        for expectation in expected["relationshipExpectations"]:
            self.assertEqual(rel_by_doc[expectation["docId"]]["relationship"], expectation["relationship"])

    def test_confidence_and_rationale_present_for_all_relationships(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        result = classify_topic_documents(topic=payload["input"]["topic"], documents=payload["input"]["documents"])
        for rel in result["relationships"]:
            self.assertIn(rel["confidence"], {"low", "medium", "high"})
            self.assertIsInstance(rel["rationale"], str)
            self.assertTrue(rel["rationale"].strip())

    def test_unresolved_when_evidence_is_weak(self) -> None:
        docs = [
            {"docId": "a", "url": "https://example.test/a", "publishedAt": "2024-01-01T00:00:00Z", "text": "Brief market note with no data.", "citations": []},
            {"docId": "b", "url": "https://example.test/b", "publishedAt": "2024-01-02T00:00:00Z", "text": "Completely unrelated municipal updates.", "citations": []},
        ]
        result = classify_topic_documents("test", docs)
        rel_by_doc = {r["docId"]: r for r in result["relationships"]}
        self.assertEqual(rel_by_doc["b"]["relationship"], "unresolved")
        self.assertEqual(rel_by_doc["b"]["confidence"], "low")

    def test_explicit_citation_outweighs_weak_lexical_similarity(self) -> None:
        docs = [
            {"docId": "p1", "url": "https://example.test/p1", "publishedAt": "2024-01-01T00:00:00Z", "text": "Policy bulletin: river condition 412 and shelter updates.", "citations": []},
            {"docId": "p2", "url": "https://example.test/p2", "publishedAt": "2024-01-01T06:00:00Z", "text": "Regional memo about transit schedule changes and weather.", "citations": []},
            {"docId": "d1", "url": "https://example.test/d1", "publishedAt": "2024-01-02T00:00:00Z", "text": "A short digest that echoes a little wording from p2 and mentions updates.", "citations": ["https://example.test/p1"]},
        ]
        result = classify_topic_documents("test", docs)
        rel_by_doc = {r["docId"]: r for r in result["relationships"]}
        self.assertEqual(rel_by_doc["d1"]["relationship"], "explicit-citation")
        self.assertEqual(rel_by_doc["d1"]["dependsOn"], ["p1"])

    def test_earliest_high_evidence_source_preferred_as_primary(self) -> None:
        docs = [
            {"docId": "orig", "url": "https://example.test/orig", "publishedAt": "2024-01-01T00:00:00Z", "text": "Original reporting with tables and measurements.", "originalData": True, "citations": []},
            {"docId": "followup", "url": "https://example.test/followup", "publishedAt": "2024-01-02T00:00:00Z", "text": "Follow-up article summarizing the same event.", "citations": ["https://example.test/orig"]},
        ]
        result = classify_topic_documents("test", docs)
        rel_by_doc = {r["docId"]: r for r in result["relationships"]}
        self.assertEqual(result["primaryDocIds"], ["orig"])
        self.assertEqual(rel_by_doc["orig"]["relationship"], "primary-source")

    def test_future_citation_not_classified_as_high_confidence_explicit_dependence(self) -> None:
        docs = [
            {"docId": "origin", "url": "https://example.test/origin", "publishedAt": "2024-01-03T00:00:00Z", "text": "Initial report.", "citations": []},
            {"docId": "digest", "url": "https://example.test/digest", "publishedAt": "2024-01-02T00:00:00Z", "text": "Digest citing a future source.", "citations": ["https://example.test/origin"]},
        ]
        result = classify_topic_documents("test", docs)
        rel_by_doc = {r["docId"]: r for r in result["relationships"]}
        self.assertNotEqual(rel_by_doc["digest"]["relationship"], "explicit-citation")
        self.assertEqual(rel_by_doc["digest"]["relationship"], "unresolved")
        self.assertEqual(rel_by_doc["digest"]["confidence"], "low")

    def test_malformed_timestamp_does_not_crash_and_returns_uncertainty(self) -> None:
        docs = [
            {"docId": "origin", "url": "https://example.test/origin", "publishedAt": "2024-01-01T00:00:00Z", "text": "Original report with data.", "citations": []},
            {"docId": "badts", "url": "https://example.test/badts", "publishedAt": "not-a-timestamp", "text": "Follow-up report with unclear timing.", "citations": []},
        ]
        result = classify_topic_documents("test", docs)
        rel_by_doc = {r["docId"]: r for r in result["relationships"]}
        self.assertEqual(rel_by_doc["badts"]["relationship"], "unresolved")
        self.assertEqual(rel_by_doc["badts"]["confidence"], "low")
        self.assertIn("Malformed publishedAt", rel_by_doc["badts"]["rationale"])


if __name__ == "__main__":
    unittest.main()
