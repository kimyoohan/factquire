#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "model_fact.schema.json"
FACTS_PATH = ROOT / "data" / "facts.json"

MIN_ENTRIES = 40
MIN_PROVIDERS = 6
PRICING_FIELDS = {
    "pricing.input_per_mtok",
    "pricing.output_per_mtok",
    "pricing.cached_input_per_mtok",
    "pricing.batch_discount_pct",
}
CONTEXT_FIELDS = {
    "context_window_tokens",
    "max_output_tokens",
}


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RuntimeError(f"Missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def source_fields(entry):
    fields = set()
    for source in entry.get("sources", []):
        fields.update(source.get("fields", []))
    return fields


def populated_checked_fields(entry):
    populated = set()
    pricing = entry.get("pricing", {})
    for field in PRICING_FIELDS:
        key = field.split(".", 1)[1]
        if pricing.get(key) is not None:
            populated.add(field)
    for field in CONTEXT_FIELDS:
        if entry.get(field) is not None:
            populated.add(field)
    return populated


def main():
    errors = []
    try:
        schema = load_json(SCHEMA_PATH)
        facts = load_json(FACTS_PATH)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    if not isinstance(facts, list):
        errors.append("data/facts.json must be a JSON array")
        facts = []

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for index, entry in enumerate(facts):
        for error in sorted(validator.iter_errors(entry), key=lambda err: list(err.path)):
            path = ".".join(str(part) for part in error.path) or "<entry>"
            model = entry.get("model_id", f"index {index}") if isinstance(entry, dict) else f"index {index}"
            errors.append(f"{model}: schema {path}: {error.message}")

    if len(facts) < MIN_ENTRIES:
        errors.append(f"Expected at least {MIN_ENTRIES} entries, found {len(facts)}")

    providers = {entry.get("provider") for entry in facts if isinstance(entry, dict)}
    if len(providers) < MIN_PROVIDERS:
        errors.append(f"Expected at least {MIN_PROVIDERS} providers, found {len(providers)}")

    keys = Counter(
        (entry.get("provider"), entry.get("model_id"))
        for entry in facts
        if isinstance(entry, dict)
    )
    for key, count in keys.items():
        if count > 1:
            errors.append(f"Duplicate provider/model_id: {key[0]} {key[1]}")

    for entry in facts:
        if not isinstance(entry, dict):
            continue
        model = f"{entry.get('provider')}/{entry.get('model_id')}"
        sources = entry.get("sources", [])
        if not sources:
            errors.append(f"{model}: missing sources")
        for idx, source in enumerate(sources):
            for field in ("url", "accessed_at", "quote"):
                if not source.get(field):
                    errors.append(f"{model}: source {idx} missing non-empty {field}")

        covered = source_fields(entry)
        for field in sorted(populated_checked_fields(entry) - covered):
            errors.append(f"{model}: non-null {field} not listed in any source fields")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validation passed: {len(facts)} entries, "
        f"{len(providers)} providers, {len(keys)} unique provider/model pairs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
