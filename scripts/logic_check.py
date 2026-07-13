#!/usr/bin/env python3
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACTS_PATH = ROOT / "data" / "facts.json"
CHANGELOG_PATH = ROOT / "data" / "changelog.json"
BASELINE_PATH = ROOT / "ops" / "logic-baseline.json"

NUMERIC_FIELDS = (
    "pricing.input_per_mtok",
    "pricing.output_per_mtok",
    "pricing.cached_input_per_mtok",
    "pricing.batch_discount_pct",
    "context_window_tokens",
    "max_output_tokens",
)
ENUM_FIELDS = ("status", "modalities")
REPORT_CLASS_ORDER = (
    "CRITICAL",
    "UNSUPPORTED",
    "AMBIGUOUS",
    "RULE-1",
    "RULE-2",
    "RULE-3",
    "RULE-4",
    "RULE-5",
    "RULE-6",
    "RULE-7",
    "RULE-8",
)
WARNING_CLASSES = {"UNSUPPORTED", "AMBIGUOUS"} | {f"RULE-{index}" for index in range(1, 9)}
ACTIVE_STATUSES = {"ga", "preview"}
INACTIVE_LANGUAGE_RE = re.compile(
    r"\b(deprecated|deprecation|retired|retirement|legacy|eol|end[- ]of[- ]life|sunset)\b",
    re.IGNORECASE,
)
MODEL_PREFIXES = (
    "openai",
    "accounts",
    "fireworks",
    "models",
)
TIER_NOTE_TERMS = (
    "tier",
    "standard",
    "short-context",
    "long-context",
    "prompt",
    "international",
    "global",
    "regional",
    "public extended",
    "base",
    "<=",
    ">",
)


@dataclass(frozen=True)
class Finding:
    entry: str
    field: str
    class_name: str
    detail: str


@dataclass(frozen=True)
class NumericCandidate:
    raw: str
    values: tuple[Decimal, ...]
    ambiguous: bool
    detail: str


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def entry_key(entry):
    return f"{entry.get('provider')}/{entry.get('model_id')}"


def get_field(entry, field):
    if field.startswith("pricing."):
        return entry.get("pricing", {}).get(field.split(".", 1)[1])
    return entry.get(field)


def decimal_from_text(value):
    try:
        return Decimal(str(value).replace(",", ""))
    except (InvalidOperation, ValueError):
        return None


def decimal_equal(left, right):
    left_dec = decimal_from_text(left)
    right_dec = decimal_from_text(right)
    if left_dec is None or right_dec is None:
        return False
    return abs(left_dec - right_dec) <= Decimal("0.000000001")


def money_unit_multiplier(window):
    lowered = window.lower()
    if re.search(r"(per[- ]?token|/ ?token|cost_per_token)", lowered):
        return Decimal("1000000")
    if re.search(r"(per ?1?k|/ ?1?k|per ?1,000|/ ?1,000|ktok)", lowered):
        return Decimal("1000")
    return Decimal("1")


PRICE_CUE_RE = re.compile(
    r"(\$|/?\$?/?1m\b|/?\$?/?1k\b|per ?1m\b|per ?1k\b|input|output|cache|price|pricing|token)",
    re.IGNORECASE,
)
BARE_PRICE_NUMBER_RE = re.compile(r"(?<![\w$])([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)(?![\w])")
PRICE_TABLE_HEADER_RE = re.compile(
    r"input\s*\([^)]*1m[^)]*\)\s*output\s*\([^)]*1m[^)]*\)\s*cache",
    re.IGNORECASE,
)


def bare_price_table_field(quote, number_start):
    header_matches = list(PRICE_TABLE_HEADER_RE.finditer(quote[:number_start]))
    if not header_matches:
        return None

    row_prefix = quote[header_matches[-1].end():number_start]
    column_index = len(list(BARE_PRICE_NUMBER_RE.finditer(row_prefix)))
    fields = (
        "pricing.input_per_mtok",
        "pricing.output_per_mtok",
        "pricing.cached_input_per_mtok",
    )
    if column_index < len(fields):
        return fields[column_index]
    return None


