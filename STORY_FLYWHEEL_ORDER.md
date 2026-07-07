# STORY_FLYWHEEL_ORDER — auto-detect story/PR opportunities from the pipeline (Codex builds the tool)

Today is 2026-07-07. Model reasoning: medium. Build a script, NOT published content.

## Why
FactQuire already runs a machine that catches quiet changes (weekly refresh diff) and
external-dataset errors (COMPARE). Today that output sits idle in a changelog + a queue.
We want it to auto-surface, each cycle, the "we caught a quiet change" story opportunities
and the "an external dataset is now stale" PR opportunities — with the verified facts
pre-filled — into a REVIEW queue. This is the compounding growth engine (each catch becomes
a citation asset), but it must never auto-publish.

## HARD INTEGRITY RULE (non-negotiable)
The script produces DRAFTS ONLY, written to a drafts/queue folder, every draft stamped
`STATUS: DRAFT — unverified by Claude; do not publish`. It must pull every number, date,
URL, and quote from existing repo data (facts.json / archive / changelog). It must NOT
invent facts, must NOT write to content/articles/ (the live folder), and must NOT touch
site/. Zero changes this cycle -> zero drafts (never manufacture a story to fill the file).

## Build: scripts/detect_stories.py
Inputs it reads (do not re-fetch the web; work from repo data):
- data/facts.json (current) and the most recent data/archive/facts-<date>.json (previous cycle)
- data/changelog.json (latest release entries)

Behavior:
1. Compute real value changes between the previous archive and current facts.json, IGNORING
   verified_at / accessed_at / sources (timestamp-only diffs are NOT stories). A change =
   a differing pricing.*, context_window_tokens, max_output_tokens, status, or a
   deprecation/retirement date.
2. For each real change, emit a story scaffold to `content/drafts/story-<slug>-<date>.md`:
   - front-matter: status: draft, detected_at, model, field, old_value, new_value
   - a headline in the "provider quietly changed X" style (factual, not clickbait)
   - a body that states: old value -> new value, the effective date if present, and the
     VERBATIM primary-source quote + source URL + accessed_at pulled from the model's
     sources[] in facts.json. If facts.json has no quote containing the new value, DO NOT
     write a confident draft — instead flag it in the summary as "needs re-sourcing".
   - a trailing `## Claude review checklist` (re-verify quote against live source; confirm
     effective date; check whether external datasets still carry the old value).
3. Write `ops/stories/summary-<date>.md`: count of real changes, list of story slugs
   emitted, and any "needs re-sourcing" flags. If zero real changes, write the summary with
   "No story opportunities this cycle (0 real value changes)" and emit no draft files.

## PASS CRITERIA (test both directions)
A. **Zero-hallucination on clean input.** Run against the CURRENT repo (this cycle had 0
   real value changes). Expected: 0 draft files created, summary says "No story
   opportunities this cycle". Prove with the command output + a directory listing.
B. **Correct detection on a known change.** Build a temp copy of the previous archive with
   ONE value changed to a known-old value so that current-vs-temp shows exactly one diff
   (e.g. set some model's pricing.input_per_mtok in the TEMP archive to an old value, so the
   "current" looks like the new value). Run the script pointed at the temp archive. Expected:
   exactly 1 draft, whose old_value/new_value match the injected change and whose body quotes
   the REAL source URL+quote from facts.json for that model. Do NOT mutate the real archive
   or facts.json. Save command outputs to ops/reports/story-flywheel-2026-07-07.md.
C. **No live-content contamination.** After both tests, `git status` shows nothing added
   under content/articles/ or site/; drafts only under content/drafts/ and ops/stories/.

## Definition of done
- scripts/detect_stories.py built; both pass criteria A and B demonstrably met with saved
  command output in ops/reports/story-flywheel-2026-07-07.md.
- data/facts.json and data/archive/* UNCHANGED. No external repo touched. No web fetches.
