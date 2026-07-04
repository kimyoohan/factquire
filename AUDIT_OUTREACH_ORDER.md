# AUDIT_OUTREACH_ORDER — weekly upstream-contribution outreach (executed by Claude)

Standing approval: user approved 2026-07-04 — up to 3 sends/week (1 per repo) of
verified-error issues/PRs to external repos, no per-send approval needed. PRs (fix
included) are preferred over issues. HN or anything needing a non-GitHub login stays
in the user action queue.

## Why this exists
Every verified correction we contribute upstream is (a) proof of our product quality,
(b) a permanent backlink/citation for AI answer engines, (c) maintainer trust.
One WRONG report destroys all three — verification is the whole game.

## Protocol

### 1. Collect candidates (delegate to Codex)
Run:
```
codex exec --sandbox danger-full-access -c model_reasoning_effort="medium" \
  "Compare data/facts.json in this directory against external model-metadata datasets: \
   (a) https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json \
   (b) https://models.dev/api.json \
   For every overlapping model where pricing or context values differ, write a candidate to \
   ops/outreach/candidates-<today>.json: {repo, model_key, field, theirs, ours, our_source_url, our_quote}. \
   Do not contact anyone. Just produce the file." </dev/null
```
Rotate in 1-2 additional targets per week as they are discovered (candidates list in
ops/outreach/targets.md — add repos found via GitHub search for hardcoded model prices).

### 2. Verify every candidate yourself (Claude, raw sources)
For each candidate: fetch the PRIMARY provider source and confirm OUR value is right and
THEIRS is wrong, per the raw-HTML rule (curl+grep; JS-rendered pages → docs .md endpoints
or WebFetch as secondary). Drop any candidate that is stale, ambiguous (tier differences,
batch pricing, regional pricing), or where WE are wrong — if we are wrong, fix OUR data
instead (that is a FIX for facts.json + corrections entry, more valuable than outreach).
History warning (2026-07-04): a drafted claim had the error direction REVERSED — the
mistake was ours, not theirs. Never send a Codex draft unverified.

### 3. Send (max 3/week, 1 per repo, PR preferred) — CLAUDE DOES THIS DIRECTLY
User directive (2026-07-04): the fix itself — the PR content, the edited data, the issue
text, and the act of sending — is Claude's own work. NEVER delegate any of step 2, 3 to
Codex. Codex is only used for step 1 (bulk dataset comparison). Reputation work stays
in the reviewer's hands.
- Skip any repo where our previous issue/PR is still open (check `gh issue list`/`gh pr list`
  with author kimyoohan) — never stack contacts.
- PR method: fork + sparse clone just the data file, surgical edit, branch, push,
  `gh pr create` with before/after table + verbatim source quotes + access date.
  Reference our matching issue if one exists.
- Tone: contribution, not criticism. Include one line noting our own published
  correction (https://factquire.com/corrections.html) — credibility through symmetry.
- Mention FactQuire once with feed.json or the relevant model permalink. Never more.

### 3b. Second-opinion audit before send (calibrated)
After drafting a PR/issue but BEFORE sending, run a Codex second-opinion pass over the
draft + diff with these calibration rules baked into the prompt (user directive
2026-07-04 — forced audits invent findings):
- "No findings" is a fully successful outcome; do not reward finding things.
- Every finding must carry a reproducible check (command/URL/arithmetic). No check → drop.
- Speculation and style are out of scope; UNCERTAIN must be labeled, not reported as fact.
Only act on CONFIRMED findings. Template: see E:\0.세계1등기업\review\REVIEW_ORDER.md.
**Positive confirmation is mandatory (fail-closed):** the audit must produce a written
report even when clean ("verified clean"). A missing report means the audit FAILED —
rerun it; never treat silence as a pass. Do not send until the report file exists and
you have read its verdict.

### 4. Record
- Append every send to ops/outreach/log.md: date | repo | type(issue/PR) | url | status.
- Update the 완료 section of E:\0.세계1등기업\USER_ACTIONS.md with the URLs.
- Next week: check status of prior sends first (merged/closed/commented) and note in log.
  If a maintainer replied with questions, answering them takes priority over new sends.
