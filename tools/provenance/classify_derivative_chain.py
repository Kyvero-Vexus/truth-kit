#!/usr/bin/env python3
"""CLI for primary-vs-derivative source chain classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.provenance.classifier import classify_topic_documents


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify primary/derivative source relationships from a document set.")
    parser.add_argument("input_json", type=Path, help="Path to fixture/document-set JSON file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    input_section = payload.get("input", {})

    result = classify_topic_documents(
        topic=input_section.get("topic", ""),
        documents=input_section.get("documents", []),
    )

    if args.pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
