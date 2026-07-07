# UPDATE_ORDER — weekly data refresh (recurring; executed by Codex every Monday)

Goal: keep ModelWire the accurate, source-verified record of commercial LLM API facts.
Sourcing rules are identical to WORK_ORDER phase 1: PRIMARY SOURCES ONLY (official provider
docs/pricing/changelogs), verbatim quotes containing the numbers, null + gaps.md when
unconfirmed, never guess. Never reconstruct a table from memory.

## Steps (in order)

1. **Archive**: copy `data/facts.json` → `data/archive/facts-<today ISO date>.json` (commit this first).
2. **Re-verify every entry** against its cited pages, fetched fresh:
   - Value changed on the live page → update value + quote + accessed_at, set verified_at now.
   - Value unchanged → refresh accessed_at + verified_at only.
   - Model no longer purchasable / marked deprecated or retired → update `status` and dates
     with a supporting quote. NEVER delete an entry; `retired` is a status, not a removal.
3. **Discover new models**: on each of the 7 providers' pricing/models pages, add any newly
   listed generally-purchasable API models (same rules; skip fine-tune-only SKUs). If a major
   NEW provider now clearly belongs (large public API launch), add it with ≥2 models and note
   it in the release summary.
4. **Changelog**: run `py scripts/diff_facts.py data/archive/facts-<today>.json data/facts.json`,
   turn the output into a new release in `data/changelog.json` (bump minor version, write a
   1-2 sentence human summary; empty diff → still add a release with summary "No changes; all
   facts re-verified" and entries []).
4b. **External audit**: run `py scripts/fetch_external.py` and `py scripts/audit_external.py`,
   adjudicate new mismatches against primary sources, and append a new audit entry to
   `data/audit.json`.
4c. **Story flywheel** (drafts only, never published): run `py scripts/detect_stories.py`.
   It emits `content/drafts/story-*.md` scaffolds for every REAL value change this cycle,
   each pre-filled with the before/after and the stored primary-source quote, plus
   `ops/stories/summary-<date>.md`. These are DRAFTS — do NOT publish them, do NOT move them
   to content/articles/. VERIFY_ORDER hands them to Claude for verification. Zero changes
   this cycle -> zero drafts (do not manufacture stories).
5. **Gaps**: update gaps.md (remove resolved lines, add new ones).
5b. **Evidence-debt paydown**: run `py scripts/logic_check.py`. Pick ~25 UNSUPPORTED
   warnings (rotate providers week to week) and re-capture quotes from the live cited
   pages so the stored quote CONTAINS the stored value (values themselves only change
   via step 2 rules). Remove the resolved keys from ops/logic-baseline.json so the
   baseline shrinks every week toward zero.
6. `py scripts/validate.py` must exit 0; run `py scripts/build_site.py`.
7. Commit everything with message `Weekly refresh <date>`. **DO NOT PUSH** — an independent
   verification pass (VERIFY_ORDER.md) pushes only after cross-checking.

## Definition of done
validate.py exits 0; changelog has today's release; archive file committed; working tree clean; not pushed.
