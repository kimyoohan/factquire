#!/usr/bin/env python3
import json
import sys
from pathlib import Path


IGNORED_FIELDS = {"sources", "verified_at", "notes"}


def model_key(entry):
    return (entry["provider"], entry["model_id"])


def leaf_values(value, prefix=""):
    if isinstance(value, dict):
        for key in sorted(value):
            if not prefix and key in IGNORED_FIELDS:
                continue
            child_prefix = f"{prefix}.{key}" if prefix else key
            yield from leaf_values(value[key], child_prefix)
    else:
        yield prefix, value


def load_facts(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def diff_facts(old_facts, new_facts):
    old_by_key = {model_key(entry): entry for entry in old_facts}
    new_by_key = {model_key(entry): entry for entry in new_facts}
    entries = []

    for provider, model_id in sorted(new_by_key.keys() - old_by_key.keys()):
        entries.append({"type": "added", "provider": provider, "model_id": model_id})

    for provider, model_id in sorted(old_by_key.keys() - new_by_key.keys()):
        entries.append({"type": "removed", "provider": provider, "model_id": model_id})

    for key in sorted(old_by_key.keys() & new_by_key.keys()):
        old_leafs = dict(leaf_values(old_by_key[key]))
        new_leafs = dict(leaf_values(new_by_key[key]))
        for field in sorted(old_leafs.keys() | new_leafs.keys()):
            old_value = old_leafs.get(field)
            new_value = new_leafs.get(field)
            if old_value != new_value:
                entries.append(
                    {
                        "type": "changed",
                        "provider": key[0],
                        "model_id": key[1],
                        "field": field,
                        "old": old_value,
                        "new": new_value,
                    }
                )

    return entries


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print("Usage: py scripts/diff_facts.py <old_facts.json> <new_facts.json>", file=sys.stderr)
        return 2

    entries = diff_facts(load_facts(argv[0]), load_facts(argv[1]))
    print(json.dumps(entries, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