def price_candidates(quote, expected_value=None, field=None):
    candidates = []
    for match in re.finditer(r"\$\s*([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)", quote):
        start, end = match.span()
        window = quote[max(0, start - 60): min(len(quote), end + 60)]
        unit_tail = quote[end: min(len(quote), end + 20)]
        if re.match(r"\s*(/ ?min|per minute|per min)", unit_tail, re.IGNORECASE):
            continue
        value = decimal_from_text(match.group(1))
        if value is None:
            continue
        multiplier = money_unit_multiplier(window)
        candidates.append(
            NumericCandidate(
                raw=match.group(0),
                values=(value * multiplier,),
                ambiguous=False,
                detail=f"{match.group(0)} as {value * multiplier} per 1M tokens",
            )
        )
    if expected_value is None:
        return candidates

    for match in BARE_PRICE_NUMBER_RE.finditer(quote):
        start, end = match.span()
        raw = quote[start:end]
        if start > 0 and quote[start - 1] == "$":
            continue
        value = decimal_from_text(match.group(1))
        if value is None or not decimal_equal(expected_value, value):
            continue
        table_field = bare_price_table_field(quote, start)
        if table_field is not None and field != table_field:
            continue
        window = quote[max(0, start - 40): min(len(quote), end + 40)]
        if not PRICE_CUE_RE.search(window):
            continue
        candidates.append(
            NumericCandidate(
                raw=raw,
                values=(value,),
                ambiguous=False,
                detail=f"{raw} as exact bare price per 1M tokens",
            )
        )
    return candidates


def percent_candidates(quote):
    candidates = []
    for match in re.finditer(r"([0-9]+(?:\.[0-9]+)?)\s*%", quote):
        value = decimal_from_text(match.group(1))
        if value is None:
            continue
        candidates.append(
            NumericCandidate(
                raw=match.group(0),
                values=(value,),
                ambiguous=False,
                detail=f"{match.group(0)} as {value} percent",
            )
        )
    return candidates


def scaled_token_candidate(raw, number, suffix, word):
    value = decimal_from_text(number)
    if value is None:
        return None

    suffix = (suffix or "").lower()
    word = (word or "").lower()
    if suffix == "k":
        decimal_value = value * Decimal("1000")
        binary_value = value * Decimal("1024")
        return NumericCandidate(
            raw=raw,
            values=(decimal_value, binary_value),
            ambiguous=True,
            detail=f"{raw} can mean decimal {decimal_value} or binary {binary_value} tokens",
        )
    if suffix == "m":
        decimal_value = value * Decimal("1000000")
        binary_value = value * Decimal("1048576")
        return NumericCandidate(
            raw=raw,
            values=(decimal_value, binary_value),
            ambiguous=True,
            detail=f"{raw} can mean decimal {decimal_value} or binary {binary_value} tokens",
        )
    if word == "thousand":
        return NumericCandidate(raw=raw, values=(value * Decimal("1000"),), ambiguous=False, detail=f"{raw} as decimal tokens")
    if word == "million":
        return NumericCandidate(raw=raw, values=(value * Decimal("1000000"),), ambiguous=False, detail=f"{raw} as decimal tokens")
    if word == "billion":
        return NumericCandidate(raw=raw, values=(value * Decimal("1000000000"),), ambiguous=False, detail=f"{raw} as decimal tokens")

    return NumericCandidate(raw=raw, values=(value,), ambiguous=False, detail=f"{raw} tokens")


def token_candidates(quote):
    candidates = []
    pattern = re.compile(
        r"(?<![\w$])([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)\s*(?:([kKmM])\b|(thousand|million|billion)\b)?"
    )
    for match in pattern.finditer(quote):
        number, suffix, word = match.groups()
        start, end = match.span()
        raw = quote[start:end].strip()
        window = quote[max(0, start - 45): min(len(quote), end + 45)]
        if start > 0 and quote[start - 1] == "$":
            continue
        # Date filtering should remove the date component itself, not nearby token
        # ranges such as "128K<Token<=256K ... qwen-2026-01-23".
        window_start = max(0, start - 45)
        inside_date = False
        for date_match in re.finditer(r"\b20[0-9]{2}[-/][0-9]{2}[-/][0-9]{2}\b", window):
            date_start = window_start + date_match.start()
            date_end = window_start + date_match.end()
            if start >= date_start and end <= date_end:
                inside_date = True
                break
        if inside_date:
            continue
        if "." in number and not (suffix or word):
            continue
        if not (suffix or word or "," in number or re.search(r"(token|context|output|input|window|length)", window, re.IGNORECASE)):
            continue
        candidate = scaled_token_candidate(raw, number, suffix, word)
        if candidate is not None:
            candidates.append(candidate)
    return candidates


