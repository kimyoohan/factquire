# WORK_ORDER — ModelWire MVP (verified facts feed for commercial LLM APIs)

You are building the MVP of ModelWire: a machine-readable, source-verified facts feed
about commercial LLM APIs. Trust is the entire product. Never guess a value.

## Deliverables (all inside this directory)

### 1. `schema/model_fact.schema.json`
JSON Schema (draft 2020-12) for one model entry. Required structure:

- `provider` (string, e.g. "openai", "anthropic", "google", "mistral", "cohere", "xai", "deepseek", "amazon", "meta")
- `model_id` (string, the exact API identifier, e.g. "claude-sonnet-5")
- `display_name` (string)
- `status` (enum: "ga" | "preview" | "deprecated" | "retired")
- `release_date` (ISO date or null)
- `deprecation_date`, `retirement_date` (ISO date or null)
- `pricing` (object, USD per 1M tokens):
  - `input_per_mtok`, `output_per_mtok` (number or null)
  - `cached_input_per_mtok` (number or null)
  - `batch_discount_pct` (number or null)
- `context_window_tokens` (integer or null)
- `max_output_tokens` (integer or null)
- `modalities` (object: `input` array, `output` array; values from "text","image","audio","video")
- `knowledge_cutoff` (string or null)
- `sources` (array, min 1): each `{ "url": string, "accessed_at": ISO datetime, "fields": [names covered by this source], "quote": string — VERBATIM text copied from the page that supports the values }`
- `verified_at` (ISO datetime)
- `notes` (string or null)

### 2. `data/facts.json`
Array of entries validating against the schema.

- **≥ 40 models across ≥ 6 providers.** Include at minimum: OpenAI, Anthropic, Google (Gemini API), Mistral, DeepSeek, xAI. Add Cohere and Amazon Bedrock (Nova) if time permits.
- Current-generation and still-purchasable previous-generation models. Skip fine-tune-only SKUs.
- **PRIMARY SOURCES ONLY**: official provider docs, pricing pages, changelogs, official blogs.
  Forbidden: Wikipedia, artificialanalysis.ai, openrouter, news articles, any third-party aggregator.
- A field you cannot confirm from a primary source stays `null` and gets a line in `gaps.md`
  (model, field, where you looked). Guessing = automatic FAIL.
- Every numeric fact must be covered by at least one source whose `quote` contains that number
  (or the number in another unit, e.g. per-1K pricing — convert and note the conversion in `notes`).

### 3. `scripts/validate.py`
Python 3, stdlib + `jsonschema` only (pip install allowed). Checks:
- facts.json validates against the schema
- ≥ 40 entries, ≥ 6 distinct providers
- every entry has ≥ 1 source; every source has non-empty url, accessed_at, quote
- no duplicate (provider, model_id)
- every non-null pricing/context field is listed in some source's `fields`
Exit 0 on pass, non-zero with a readable report on fail.

### 4. `site/`
Static site, no framework, no build step (plain HTML + one JS file + one CSS file):
- `site/index.html` — sortable/filterable table of all models (filter by provider and status,
  sort by price). Load data from `site/feed.json`.
- `site/feed.json` — copy of data/facts.json plus `{ "generated_at": ..., "count": ..., "version": "0.1" }` wrapper.
- `site/about.html` — one page: what this is, sourcing policy (primary sources only, verbatim
  quotes, corrections published), how to consume the feed programmatically.
- `netlify.toml` at repo root publishing `site/`.
- `scripts/build_site.py` — regenerates site/feed.json from data/facts.json.
- Design: clean, dense, readable. No AI chat features. English only.

### 5. `gaps.md` and `README.md`
README: what ModelWire is, how to run validate/build, sourcing policy.

## Definition of done (ALL must hold)
1. `python scripts/validate.py` exits 0.
2. `data/facts.json` has ≥ 40 models, ≥ 6 providers, zero schema violations.
3. Opening `site/index.html` in a browser shows the full table; provider filter and price sort work.
4. Spot-check contract — these will be independently re-verified by a reviewer against the live
   official pages, so they must match reality at your collection time:
   - Every OpenAI and Anthropic entry's `input_per_mtok`/`output_per_mtok` matches the official
     pricing page exactly.
   - Every `deprecation_date`/`retirement_date` you set appears verbatim in the cited source quote.
   - At least 3 providers have ≥ 5 models each.
5. `git log` shows incremental commits (init → schema → data → validator → site).

## Rules
- Work autonomously until the Definition of done is met. Do not stop to ask questions.
- Commit as you go with meaningful messages.
- USD only. Token prices normalized to per-1M tokens.
- Record accessed_at honestly (actual fetch time, UTC).
