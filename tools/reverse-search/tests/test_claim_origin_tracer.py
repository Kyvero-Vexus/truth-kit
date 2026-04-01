import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "tools" / "reverse-search" / "claim_origin_tracer.py"
FIXTURE_PATH = ROOT / "benchmarks" / "datasets" / "dork-fixture-001-known-source-recovery.json"

spec = importlib.util.spec_from_file_location("claim_origin_tracer", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ClaimOriginTracerTests(unittest.TestCase):
    def test_fixture_known_source_recovery(self):
        """MVP1-TC01 + MVP1-TC04."""
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        request = module._build_request_from_fixture(fixture)

        response = module.trace_claim_origin(request)

        self.assertIn(response["status"], {"ok", "partial"})
        self.assertEqual(response["queryType"], "reverse.text")

        results_by_id = {item["resultId"]: item for item in response["results"]}

        self.assertIn("src-1", results_by_id)
        self.assertEqual(response["results"][0]["resultId"], fixture["expected"]["earliestReachableSourceDocId"])

        required_relationships = {
            item["docId"]: item["relationship"]
            for item in fixture["expected"]["requiredRelationships"]
        }
        for doc_id, relationship in required_relationships.items():
            self.assertIn(doc_id, results_by_id)
            self.assertEqual(results_by_id[doc_id]["provenance"]["relationship"], relationship)

        minimum = fixture["expected"]["minimumProvenanceConfidence"]
        min_rank = module.CONFIDENCE_ORDER[minimum]
        self.assertGreaterEqual(
            module.CONFIDENCE_ORDER[results_by_id["src-1"]["provenance"]["confidence"]],
            min_rank,
        )

    def test_quote_and_url_inputs_are_accepted(self):
        """MVP1-TC02."""
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        docs = fixture["input"]["documents"]

        quote_request = {
            "schemaVersion": "0.1.0",
            "requestId": "quote-case",
            "queryType": "reverse.quote",
            "inputs": [
                {"kind": "quote", "value": fixture["input"]["claim"], "metadata": {"documents": docs}}
            ],
        }
        url_request = {
            "schemaVersion": "0.1.0",
            "requestId": "url-case",
            "queryType": "reverse.text",
            "inputs": [
                {
                    "kind": "url",
                    "value": docs[0]["url"],
                    "metadata": {"documents": docs},
                }
            ],
        }

        quote_response = module.trace_claim_origin(quote_request)
        url_response = module.trace_claim_origin(url_request)

        self.assertTrue(quote_response["results"])
        self.assertTrue(url_response["results"])
        self.assertEqual(quote_response["results"][0]["resultId"], "src-1")

    def test_output_contract_minimum_fields(self):
        """MVP1-TC03."""
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        response = module.trace_claim_origin(module._build_request_from_fixture(fixture))

        self.assertIsInstance(response.get("results"), list)
        self.assertIn("uncertainty", response)
        self.assertIsInstance(response["uncertainty"], list)
        self.assertGreaterEqual(len(response["results"]), 1)

        first = response["results"][0]
        self.assertIn("provenance", first)
        self.assertIn("relationship", first["provenance"])
        self.assertIn("confidence", first["provenance"])

    def test_no_candidates_returns_partial_with_explicit_uncertainty(self):
        """MVP1-TC05 (P1 robustness)."""
        request = {
            "schemaVersion": "0.1.0",
            "requestId": "no-candidates",
            "queryType": "reverse.text",
            "inputs": [
                {
                    "kind": "text",
                    "value": "alpha beta gamma",
                    "metadata": {
                        "documents": [
                            {
                                "docId": "doc-a",
                                "url": "https://example.com/a",
                                "text": "unrelated tokens only",
                                "publishedAt": "2024-01-01T00:00:00Z",
                            }
                        ]
                    },
                }
            ],
        }

        response = module.trace_claim_origin(request)

        self.assertEqual(response["status"], "partial")
        self.assertEqual(response["results"], [])
        codes = {item["code"] for item in response["uncertainty"]}
        self.assertIn("no-plausible-candidates", codes)

    def test_deterministic_ordering_for_same_input(self):
        """MVP1-TC08 (P2 generalization)."""
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        request = module._build_request_from_fixture(fixture)

        first = module.trace_claim_origin(request)
        second = module.trace_claim_origin(request)

        self.assertEqual(
            [item["resultId"] for item in first["results"]],
            [item["resultId"] for item in second["results"]],
        )


if __name__ == "__main__":
    unittest.main()