def numeric_candidates_for_field(quote, field, expected_value=None):
    if field == "pricing.batch_discount_pct":
        return percent_candidates(quote)
    if field.startswith("pricing."):
        return price_candidates(quote, expected_value=expected_value, field=field)
    return token_candidates(quote)


def exact_candidate_matches(value, candidates):
    matches = []
    for candidate in candidates:
        if any(decimal_equal(value, candidate_value) for candidate_value in candidate.values):
            matches.append(candidate)
    return matches


def source_quotes(entry, field=None):
    sources = entry.get("sources", [])
    if field is None:
        return [source.get("quote", "") for source in sources]
    field_sources = [source.get("quote", "") for source in sources if field in source.get("fields", [])]
    return field_sources or [source.get("quote", "") for source in sources]


def labeled_numeric_candidates(quote, field):
    lowered = quote.lower()
    labels = {
        "pricing.input_per_mtok": ("input price", "input"),
        "pricing.output_per_mtok": ("output price", "output"),
        "pricing.cached_input_per_mtok": ("cached input", "context caching", "cache read"),
        "pricing.batch_discount_pct": ("batch", "discount"),
        "context_window_tokens": ("context window", "context length", "context"),
        "max_output_tokens": ("max output tokens", "max output", "maximum output"),
    }.get(field, ())
    if not labels:
        return []

    candidates = []
    for label in labels:
        start = 0
        while True:
            index = lowered.find(label, start)
            if index == -1:
                break
            snippet = quote[index: min(len(quote), index + 220)]
            candidates.extend(numeric_candidates_for_field(snippet, field))
            start = index + len(label)
    return candidates


def tiered_pricing_without_note(entry, field):
    value = get_field(entry, field)
    if not field.startswith("pricing.") or value is None:
        return None
    notes = (entry.get("notes") or "").lower()
    if any(term in notes for term in TIER_NOTE_TERMS):
        return None

    tier_markers = re.compile(
        r"(<=|>=|<|>|\btier\b|first\s+[0-9][0-9,]*(?:\.\d+)?|after\s+[0-9][0-9,]*(?:\.\d+)?|above\s+[0-9][0-9,]*(?:\.\d+)?|over\s+[0-9][0-9,]*(?:\.\d+)?|under\s+[0-9][0-9,]*(?:\.\d+)?|long[- ]context|context size|search context|volume|threshold|duration|resolution|regional|global|international)",
        re.IGNORECASE,
    )
    for source in entry.get("sources", []):
        if field not in source.get("fields", []):
            continue
        quote = source.get("quote", "")
        for clause in re.split(r"(?:\r?\n|---+|[;|])", quote):
            if not tier_markers.search(clause):
                continue
            candidates = numeric_candidates_for_field(clause, field, expected_value=value)
            if not exact_candidate_matches(value, candidates):
                continue
            distinct = {str(candidate.values[0]) for candidate in candidates if candidate.values}
            if len(distinct) > 1:
                return f"tiered pricing quote has multiple values ({', '.join(sorted(distinct)[:6])}) but notes do not document the chosen tier"
    return None


def audit_numeric_field(entry, field):
    value = get_field(entry, field)
    if value is None:
        return []

    all_candidates = []
    for quote in source_quotes(entry):
        all_candidates.extend(numeric_candidates_for_field(quote, field, expected_value=value))
    matches = exact_candidate_matches(value, all_candidates)
    if any(not match.ambiguous for match in matches):
        tier_detail = tiered_pricing_without_note(entry, field)
        if tier_detail:
            return [Finding(entry_key(entry), field, "UNSUPPORTED", tier_detail)]
        return []
    if matches:
        details = "; ".join(match.detail for match in matches[:3])
        return [Finding(entry_key(entry), field, "AMBIGUOUS", f"stored value {value} only matches ambiguous quote unit(s): {details}")]

    field_source_candidates = []
    field_labeled_candidates = []
    for quote in source_quotes(entry, field):
        field_source_candidates.extend(numeric_candidates_for_field(quote, field, expected_value=value))
        field_labeled_candidates.extend(labeled_numeric_candidates(quote, field))
    if field_labeled_candidates:
        seen = sorted({candidate.raw for candidate in field_labeled_candidates})
        return [
            Finding(
                entry_key(entry),
                field,
                "CRITICAL",
                f"field-labeled quote value(s) {', '.join(seen[:8])} do not match stored value {value}",
            )
        ]
    if field_source_candidates:
        seen = sorted({candidate.raw for candidate in field_source_candidates})
        return [
            Finding(
                entry_key(entry),
                field,
                "CRITICAL",
                f"source assigned to field has numeric value(s) {', '.join(seen[:8])} but none match stored value {value}",
            )
        ]
    return [Finding(entry_key(entry), field, "UNSUPPORTED", f"no stored quote contains numeric evidence for stored value {value}")]


