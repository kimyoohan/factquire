# CONTENT_AMMO_ORDER — high-intent query research + content-gap map (Codex researches; Claude decides)

Today is 2026-07-07. Model reasoning: medium. You (Codex) have web access. This is RESEARCH,
not publishing. Produce one analysis file. Do not write articles, do not touch site/ or
data/facts.json, do not contact anyone.

## Goal
FactQuire's growth lever is being CITED (by developers and AI answer engines) for LLM-API
facts. To aim our content, we need: which real, high-intent questions developers ask about
LLM API pricing / limits / deprecations, where the current answers are weak or stale, and
which of those we already cover vs. gaps.

## CALIBRATION (read carefully — inventing data is worse than saying "unknown")
- We have NO keyword-volume tool. DO NOT fabricate search volumes or invent precise numbers.
  Rank qualitatively (high / medium / low intent) with a one-line REASON grounded in
  something you actually observed (a real forum thread, a StackOverflow question, a docs gap,
  a SERP you fetched). No evidence -> mark "unverified".
- "Few good opportunities found" is an acceptable, useful result. Do not pad the list.
- Distinguish INTENT from VOLUME. A rarely-asked but high-stakes question (e.g. "did provider
  X raise prices") can be worth more than a common vague one.

## Research tasks
1. **Query landscape.** Gather real questions developers ask about LLM API pricing, context
   windows, max output tokens, rate limits, deprecations, and quiet price/limit changes.
   Sources to actually check: StackOverflow, GitHub issues/discussions in LLM tooling repos
   (litellm, models.dev, langchain, etc.), provider community forums, HN/Reddit threads you
   can reach. For each recurring question theme, record: the theme, an example real thread
   URL, intent level + reason, and whether the answers there are stale/scattered/missing.
2. **Competitive SERP check.** For ~10 concrete high-intent queries (e.g. "<model> pricing",
   "<model> max output tokens", "bedrock price change", "<model> deprecated"), fetch the
   query in a search engine if reachable and note what currently ranks (official docs,
   models.dev, random blogs, nothing authoritative). Flag queries where no fresh,
   primary-sourced answer dominates = our opening.
3. **Gap map vs our coverage.** We publish per-model pages at /models/<provider>/<id>.html
   (135 models) + a few articles. For each high-value query theme, mark: COVERED (we have a
   strong page), WEAK (page exists but thin/not targeted), or MISSING.

## Also fold in existing ammunition
We already verified 5 stale values in LiteLLM's dataset (see
ops/outreach/queue/litellm-groq-deepseek-2026-07-07.md: 3 Groq max_output + 2 DeepSeek V4
Pro input prices). Note in your output whether any of these map to a high-intent query theme
(i.e., would a "facts rot" article about them capture real search/citation demand).

## Output: ops/reports/content-ammo-2026-07-07.md
- Table: query theme | intent (H/M/L) + reason + evidence URL | current best answer (who
  ranks / stale?) | our coverage (COVERED/WEAK/MISSING)
- A short ranked shortlist: the top 5 content actions (write article X / strengthen page Y),
  each justified by the research above, most-defensible first.
- An "unknown / could not verify" section listing anything you couldn't ground.

## Definition of done
- ops/reports/content-ammo-2026-07-07.md exists with the table, ranked shortlist, and the
  unknown section. No fabricated volumes. No files changed outside that report.
