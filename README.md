# FactQuire

FactQuire (factquire.com) is a machine-readable, source-verified facts feed for commercial LLM APIs. It tracks model identifiers, pricing, lifecycle status, token limits, modalities, and primary-source evidence.

## Publish (the everyday command)

```bash
py scripts/publish.py                 # build → detect changes → commit+push → wait deploy → ping only changed URLs
py scripts/publish.py -m "메시지"      # custom commit message
py scripts/publish.py --dry-run       # preview what would be published
py scripts/publish.py --full-ping     # ping entire sitemap after deploy
```

After editing `data/facts.json` (adding models, price changes, etc.), run `py scripts/publish.py` once. It regenerates the site, publishes only what changed, verifies the deploy landed, and notifies search engines (IndexNow) of just the changed URLs.

## IndexNow (search engine ping, standalone)

```bash
py scripts/indexnow.py                # submit all sitemap URLs
py scripts/indexnow.py --new          # submit only never-submitted URLs
py scripts/indexnow.py --provider groq  # submit one provider's model pages
py scripts/indexnow.py <url> [url...] # submit specific URLs
py scripts/indexnow.py --dry-run      # preview without sending
py scripts/indexnow.py --log          # show submission history (ops/indexnow-log.jsonl)
```

## Files

- `schema/model_fact.schema.json` defines one model fact entry.
- `data/facts.json` is the source facts array.
- `data/changelog.json` records release-level model additions, removals, and field changes.
- `data/archive/` stores prior facts snapshots before weekly refresh edits.
- `site/feed.json` is the public feed wrapper generated from `data/facts.json`.
- `site/changelog.json` is generated from `data/changelog.json`.
- `gaps.md` lists fields left null because collected primary sources did not confirm them.

## Validate

```bash
python scripts/validate.py
```

On this Windows workspace, use the Python launcher if `python` resolves to the Microsoft Store alias:

```bash
py scripts/validate.py
```

## Build Site Feed

```bash
python scripts/build_site.py
```

Then open `site/index.html` in a browser. The table supports provider filtering, status filtering, and input/output price sorting.

## Changelog Diff

```bash
py scripts/diff_facts.py data/archive/facts-YYYY-MM-DD.json data/facts.json
```

Tests can be run with either command:

```bash
py -m pytest tests/
py tests/test_diff_facts.py
```

## Weekly Refresh Archive

Before editing `data/facts.json` during a weekly refresh, archive the previous file as `data/archive/facts-<date>.json`. Then update facts, run the diff script against that archive, and use the resulting entries for the next `data/changelog.json` release.

## Sourcing Policy

FactQuire uses primary sources only: official provider docs, official pricing pages, official changelogs, and official blogs. Every source record includes the source URL, access timestamp, covered fields, and a verbatim quote supporting the values. Values that could not be confirmed from a collected primary source remain `null` and are recorded in `gaps.md`.

Prices are normalized to USD per 1M tokens. When providers publish multiple tiers for the same model, notes identify which cited tier was recorded.