def status_quote_statuses(quote):
    lowered = quote.lower()
    statuses = set()
    if re.search(r"\b(preview|beta|experimental)\b", lowered):
        statuses.add("preview")
    if re.search(r"\b(ga|generally available|live)\b", lowered):
        statuses.add("ga")
    if re.search(r"\b(deprecated|deprecation|legacy)\b", lowered):
        statuses.add("deprecated")
    if re.search(r"\b(retired|retirement|eol|end[- ]of[- ]life|sunset)\b", lowered):
        statuses.add("retired")
    return statuses


def status_aliases(entry):
    aliases = {
        str(entry.get("model_id") or ""),
        str(entry.get("display_name") or ""),
    }
    display = str(entry.get("display_name") or "")
    compact_display = display.replace(" ", "-")
    aliases.add(compact_display)
    aliases.add(compact_display.lower())
    for alias in list(aliases):
        aliases.add(alias.replace("-", " "))
        aliases.add(alias.replace(".", " "))
    return tuple(sorted({alias for alias in aliases if alias}, key=len, reverse=True))


def scoped_status_quote_statuses(entry, quote):
    statuses = set()
    alias_blob = " ".join(status_aliases(entry))
    statuses.update(status_quote_statuses(alias_blob))

    for alias in status_aliases(entry):
        pattern = re.compile(rf"(?<![A-Za-z0-9._-]){re.escape(alias)}(?![A-Za-z0-9._-])", re.IGNORECASE)
        for match in pattern.finditer(quote):
            start, end = match.span()
            scoped_quote = quote[max(0, start - 50): min(len(quote), end + 50)]
            if re.search(r"\b(ga|generally available|live|available|serving)\b", scoped_quote, re.IGNORECASE):
                statuses.add("ga")
            if re.search(rf"\b(legacy|deprecated|retired)\s+models?\b.{{0,60}}{re.escape(alias)}", scoped_quote, re.IGNORECASE):
                statuses.add("deprecated")
            if re.search(rf"{re.escape(alias)}.{{0,25}}\b(preview|beta|experimental)\b", scoped_quote, re.IGNORECASE):
                statuses.add("preview")
            if re.search(rf"\b(preview|beta|experimental)\b.{{0,25}}{re.escape(alias)}", scoped_quote, re.IGNORECASE):
                statuses.add("preview")
    return statuses


def audit_status(entry):
    status = entry.get("status")
    if status is None:
        return []
    quote_statuses = set()
    for quote in source_quotes(entry):
        quote_statuses.update(scoped_status_quote_statuses(entry, quote))

    if status in quote_statuses:
        return []
    if quote_statuses:
        incompatible = ", ".join(sorted(quote_statuses))
        return [Finding(entry_key(entry), "status", "CRITICAL", f"quote status language implies {incompatible}, not stored status {status}")]
    return [Finding(entry_key(entry), "status", "UNSUPPORTED", f"no stored quote entails status {status}")]


def modality_word(modality):
    if modality == "image":
        return r"(image|images|vision)"
    return re.escape(modality)


def negated_modality(quote, modality):
    pattern = modality_word(modality)
    checks = [
        rf"{pattern}.{{0,40}}\b(input|output)\b.{{0,40}}\b(not supported|unsupported)\b",
        rf"\b(input|output|support)\b.{{0,40}}{pattern}.{{0,40}}\b(not supported|unsupported)\b",
    ]
    return any(re.search(check, quote, re.IGNORECASE) for check in checks)


