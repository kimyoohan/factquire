# VERIFY_ORDER — weekly independent cross-verification (executed by Claude after UPDATE_ORDER)

You are the reviewer, not the collector. Your job: catch wrong facts before they publish.
The collector's evidence is NOT proof — the live page is.

## Protocol

1. Preconditions: `git log -1` shows today's `Weekly refresh` commit; `py scripts/validate.py` exits 0.
   If UPDATE_ORDER didn't run or validation fails, stop and write `ops/ALERT-<date>.md` (do not push).
2. **Sample selection**: every entry that CHANGED this week (from the newest changelog release),
   plus enough unchanged entries to reach minimum 5 total, spanning ≥ 4 providers. Rotate the
   unchanged picks week to week — do not reuse last week's sample (see ops/reports/ history).
3. **Verification method — raw HTML only**: for each sampled entry, `curl -sL <cited url>` and
   grep for the exact numbers/dates. Page-summarizing fetch tools DROP TABLE COLUMNS — do not
   trust them for tables (proven 2026-07-04). JS-rendered pages: grep the embedded JSON payload too.
   A fact passes only if the number is present in the raw response (or its documented unit conversion).
4. **Verdict**:
   - ALL PASS → run `py scripts/publish.py -m "Weekly refresh <date>"` — it builds, pushes,
     confirms the live deploy (auto-reruns one transient Pages failure), and pings IndexNow
     for changed + new URLs. If it reports "deploy not confirmed", check `gh run list`,
     rerun the failed run (`gh run rerun <id>`), verify live generated_at via curl, then
     `py scripts/indexnow.py --new`. Then write `ops/reports/<date>.md`: sample list,
     evidence snippets, PASS.
   - ANY FAIL → write `FIX_ORDER-<date>.md` with exact reproduction (url, what the page shows,
     what facts.json claims), run
     `codex exec --sandbox danger-full-access -c model_reasoning_effort="medium" "Read FIX_ORDER-<date>.md and execute it fully." </dev/null`,
     then re-verify the failed items once. Still failing → DO NOT PUSH, write `ops/ALERT-<date>.md`
     with details. Either way write `ops/reports/<date>.md`.
5. Report file is mandatory every run — it is the audit trail and next week's rotation memory.
