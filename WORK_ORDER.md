# WORK_ORDER — Phase 2: changelog infrastructure (2026-07-04)

Phase 1 (schema/data/validator/site) is DONE and live at https://kimyoohan.github.io/modelwire/.
This phase builds the change-tracking machinery. The changelog IS the future product
("what changed this week") — treat it with the same rigor as facts.json.
Do NOT re-collect data from the web in this phase. No changes to values in data/facts.json.

## Deliverables

### 1. `scripts/diff_facts.py`
`py scripts/diff_facts.py <old_facts.json> <new_facts.json>` → prints a JSON array of entries:
- `{"type":"added","provider":...,"model_id":...}` — model present only in new
- `{"type":"removed","provider":...,"model_id":...}` — present only in old (should be rare; refresh policy is to mark retired, not delete)
- `{"type":"changed","provider":...,"model_id":...,"field":"pricing.input_per_mtok","old":...,"new":...}`
  — one entry per changed leaf field. Ignore fields: `sources`, `verified_at`, `notes` (evidence
  refreshes are not news). Everything else (pricing.*, status, dates, context/output limits,
  modalities, knowledge_cutoff, display_name) IS news.

### 2. `data/changelog.json`
`{"releases":[{"date":"YYYY-MM-DD","version":"0.1","summary":"...","entries":[...]}]}`
Seed with one release: date 2026-07-04, version 0.1, summary "Initial dataset: 40 models across
7 providers", entries = one "added" entry per current model in data/facts.json (generate, don't hand-write).

### 3. `site/changelog.html`
Renders changelog.json (fetched relatively, same pattern as app.js): newest release first,
human-readable lines like "openai/gpt-5.5 — input price $5.00 → $4.50". Add nav links between
index.html / changelog.html / about.html (all three pages).
`scripts/build_site.py` must now also copy data/changelog.json → site/changelog.json.

### 4. `tests/test_diff_facts.py`
Synthetic fixtures (two small facts arrays inline or in tests/fixtures/): cover added, removed,
one pricing change, one status change, and confirms `sources`/`verified_at` churn produces NO entry.
Runnable with `py -m pytest tests/` or plain `py tests/test_diff_facts.py` (your choice, document it).

### 5. `data/archive/` + docs
Create `data/archive/.gitkeep`. Document in README: weekly refresh archives the previous
facts.json as `data/archive/facts-<date>.json` before editing (UPDATE_ORDER.md relies on this).

## Definition of done
1. Tests pass; `py scripts/validate.py` still exits 0; `py scripts/build_site.py` regenerates site/ including changelog.json.
2. site/changelog.html shows the v0.1 release with 40 "added" lines; nav links work from all three pages.
3. data/facts.json byte-identical except nothing (no edits allowed).
4. Incremental commits. Do not push.