def has_modality_context(quote, modality, direction):
    pattern = modality_word(modality)
    lowered = quote.lower()
    if direction == "input":
        checks = [
            rf"{pattern}.{{0,40}}\binput\b",
            rf"\binput modalities\b.{{0,120}}{pattern}",
            rf"\binput\b.{{0,80}}{pattern}",
            rf"\bsupports\b.{{0,80}}{pattern}.{{0,40}}\binput\b",
        ]
    else:
        checks = [
            rf"{pattern}.{{0,40}}\boutput\b",
            rf"\boutput modalities\b.{{0,120}}{pattern}",
            rf"\boutput\b.{{0,80}}{pattern}",
        ]
    if any(re.search(check, quote, re.IGNORECASE) for check in checks):
        return True
    if modality == "text" and re.search(r"\btext-to-text\b", lowered):
        return True
    return False


def audit_modalities(entry):
    modalities = entry.get("modalities")
    if modalities is None:
        return []
    required_input = set(modalities.get("input") or [])
    required_output = set(modalities.get("output") or [])
    contradictions = []
    for quote in source_quotes(entry, "modalities"):
        for modality in sorted(required_input | required_output):
            if negated_modality(quote, modality) and modality in required_input:
                contradictions.append(f"{modality} input marked unsupported")
    if contradictions:
        return [Finding(entry_key(entry), "modalities", "CRITICAL", "; ".join(sorted(set(contradictions))))]

    for quote in source_quotes(entry, "modalities"):
        input_ok = all(has_modality_context(quote, modality, "input") or (modality == "text" and "text" in quote.lower()) for modality in required_input)
        output_ok = all(has_modality_context(quote, modality, "output") or (modality == "text" and "text" in quote.lower()) for modality in required_output)
        if input_ok and output_ok:
            return []
    return [
        Finding(
            entry_key(entry),
            "modalities",
            "UNSUPPORTED",
            f"no stored quote entails input={sorted(required_input)} and output={sorted(required_output)}",
        )
    ]


def audit_quote_entailment(facts):
    findings = []
    for entry in facts:
        for field in NUMERIC_FIELDS:
            findings.extend(audit_numeric_field(entry, field))
        findings.extend(audit_status(entry))
        findings.extend(audit_modalities(entry))
    return findings


def canonical_model_key(entry):
    value = str(entry.get("model_id", "")).lower()
    value = value.replace("qwen-3", "qwen3").replace("qwen-2", "qwen2")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    parts = [part for part in value.split("-") if part and part not in MODEL_PREFIXES]
    if parts and parts[0] == str(entry.get("provider", "")).lower():
        parts = parts[1:]
    value = "-".join(parts)
    value = re.sub(r"^(openai-)+", "", value)
    value = re.sub(r"-(fast)$", "", value)
    return value


def explanation_present(entries):
    blob = " ".join((entry.get("notes") or "") + " " + " ".join(source.get("quote", "") for source in entry.get("sources", [])) for entry in entries)
    return re.search(r"(provider-specific|serving limit|context cap|limited|caps? at|supports up to)", blob, re.IGNORECASE) is not None


def rule_same_model_context(facts):
    groups = defaultdict(list)
    for entry in facts:
        context = entry.get("context_window_tokens")
        if context is not None:
            groups[canonical_model_key(entry)].append(entry)

    findings = []
    for key, entries in groups.items():
        providers = {entry.get("provider") for entry in entries}
        contexts = {entry.get("context_window_tokens") for entry in entries}
        if len(providers) <= 1 or len(contexts) <= 1:
            continue
        if explanation_present(entries):
            continue
        detail = "; ".join(f"{entry_key(entry)}={entry.get('context_window_tokens')}" for entry in sorted(entries, key=entry_key))
        findings.append(Finding(key, "context_window_tokens", "RULE-1", f"same canonical model has divergent context windows: {detail}"))
    return findings


def rule_output_less_than_input(facts):
    findings = []
    for entry in facts:
        pricing = entry.get("pricing", {})
        input_price = pricing.get("input_per_mtok")
        output_price = pricing.get("output_per_mtok")
        if input_price is not None and output_price is not None and Decimal(str(output_price)) < Decimal(str(input_price)):
            findings.append(
                Finding(
                    entry_key(entry),
                    "pricing.output_per_mtok",
                    "RULE-2",
                    f"output price {output_price} is lower than input price {input_price}",
                )
            )
    return findings


