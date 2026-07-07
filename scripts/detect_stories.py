#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CURRENT = ROOT / "data" / "facts.json"
DEFAULT_ARCHIVE_DIR = ROOT / "data" / "archive"
DEFAULT_CHANGELOG = ROOT / "data" / "changelog.json"
DEFAULT_DRAFT_DIR = ROOT / "content" / "drafts"
DEFAULT_SUMMARY_DIR = ROOT / "ops" / "stories"

STORY_FIELDS = {
    "context_window_tokens",
    "max_output_tokens",
    "status",
    "deprecation_date",
    "retirement_date",
}
PRICING_PREFIX = "pricing."
DRAFT_STAMP = "STATUS: DRAFT - unverified by Claude; do not publish"


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def latest_archive_path(archive_dir):
    candidates = []
    for path in archive_dir.glob("facts-*.json"):
        match = re.match(r"facts-(\d{4}-\d{2}-\d{2})(?:-.+)?\.json$", path.name)
        if match:
            candidates.append((match.group(1), path.name, path))
    if not candidates:
        raise SystemExit(f"No facts-<date>.json archive found in {archive_dir}")
    return sorted(candidates)[-1][2]


def model_key(entry):
    return (entry.get("provider"), entry.get("model_id"))


def field_value(entry, field):
    if field.startswith(PRICING_PREFIX):
        return entry.get("pricing", {}).get(field.split(".", 1)[1])
    return entry.get(field)


def story_fields_for(entry):
    fields = set(STORY_FIELDS)
    pricing = entry.get("pricing", {})
    fields.update(f"{PRICING_PREFIX}{key}" for key in pricing)
    return fields


def real_changes(previous_facts, current_facts):
    previous_by_key = {model_key(entry): entry for entry in previous_facts}
    current_by_key = {model_key(entry): entry for entry in current_facts}
    changes = []

    for key in sorted(previous_by_key.keys() & current_by_key.keys()):
        previous = previous_by_key[key]
        current = current_by_key[key]
        for field in sorted(story_fields_for(previous) | story_fields_for(current)):
            old_value = field_value(previous, field)
            new_value = field_value(current, field)
            if old_value != new_value:
                changes.append(
                    {
                        "provider": key[0],
                        "model_id": key[1],
                        "display_name": current.get("display_name") or key[1],
                        "field": field,
                        "old_value": old_value,
                        "new_value": new_value,
                        "entry": current,
                    }
                )
    return changes


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "change"


def value_tokens(value):
    if value is None:
        return {"null", "none"}
    tokens = {str(value)}
    if isinstance(value, (int, float)):
        tokens.add(f"{value:,}")
        tokens.add(f"{float(value):.1f}")
        tokens.add(f"{float(value):.2f}")
        tokens.add(f"${float(value):.2f}")
        if float(value).is_integer():
            integer = int(value)
            tokens.add(str(integer))
            tokens.add(f"{integer:,}")
            tokens.add(f"${integer}")
    return {token for token in tokens if token}


def quote_contains_value(quote, value):
    normalized_quote = quote.lower()
    compact_quote = re.sub(r"\s+", "", normalized_quote)
    for token in value_tokens(value):
        normalized_token = token.lower()
        if normalized_token in normalized_quote:
            return True
        if re.sub(r"\s+", "", normalized_token) in compact_quote:
            return True
    return False


def source_for_change(entry, field, new_value):
    for source in entry.get("sources", []):
        quote = source.get("quote", "")
        if field in source.get("fields", []) and quote_contains_value(quote, new_value):
            return source
    return None


def yaml_scalar(value):
    return json.dumps(value, ensure_ascii=False)


def draft_body(change, source, detected_at):
    model = change["display_name"]
    field_label = change["field"]
    old_value = change["old_value"]
    new_value = change["new_value"]
    effective_date = change["entry"].get("deprecation_date") or change["entry"].get("retirement_date")
    effective_line = f"\nEffective date in facts.json: {effective_date}\n" if effective_date else ""
    quote = source.get("quote", "")
    url = source.get("url", "")
    accessed_at = source.get("accessed_at", "")

    headline = f"{change['provider']} quietly changed {model} {field_label}"
    return (
        "---\n"
        "status: draft\n"
        f"detected_at: {yaml_scalar(detected_at)}\n"
        f"model: {yaml_scalar(change['model_id'])}\n"
        f"field: {yaml_scalar(field_label)}\n"
        f"old_value: {yaml_scalar(old_value)}\n"
        f"new_value: {yaml_scalar(new_value)}\n"
        "---\n\n"
        f"{DRAFT_STAMP}\n\n"
        f"# {headline}\n\n"
        f"{model} changed `{field_label}` from `{old_value}` to `{new_value}`."
        f"{effective_line}\n"
        "Primary-source quote from facts.json:\n\n"
        f"> {quote}\n\n"
        f"Source URL: {url}\n\n"
        f"Accessed at: {accessed_at}\n\n"
        "## Claude review checklist\n\n"
        "- Re-verify quote against live source.\n"
        "- Confirm effective date.\n"
        "- Check whether external datasets still carry the old value.\n"
    )


