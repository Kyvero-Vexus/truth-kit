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
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        request = module._build_request_from_fixture(fixture)

        response = module.trace_claim_origin(request)

        self.assertIn(response["status"], {"ok", "partial"})
        self.assertEqual(response["queryType"], "reverse.text")

        results_by_id = {item["resultId"]: item for item in response["results"]}

        # Earliest reachable source should be top-ranked by publish time.
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


if __name__ == "__main__":
    unittest.main()