def rule_context_less_than_output(facts):
    findings = []
    for entry in facts:
        context = entry.get("context_window_tokens")
        output = entry.get("max_output_tokens")
        if context is not None and output is not None and int(context) < int(output):
            findings.append(
                Finding(
                    entry_key(entry),
                    "context_window_tokens",
                    "RULE-3",
                    f"context window {context} is lower than max output {output}",
                )
            )
    return findings


def is_exact_ratio(left, right):
    if left is None or right is None:
        return False
    left_dec = Decimal(str(left))
    right_dec = Decimal(str(right))
    if left_dec == 0 or right_dec == 0:
        return False
    ratio = left_dec / right_dec
    return ratio in {Decimal("2"), Decimal("10"), Decimal("0.5"), Decimal("0.1")}


def rule_price_ratio_slips(facts):
    groups = defaultdict(list)
    for entry in facts:
        groups[canonical_model_key(entry)].append(entry)

    findings = []
    for entries in groups.values():
        if len({entry.get("provider") for entry in entries}) <= 1:
            continue
        entries = sorted(entries, key=entry_key)
        for index, left in enumerate(entries):
            for right in entries[index + 1:]:
                if left.get("provider") == right.get("provider"):
                    continue
                for field in ("pricing.input_per_mtok", "pricing.output_per_mtok", "pricing.cached_input_per_mtok"):
                    left_value = get_field(left, field)
                    right_value = get_field(right, field)
                    if is_exact_ratio(left_value, right_value):
                        findings.append(
                            Finding(
                                f"{entry_key(left)} <> {entry_key(right)}",
                                field,
                                "RULE-4",
                                f"same canonical model prices are exact 2x/10x ratio: {left_value} vs {right_value}",
                            )
                        )
    return findings


def rule_active_with_inactive_quote(facts):
    findings = []
    for entry in facts:
        if entry.get("status") not in ACTIVE_STATUSES:
            continue
        for source_index, source in enumerate(entry.get("sources", [])):
            quote = source.get("quote", "")
            match = INACTIVE_LANGUAGE_RE.search(quote)
            if match:
                findings.append(
                    Finding(
                        entry_key(entry),
                        "status",
                        "RULE-5",
                        f"active status but source {source_index} contains inactive language: {match.group(0)}",
                    )
                )
                break
    return findings


def parse_source_date(value):
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized).date()
    except ValueError:
        return None


def rule_accessed_at_age(facts, today=None):
    today = today or datetime.now(timezone.utc).date()
    findings = []
    cutoff = today - timedelta(days=30)
    for entry in facts:
        for source_index, source in enumerate(entry.get("sources", [])):
            accessed_date = parse_source_date(source.get("accessed_at"))
            if accessed_date is None:
                continue
            if accessed_date > today:
                findings.append(
                    Finding(entry_key(entry), f"sources[{source_index}].accessed_at", "RULE-6", f"accessed_at {accessed_date} is in the future relative to {today}")
                )
            elif accessed_date < cutoff:
                findings.append(
                    Finding(entry_key(entry), f"sources[{source_index}].accessed_at", "RULE-6", f"accessed_at {accessed_date} is older than 30 days relative to {today}")
                )
    return findings


def sanitize_filename(value):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value))


def rule_duplicates_and_permalink_collisions(facts):
    findings = []
    provider_model_counts = Counter((entry.get("provider"), entry.get("model_id")) for entry in facts)
    for (provider, model_id), count in sorted(provider_model_counts.items()):
        if count > 1:
            findings.append(Finding(f"{provider}/{model_id}", "model_id", "RULE-7", f"duplicate provider/model_id appears {count} times"))

    permalinks = defaultdict(list)
    for entry in facts:
        permalink = f"/models/{sanitize_filename(entry.get('provider'))}/{sanitize_filename(entry.get('model_id'))}.html"
        permalinks[permalink].append(entry)
    for permalink, entries in sorted(permalinks.items()):
        unique_ids = {(entry.get("provider"), entry.get("model_id")) for entry in entries}
        if len(unique_ids) > 1:
            models = ", ".join(entry_key(entry) for entry in sorted(entries, key=entry_key))
            findings.append(Finding(permalink, "permalink", "RULE-7", f"sanitized permalink collision among {models}"))
    return findings