def write_summary(summary_path, detected_at, changes, emitted, needs_resourcing, changelog):
    latest = {}
    releases = changelog.get("releases", []) if isinstance(changelog, dict) else []
    if releases:
        latest = releases[0]

    lines = [
        f"# Story flywheel summary - {detected_at}",
        "",
        f"Latest changelog release: {latest.get('date', 'unknown')} {latest.get('version', '')}".rstrip(),
        f"Real value changes: {len(changes)}",
        "",
    ]
    if not changes:
        lines.append("No story opportunities this cycle (0 real value changes)")
    else:
        lines.append("## Drafts emitted")
        lines.append("")
        if emitted:
            lines.extend(f"- {slug}" for slug in emitted)
        else:
            lines.append("- None")
        lines.append("")
        lines.append("## Needs re-sourcing")
        lines.append("")
        if needs_resourcing:
            for item in needs_resourcing:
                lines.append(
                    f"- {item['provider']}/{item['model_id']} {item['field']}: "
                    f"new value {item['new_value']!r} not found in a matching facts.json source quote"
                )
        else:
            lines.append("- None")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def detect(args):
    current_path = Path(args.current)
    previous_path = Path(args.previous) if args.previous else latest_archive_path(Path(args.archive_dir))
    changelog_path = Path(args.changelog)
    draft_dir = Path(args.draft_dir)
    summary_dir = Path(args.summary_dir)
    detected_at = args.date

    previous_facts = load_json(previous_path)
    current_facts = load_json(current_path)
    changelog = load_json(changelog_path)
    changes = real_changes(previous_facts, current_facts)

    emitted = []
    needs_resourcing = []
    for change in changes:
        source = source_for_change(change["entry"], change["field"], change["new_value"])
        if not source:
            needs_resourcing.append(change)
            continue
        slug = slugify(f"{change['provider']}-{change['model_id']}-{change['field']}-{detected_at}")
        path = draft_dir / f"story-{slug}.md"
        draft_dir.mkdir(parents=True, exist_ok=True)
        path.write_text(draft_body(change, source, detected_at), encoding="utf-8")
        emitted.append(path.name)

    summary_path = summary_dir / f"summary-{detected_at}.md"
    write_summary(summary_path, detected_at, changes, emitted, needs_resourcing, changelog)

    print(f"Previous facts: {previous_path}")
    print(f"Current facts: {current_path}")
    print(f"Real value changes: {len(changes)}")
    print(f"Drafts emitted: {len(emitted)}")
    for slug in emitted:
        print(f"- {slug}")
    print(f"Needs re-sourcing: {len(needs_resourcing)}")
    for item in needs_resourcing:
        print(f"- {item['provider']}/{item['model_id']} {item['field']}")
    print(f"Summary: {summary_path}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Detect draft story opportunities from facts diffs.")
    parser.add_argument("--current", default=str(DEFAULT_CURRENT), help="Current facts.json path")
    parser.add_argument("--previous", help="Previous facts archive path; defaults to latest data/archive/facts-<date>.json")
    parser.add_argument("--archive-dir", default=str(DEFAULT_ARCHIVE_DIR), help="Archive directory for default previous lookup")
    parser.add_argument("--changelog", default=str(DEFAULT_CHANGELOG), help="Changelog JSON path")
    parser.add_argument("--draft-dir", default=str(DEFAULT_DRAFT_DIR), help="Draft output directory")
    parser.add_argument("--summary-dir", default=str(DEFAULT_SUMMARY_DIR), help="Summary output directory")
    parser.add_argument("--date", default=date.today().isoformat(), help="Detection date for output filenames")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return detect(args)


if __name__ == "__main__":
    sys.exit(main())
