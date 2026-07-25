# COMPARE_ORDER — bulk dataset comparison for upstream outreach (Codex step 1 only)

Today is 2026-07-13.

## Task
Compare THIS repo's `data/facts.json` (verified model records, each with pricing,
context_window_tokens, max_output_tokens, and source quotes) against external community
model-metadata datasets, and produce a candidates file of discrepancies. DO NOT contact
anyone, DO NOT open any PR/issue, DO NOT edit any external repo. Only produce the file.

## Datasets to fetch FRESH (they may have changed since last week)
(a) LiteLLM:   https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json
(b) models.dev: https://models.dev/api.json

## What counts as a candidate
For every model that overlaps between our facts.json and a dataset, where a numeric field
(input price per 1M, output price per 1M, cache read/write price, context window, max output)
DIFFERS by more than rounding:
  - Record: {repo, dataset, model_key_theirs, model_key_ours, field, theirs, ours,
             our_source_url, our_quote, our_verified_at}
  - Only include fields where we have a stored source quote containing our number
    (no quote -> skip; we can't defend it).
  - Skip cross-provider models.dev aliases (do not compare one host's price against a
    different host's price). Match same-provider entries only.

## EXCLUDE (already contacted / still open — do not re-list)
Read ops/outreach/candidates-2026-07-04.json AND ops/outreach/candidates-2026-07-05.json
and skip any (repo, model_key, field) triple already present in either. In particular:
- BerriAI/litellm: ALL fields already listed in either candidates file, plus issue #32111 /
  PR #32113 topics (Gemini TTS pricing, Groq max_output/context, DeepSeek V4 Pro host pricing).
  litellm has open contacts and is HELD this week regardless -- still list new litellm diffs
  for the record, but flag repo_status:"HELD_open_contact".
- anomalyco/models.dev: mistral-medium pricing (issue #3025, CLOSED-completed).
- Helicone/helicone: claude-3.5-sonnet-v2 bedrock pricing (PR #5709, open) -- HELD.

## Output
Write ops/outreach/candidates-2026-07-13.json — a JSON array of candidate objects
(add a "repo_status" field to each: "eligible" or "HELD_open_contact").
If there are zero NEW discrepancies, write an empty array []. Zero is a valid, successful
result — do not invent differences to fill the file. Also write a one-paragraph summary at
ops/outreach/candidates-2026-07-13-summary.md (how many models compared, how many raw diffs,
how many survived the has-quote filter, how many excluded as already-contacted, how many
eligible vs held).

## Definition of done
- ops/outreach/candidates-2026-07-13.json exists (array, possibly empty)
- ops/outreach/candidates-2026-07-13-summary.md exists
- No external repo was contacted or modified