def changelog_model_keys(changelog):
    all_entries = set()
    added_entries = set()
    for release in changelog.get("releases", []):
        for entry in release.get("entries", []):
            key = (entry.get("provider"), entry.get("model_id"))
            all_entries.add(key)
            if entry.get("type") == "added":
                added_entries.add(key)
    return all_entries, added_entries


def rule_changelog_coverage(facts, changelog):
    facts_keys = {(entry.get("provider"), entry.get("model_id")) for entry in facts}
    changelog_keys, added_keys = changelog_model_keys(changelog)
    findings = []
    for provider, model_id in sorted(facts_keys - changelog_keys):
        findings.append(Finding(f"{provider}/{model_id}", "changelog", "RULE-8", "fact entry does not appear in any changelog release"))
    for provider, model_id in sorted(added_keys - facts_keys):
        findings.append(Finding(f"{provider}/{model_id}", "changelog", "RULE-8", "changelog added model is missing from facts.json"))
    return findings


def audit_rules(facts, changelog, today=None):
    findings = []
    findings.extend(rule_same_model_context(facts))
    findings.extend(rule_output_less_than_input(facts))
    findings.extend(rule_context_less_than_output(facts))
    findings.extend(rule_price_ratio_slips(facts))
    findings.extend(rule_active_with_inactive_quote(facts))
    findings.extend(rule_accessed_at_age(facts, today=today))
    findings.extend(rule_duplicates_and_permalink_collisions(facts))
    findings.extend(rule_changelog_coverage(facts, changelog))
    return findings


def audited_field_count(facts):
    count = 0
    for entry in facts:
        count += sum(1 for field in NUMERIC_FIELDS if get_field(entry, field) is not None)
        count += sum(1 for field in ENUM_FIELDS if get_field(entry, field) is not None)
    return count


def run_logic_checks(facts, changelog, today=None):
    findings = []
    findings.extend(audit_quote_entailment(facts))
    findings.extend(audit_rules(facts, changelog, today=today))
    return sorted(findings, key=lambda item: (item.class_name, item.entry, item.field, item.detail))


def markdown_escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def finding_key(finding):
    return "|".join(
        markdown_escape(part)
        for part in (finding.entry, finding.field, finding.class_name, finding.detail)
    )


