#!/usr/bin/env python3
import sys
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.logic_check import (  # noqa: E402
    audit_numeric_field,
    exact_candidate_matches,
    price_candidates,
    rule_accessed_at_age,
    rule_active_with_inactive_quote,
    rule_changelog_coverage,
    rule_context_less_than_output,
    rule_duplicates_and_permalink_collisions,
    rule_output_less_than_input,
    rule_price_ratio_slips,
    rule_same_model_context,
    token_candidates,
)


def fact(provider="acme", model_id="model-a", **overrides):
    entry = {
        "provider": provider,
        "model_id": model_id,
        "display_name": model_id,
        "status": "ga",
        "release_date": None,
        "deprecation_date": None,
        "retirement_date": None,
        "pricing": {
            "input_per_mtok": 1.0,
            "output_per_mtok": 2.0,
            "cached_input_per_mtok": None,
            "batch_discount_pct": None,
        },
        "context_window_tokens": 1000,
        "max_output_tokens": 100,
        "modalities": {"input": ["text"], "output": ["text"]},
        "knowledge_cutoff": None,
        "sources": [
            {
                "url": "https://example.com",
                "accessed_at": "2026-07-04T00:00:00Z",
                "fields": ["pricing.input_per_mtok", "pricing.output_per_mtok", "context_window_tokens", "max_output_tokens", "modalities"],
                "quote": "Input $1.00 Output $2.00 Context Window 1,000 Max Output Tokens 100 Input modalities Text Output modalities Text",
            }
        ],
        "verified_at": "2026-07-04T00:00:00Z",
        "notes": None,
    }
    for key, value in overrides.items():
        entry[key] = value
    return entry


class LogicCheckTests(unittest.TestCase):
    def test_price_unit_conversions_match_per_mtok(self):
        self.assertTrue(exact_candidate_matches(1.0, price_candidates("Input $0.000001 per token")))
        self.assertTrue(exact_candidate_matches(5.0, price_candidates("Input $0.005 per 1K tokens")))
        self.assertTrue(exact_candidate_matches(0.9, price_candidates("Price per 1M tokens $0.90")))

    def test_token_suffix_conversions_are_ambiguous(self):
        decimal_match = exact_candidate_matches(128000, token_candidates("Context length 128K"))
        binary_match = exact_candidate_matches(131072, token_candidates("Context length 128K"))

        self.assertTrue(decimal_match)
        self.assertTrue(binary_match)
        self.assertTrue(decimal_match[0].ambiguous)
        self.assertTrue(binary_match[0].ambiguous)

    def test_numeric_quote_disagreement_is_critical(self):
        entry = fact()
        entry["pricing"]["input_per_mtok"] = 3.0
        entry["sources"][0]["quote"] = "Input price $1.00 per 1M tokens"

        findings = audit_numeric_field(entry, "pricing.input_per_mtok")

        self.assertEqual(findings[0].class_name, "CRITICAL")

    def test_rule_1_same_model_context_divergence(self):
        findings = rule_same_model_context(
            [
                fact("groq", "openai/gpt-oss-120b", context_window_tokens=128000),
                fact("together", "gpt-oss-120b", context_window_tokens=131072),
            ]
        )

        self.assertEqual(findings[0].class_name, "RULE-1")

    def test_rule_2_output_lower_than_input(self):
        entry = fact()
        entry["pricing"]["input_per_mtok"] = 2.0
        entry["pricing"]["output_per_mtok"] = 1.0

        self.assertEqual(rule_output_less_than_input([entry])[0].class_name, "RULE-2")

    def test_rule_3_context_lower_than_output(self):
        self.assertEqual(rule_context_less_than_output([fact(context_window_tokens=10, max_output_tokens=20)])[0].class_name, "RULE-3")

    def test_rule_4_exact_price_ratio_same_model(self):
        left = fact("provider-a", "same-model")
        right = fact("provider-b", "same-model")
        right["pricing"]["input_per_mtok"] = 2.0

        self.assertEqual(rule_price_ratio_slips([left, right])[0].class_name, "RULE-4")

    def test_rule_5_active_status_with_inactive_language(self):
        entry = fact()
        entry["sources"][0]["quote"] = "This model is deprecated and will be retired soon."

        self.assertEqual(rule_active_with_inactive_quote([entry])[0].class_name, "RULE-5")

    def test_rule_6_accessed_at_future_or_stale(self):
        stale = fact("acme", "stale")
        stale["sources"][0]["accessed_at"] = "2026-06-01T00:00:00Z"
        future = fact("acme", "future")
        future["sources"][0]["accessed_at"] = "2026-07-05T00:00:00Z"

        findings = rule_accessed_at_age([stale, future], today=date(2026, 7, 4))

        self.assertEqual([finding.class_name for finding in findings], ["RULE-6", "RULE-6"])

    def test_rule_7_duplicates_and_permalink_collisions(self):
        findings = rule_duplicates_and_permalink_collisions(
            [
                fact("acme", "duplicate"),
                fact("acme", "duplicate"),
                fact("acme", "a.b"),
                fact("acme", "a_b"),
            ]
        )

        self.assertGreaterEqual(sum(1 for finding in findings if finding.class_name == "RULE-7"), 2)

    def test_rule_8_changelog_coverage(self):
        findings = rule_changelog_coverage(
            [fact("acme", "present")],
            {
                "releases": [
                    {
                        "entries": [
                            {"type": "added", "provider": "acme", "model_id": "missing"},
                        ]
                    }
                ]
            },
        )

        self.assertEqual([finding.class_name for finding in findings], ["RULE-8", "RULE-8"])


if __name__ == "__main__":
    unittest.main()
