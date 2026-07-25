# FIX_ORDER — 2026-07-25 — validate.py must pass before the stalled 2026-07-20 refresh can ship

## Situation
The 2026-07-20 weekly refresh (UPDATE_ORDER run) added 11 models (135→146) but stopped before
publishing: `py scripts/validate.py` exits 1 with **25 failures** (12 UNSUPPORTED + 13 AMBIGUOUS).
The working tree still holds the uncommitted refresh. Nothing has been pushed since 2026-07-13.

## Exact reproduction
```
cd /this/directory
py scripts/validate.py   # exit code 1
```
Full failure list (verbatim from 2026-07-25 run):

### A. UNSUPPORTED — stored value has no entailing quote (12)
- alibaba/qwen3-max-2026-01-23: status deprecated
- alibaba/qwen3.7-max-2026-06-08: status ga
- alibaba/qwen3.7-max-2026-06-08: modalities input=[image,text] output=[text]
- cohere/c4ai-aya-vision-32b: modalities input=[image,text] output=[text]
- cohere/tiny-aya-earth: modalities input=[image,text] output=[text]
- cohere/tiny-aya-fire: modalities input=[image,text] output=[text]
- cohere/tiny-aya-water: modalities input=[image,text] output=[text]
- google/gemini-3.5-flash: modalities input=[audio,image,text,video] output=[text]
- openai/gpt-5.6-luna: status ga
- openai/gpt-5.6-sol: status ga
- openai/gpt-5.6-terra: status ga
- together/LiquidAI/LFM2.5-8B-A1B: modalities input=[image,text] output=[text]

### B. AMBIGUOUS — quote says "8k/16k/128K/1M", stored value picked one expansion without evidence (13)
- alibaba/qwen3.6-plus, qwen3.6-plus-2026-04-02, qwen3.7-plus, qwen3.7-plus-2026-05-26: context_window_tokens 1000000 (quote only says "1M")
- cohere/c4ai-aya-vision-32b: context 16000 ("16k"), max_output 4000 ("4k")
- cohere/tiny-aya-earth / tiny-aya-fire / tiny-aya-water: context 8000 and max_output 8000 ("8k")
- together/LiquidAI/LFM2.5-8B-A1B: context 128000 ("128K")

## Required fix (follow README Sourcing Policy strictly)
1. For every failure above, re-fetch the PRIMARY source (official provider docs/pricing/model pages,
   raw HTML or official API like /v1/models where documented) and either:
   a. add/extend a `sources[]` entry whose verbatim `quote` explicitly entails the stored value
      (for AMBIGUOUS: find the exact integer — e.g. provider API metadata, tables listing 8192 vs 8000;
       for status ga/deprecated: quote the page text that states availability/deprecation), or
   b. if no primary source confirms it, set the field to `null` (or drop the model if status itself is
      unverifiable) and record the gap in `gaps.md`, per policy.
2. Do NOT invent quotes. Do NOT change a value unless the new quote says so.
3. Re-run `py scripts/validate.py` until exit 0.
4. Update `data/changelog.json` v0.8 entry if any values changed in step 1b.
5. Do NOT commit, do NOT push, do NOT run publish.py — the human lead reviews first.
6. Write a short report of what was fixed per model to `ops/reports/fix-validate-2026-07-25.md`.

## Definition of done
- `py scripts/validate.py` exits 0 on this working tree.
- Every touched field has a verbatim primary-source quote or is null + listed in gaps.md.
- `ops/reports/fix-validate-2026-07-25.md` exists and lists per-model resolution (quote-added / value-corrected / nulled).
- No commits made; working tree left for review.
