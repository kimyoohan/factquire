#!/usr/bin/env python3
import unittest
from copy import deepcopy
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.diff_facts import diff_facts


def fact(provider, model_id, status="ga", input_price=1.0, verified_at="2026-01-01T00:00:00Z"):
    return {
        "provider": provider,
        "model_id": model_id,
        "display_name": model_id,
        "status": status,
        "release_date": None,
        "deprecation_date": None,
        "retirement_date": None,
        "pricing": {
            "input_per_mtok": input_price,
            "output_per_mtok": 2.0,
            "cached_input_per_mtok": None,
            "batch_discount_pct": None,
        },
        "context_window_tokens": 1000,
        "max_output_tokens": 100,
        "modalities": {"input": ["text"], "output": ["text"]},
        "knowledge_cutoff": None,
        "sources": [{"url": "https://example.com", "accessed_at": verified_at, "quote": "example"}],
        "verified_at": verified_at,
        "notes": None,
    }


class DiffFactsTests(unittest.TestCase):
    def test_added_removed_and_changed_entries(self):
        old = [
            fact("acme", "stable", input_price=1.0, status="ga"),
            fact("acme", "removed"),
        ]
        new = [
            fact("acme", "stable", input_price=1.5, status="deprecated"),
            fact("acme", "added"),
        ]

        self.assertEqual(
            diff_facts(old, new),
            [
                {"type": "added", "provider": "acme", "model_id": "added"},
                {"type": "removed", "provider": "acme", "model_id": "removed"},
                {
                    "type": "changed",
                    "provider": "acme",
                    "model_id": "stable",
                    "field": "pricing.input_per_mtok",
                    "old": 1.0,
                    "new": 1.5,
                },
                {
                    "type": "changed",
                    "provider": "acme",
                    "model_id": "stable",
                    "field": "status",
                    "old": "ga",
                    "new": "deprecated",
                },
            ],
        )

    def test_sources_verified_at_and_notes_are_ignored(self):
        old = [fact("acme", "stable", verified_at="2026-01-01T00:00:00Z")]
        new = deepcopy(old)
        new[0]["sources"] = [{"url": "https://example.org", "accessed_at": "2026-02-01T00:00:00Z", "quote": "new"}]
        new[0]["verified_at"] = "2026-02-01T00:00:00Z"
        new[0]["notes"] = "refreshed evidence"

        self.assertEqual(diff_facts(old, new), [])


if __name__ == "__main__":
    unittest.main()
