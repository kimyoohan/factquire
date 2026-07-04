# LOGIC_AUDIT_ORDER — deep internal consistency audit of the entire dataset

You are running with maximum reasoning. The goal is not to re-fetch web pages — it is to
find LOGICAL flaws inside what we already have. Treat data/facts.json (135 entries) as a
set of claims + evidence, and attack it like a skeptical auditor.

## Part A: Quote-entailment audit (the core)
For EVERY entry and EVERY non-null numeric/enum field (pricing.*, context_window_tokens,
max_output_tokens, status, modalities), answer: **does at least one of the entry's stored
verbatim quotes actually entail this exact value?**

Rules:
- A quote entails a value only if the number appears in the quote (allowing documented
  unit conversions: $/1M vs $/1K vs per-token; K/M suffixes: 128k=128000 or 131072 —
  flag which convention the quote uses; "1M"=1000000 or 1048576 — flag ambiguity).
- Quote says a DIFFERENT number → CRITICAL.
- Value present but NO quote contains it (after conversions) → UNSUPPORTED.
- Quote ambiguous between two readings (e.g. "128K" could be 128000 or 131072 and we
  stored one of them) → AMBIGUOUS, list both readings.
- Tiered pricing: if quotes show multiple tiers and we stored one number, check the note
  field documents WHICH tier; undocumented tier choice → UNSUPPORTED.

## Part B: Cross-entry logic rules
Check the whole dataset against sanity invariants and list every violation with severity:
1. Same underlying model on multiple providers (e.g. gpt-oss-120b on groq/fireworks/
   together): context_window_tokens SHOULD usually match; differences must be explainable
   (provider-specific serving limits) — flag unexplained divergence.
2. output price < input price is rare — flag occurrences for manual review.
3. context_window_tokens < max_output_tokens is almost always wrong — flag.
4. Prices that are exact 2x/10x of another provider's same model — possible unit slip.
5. status="active" but source quote contains deprecated/retired/legacy language — flag.
6. accessed_at timestamps in the future or older than 30 days — flag.
7. Duplicate model_id within a provider; permalink collisions after filename
   sanitization (dots→underscores could collide two distinct IDs) — flag.
8. changelog.json vs facts.json: every model in facts appears in some changelog release;
   changelog "added" models that are missing from facts — flag.

## Part C: Permanent tooling
Write `scripts/logic_check.py` implementing everything from Part A+B that is mechanically
checkable (quote number-matching with unit conversion, all Part B rules). It must:
- exit 0 with summary when clean, exit 1 listing violations when not
- be runnable standalone: `py scripts/logic_check.py`
- get wired into `scripts/validate.py` (call it or merge its checks) so every future
  weekly refresh runs it automatically
Add tests in tests/test_logic_check.py (unit conversion cases, one synthetic violation
per rule proving detection works).

## Part D: Report
Write ops/reports/logic-audit-2026-07-04.md:
- table of ALL findings: entry | field | class (CRITICAL/UNSUPPORTED/AMBIGUOUS/RULE-N) | detail
- counts by class
- your judgment: which findings need re-collection from live sources vs which are
  documentation fixes (note/quote improvements)
DO NOT edit data/facts.json yourself — findings only. The reviewer decides fixes.
Commit everything on main (message "Logic audit: quote-entailment + invariant tooling").
DO NOT PUSH.

## Definition of done
- Every entry × field judged in Part A (no sampling — full sweep)
- All 8 Part B rules executed dataset-wide
- scripts/logic_check.py + tests pass; validate.py wired
- Report written, committed, not pushed
