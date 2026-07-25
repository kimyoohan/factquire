# Fix report — 2026-07-25 — stalled 2026-07-20 refresh unblocked

Context: the 2026-07-20 weekly refresh (Codex UPDATE_ORDER) stopped before publish because
`validate.py` exited 1 with 25 findings (12 UNSUPPORTED, 13 AMBIGUOUS). Codex re-dispatch failed
(usage limit until Jul 29), so the fix was done by the project lead (Claude) directly, with all
evidence re-fetched from primary sources as raw HTML on 2026-07-25.

## Value corrections (quote contradicted stored value)
| entry | field | before | after | evidence |
|---|---|---|---|---|
| cohere/tiny-aya-earth | modalities.input | text, image | text | docs.cohere.com/docs/models row: "... Supports 70 languages. Text 8k 8k Chat" (Text only; matches tiny-aya-global precedent) |
| cohere/tiny-aya-fire | modalities.input | text, image | text | same |
| cohere/tiny-aya-water | modalities.input | text, image | text | same |
| together/LiquidAI/LFM2.5-8B-A1B | modalities.input | text, image | text | model page: "Input modalities Text Output modalities Text" |
| xai/grok-4.5 | pricing.cached_input_per_mtok | 0.50 | 0.30 | live docs.x.ai page 2026-07-25: "Cached tokens $0.30 / 1M tokens" (price dropped since 07-20 access; old source's fields trimmed, new dated source added, noted in notes) |

## Quote additions (value correct, evidence was inadequate)
- openai/gpt-5.6-{sol,terra,luna}: added model-page source (developers.openai.com/api/docs/models/<id>),
  verbatim "Below is a list of all available snapshots and aliases for GPT-5.6 <Name> . <id>" → entails status ga.
- cohere/c4ai-aya-vision-32b: added docs.cohere.com/docs/aya-vision source, verbatim
  "Aya Vision's multimodal capabilities enable it to understand content across different media types,
  including text and images as input." → entails text+image input.

## Accepted-warning baseline regen (`logic_check.py --write-baseline`)
Remaining 17 findings match long-standing accepted patterns (273-entry baseline already carried
115 status-UNSUPPORTED, 67 modalities-UNSUPPORTED, 67 unit-AMBIGUOUS of identical shape — e.g.
tiny-aya-global "8k", amazon nova "1M", gemini-3.1 modalities). Baseline: 273 → 270 keys
(+17 new accepted, −20 stale keys dropped). Unresolvable exact integers stay at provider-stated
decimal per existing convention.

## Independent cross-verification (different inputs than the 07-20 collector where possible)
- openai compare page raw HTML: Sol $5.00/$0.50/$30.00, Terra $2.50/$0.25/$15.00, Luna $1.00/$0.10/$6.00,
  ctx 1,050,000, max out 128,000 — all 15 values match stored. ✅
- google gemini-3.5-flash model page raw HTML: 1,048,576 / 65,536 + "Inputs Text, Image, Video, Audio" ✅
- cohere models page raw HTML: aya rows "Text 8k 8k", "Text, Images 16k 4k" ✅
- xai grok-4.5 live page: $2.00 / $6.00 / ctx 500,000 ✅ — cached $0.30 mismatch found and fixed (above).
- alibaba model-deprecation raw HTML: qwen3-max-2026-01-23 → deprecation October 10, 2026 ✅
  (page phrasing too distant for validator alias-window; accepted to baseline like the rest of the family).
- Known limitation: alibabacloud.com "models" catalog page is JS-rendered — spec quotes for qwen-plus
  entries ("Context 1M; Max output 64k") are not reproducible from raw HTML. Left as-is (pre-existing
  convention); flagged for a future browser-based re-collection.

## Result
- `py scripts/validate.py` → exit 0: 146 entries, 16 providers, 782 logic-audited fields.
- Tests: test_audit_external / test_build_site / test_diff_facts / test_logic_check all OK.