def write_baseline(path, findings, today):
    accepted = [finding for finding in findings if finding.class_name in WARNING_CLASSES]
    payload = {
        "generated_at": datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
        "policy": "Findings listed here are accepted warnings. Validation fails only on logic findings with keys absent from this baseline.",
        "findings": [
            {
                "key": finding_key(finding),
                "entry": finding.entry,
                "field": finding.field,
                "class": finding.class_name,
                "detail": finding.detail,
            }
            for finding in accepted
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def judgment_for(finding):
    if finding.class_name == "CRITICAL":
        return "Re-collect from live source; stored value and cited evidence conflict."
    if finding.class_name == "AMBIGUOUS":
        return "Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention."
    if finding.class_name == "UNSUPPORTED":
        if finding.field.startswith("pricing.") and "tier" in finding.detail.lower():
            return "Documentation fix: note the selected pricing tier, or re-collect if the tier choice is uncertain."
        return "Documentation fix if the stored value is correct; otherwise re-collect the missing evidence."
    if finding.class_name in {"RULE-1", "RULE-4"}:
        return "Manual review; likely re-collect or document provider-specific serving/pricing differences."
    if finding.class_name in {"RULE-2", "RULE-3", "RULE-5"}:
        return "Re-collect from live source; this violates a high-signal sanity invariant."
    if finding.class_name == "RULE-6":
        return "Re-collect from live source if the timestamp is stale or future-dated."
    if finding.class_name in {"RULE-7", "RULE-8"}:
        return "Repository documentation/tooling fix; no live source needed unless the model list itself is wrong."
    return "Manual review."


def write_markdown_report(path, facts, findings, today):
    counts = Counter(finding.class_name for finding in findings)
    zero_rule_classes = [class_name for class_name in REPORT_CLASS_ORDER if class_name.startswith("RULE-") and counts[class_name] == 0]
    lines = [
        f"# Logic Audit - {today.isoformat()}",
        "",
        f"Audit date: {today.isoformat()}",
        f"Entries audited: {len(facts)}",
        f"Non-null Part A fields judged: {audited_field_count(facts)}",
        "Part B rules executed: RULE-1 through RULE-8",
        f"Part B rules with zero findings: {', '.join(zero_rule_classes) if zero_rule_classes else 'none'}",
        f"Findings: {len(findings)}",
        "",
        "## Counts by class",
        "",
        "| Class | Count |",
        "| --- | ---: |",
    ]
    for class_name in REPORT_CLASS_ORDER:
        lines.append(f"| {class_name} | {counts[class_name]} |")
    for class_name, count in sorted(counts.items()):
        if class_name not in REPORT_CLASS_ORDER:
            lines.append(f"| {class_name} | {count} |")

    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| Entry | Field | Class | Detail |",
            "| --- | --- | --- | --- |",
        ]
    )
    for finding in findings:
        lines.append(
            f"| {markdown_escape(finding.entry)} | {markdown_escape(finding.field)} | "
            f"{markdown_escape(finding.class_name)} | {markdown_escape(finding.detail)} |"
        )

    recollect = [finding for finding in findings if "Re-collect" in judgment_for(finding)]
    documentation = [finding for finding in findings if "Documentation fix" in judgment_for(finding) or "Repository documentation" in judgment_for(finding)]
    manual = [finding for finding in findings if finding not in recollect and finding not in documentation]
    lines.extend(
        [
            "",
            "## Judgment",
            "",
            f"- Re-collection from live sources: {len(recollect)} findings. This includes CRITICAL conflicts, stale/future timestamps, and high-signal invariant failures.",
            f"- Documentation or quote/note fixes: {len(documentation)} findings. This includes unsupported or ambiguous quote entailment where the stored value may still be correct but the stored evidence is inadequate.",
            f"- Manual review before deciding: {len(manual)} findings. This mainly covers cross-provider same-model comparisons and exact-ratio price checks.",
            "",
            "| Entry | Field | Class | Judgment |",
            "| --- | --- | --- | --- |",
        ]
    )
    for finding in findings:
        lines.append(
            f"| {markdown_escape(finding.entry)} | {markdown_escape(finding.field)} | "
            f"{markdown_escape(finding.class_name)} | {markdown_escape(judgment_for(finding))} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_findings(findings):
    for finding in findings:
        print(f"- {finding.entry} | {finding.field} | {finding.class_name} | {finding.detail}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit quote entailment and cross-entry logic invariants.")
    parser.add_argument("--facts", default=str(FACTS_PATH), help="Path to facts.json")
    parser.add_argument("--changelog", default=str(CHANGELOG_PATH), help="Path to changelog.json")
    parser.add_argument("--report", help="Optional Markdown report path")
    parser.add_argument("--write-baseline", action="store_true", help="Write accepted warning findings to ops/logic-baseline.json")
    parser.add_argument("--today", help="Override current date for timestamp checks, YYYY-MM-DD")
    args = parser.parse_args(argv)

    facts_path = Path(args.facts)
    changelog_path = Path(args.changelog)
    facts = load_json(facts_path)
    changelog = load_json(changelog_path)
    today = date.fromisoformat(args.today) if args.today else datetime.now(timezone.utc).date()

    findings = run_logic_checks(facts, changelog, today=today)
    if args.report:
        report_path = Path(args.report)
        if not report_path.is_absolute():
            report_path = ROOT / report_path
        write_markdown_report(report_path, facts, findings, today)
        print(f"Wrote {report_path.relative_to(ROOT)}")
    if args.write_baseline:
        write_baseline(BASELINE_PATH, findings, today)
        print(f"Wrote {BASELINE_PATH.relative_to(ROOT)}")

    critical_findings = [finding for finding in findings if finding.class_name == "CRITICAL"]
    warning_findings = [finding for finding in findings if finding.class_name != "CRITICAL"]
    if critical_findings:
        print(f"Logic check failed: {len(critical_findings)} critical findings, {len(warning_findings)} warnings across {len(facts)} entries and {audited_field_count(facts)} audited Part A fields.")
        print_findings(critical_findings)
        return 1

    if warning_findings:
        print(f"Logic check passed with warnings: {len(warning_findings)} accepted warning findings across {len(facts)} entries and {audited_field_count(facts)} audited Part A fields.")
        print_findings(warning_findings)
        return 0

    print(f"Logic check passed: {len(facts)} entries, {audited_field_count(facts)} audited Part A fields, all 8 invariant rules clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
