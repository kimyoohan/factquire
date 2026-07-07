# Story flywheel proof - 2026-07-07

Pass criteria A and B were run without web fetches. The injected test uses a temp copy under .tmp/story-flywheel and does not mutate data/facts.json or data/archive/*.

## A1 clean input detector run

```powershell
py scripts/detect_stories.py --date 2026-07-07
```

Output:
```text
Previous facts: E:\0.����1����\modelwire\data\archive\facts-2026-07-07.json
Current facts: E:\0.����1����\modelwire\data\facts.json
Real value changes: 0
Drafts emitted: 0
Needs re-sourcing: 0
Summary: E:\0.����1����\modelwire\ops\stories\summary-2026-07-07.md
```

## A2 clean input draft count

```powershell
@(Get-ChildItem -LiteralPath 'content\drafts' -File -ErrorAction SilentlyContinue).Count
```

Output:
```text
0
```

## A3 clean input draft listing

```powershell
Get-ChildItem -LiteralPath 'content\drafts' -File -ErrorAction SilentlyContinue | Select-Object Name,Length
```

Output:
```text
<no output>
```

## A4 clean input summary

```powershell
Get-Content -Raw -LiteralPath 'ops\stories\summary-2026-07-07.md'
```

Output:
```text
# Story flywheel summary - 2026-07-07

Latest changelog release: 2026-07-07 0.6
Real value changes: 0

No story opportunities this cycle (0 real value changes)
```

## B1 create temp archive with one injected old value

```powershell
@'
import json
from pathlib import Path
src = Path('data/archive/facts-2026-07-07.json')
dst = Path('.tmp/story-flywheel/facts-injected-old-price.json')
dst.parent.mkdir(parents=True, exist_ok=True)
data = json.loads(src.read_text(encoding='utf-8'))
for entry in data:
    if entry.get('provider') == 'openai' and entry.get('model_id') == 'gpt-5.5':
        entry['pricing']['input_per_mtok'] = 4.0
        break
else:
    raise SystemExit('target model not found')
dst.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(dst)
'@ | py -
```

Output:
```text
.tmp\story-flywheel\facts-injected-old-price.json
```

## B2 injected detector run

```powershell
py scripts/detect_stories.py --date 2026-07-07 --previous '.tmp\story-flywheel\facts-injected-old-price.json'
```

Output:
```text
Previous facts: .tmp\story-flywheel\facts-injected-old-price.json
Current facts: E:\0.����1����\modelwire\data\facts.json
Real value changes: 1
Drafts emitted: 1
- story-openai-gpt-5-5-pricing-input-per-mtok-2026-07-07.md
Needs re-sourcing: 0
Summary: E:\0.����1����\modelwire\ops\stories\summary-2026-07-07.md
```

## B3 injected draft count

```powershell
@(Get-ChildItem -LiteralPath 'content\drafts' -File -Filter 'story-*.md').Count
```

Output:
```text
1
```

## B4 injected draft listing

```powershell
Get-ChildItem -LiteralPath 'content\drafts' -File -Filter 'story-*.md' | Select-Object Name,Length
```

Output:
```text

Name                                                      Length
----                                                      ------
story-openai-gpt-5-5-pricing-input-per-mtok-2026-07-07.md    660
```

## B5 injected draft content

```powershell
Get-Content -Raw -LiteralPath 'content\drafts\story-openai-gpt-5-5-pricing-input-per-mtok-2026-07-07.md'
```

Output:
```text
---
status: draft
detected_at: "2026-07-07"
model: "gpt-5.5"
field: "pricing.input_per_mtok"
old_value: 4.0
new_value: 5.0
---

STATUS: DRAFT - unverified by Claude; do not publish

# openai quietly changed GPT-5.5 pricing.input_per_mtok

GPT-5.5 changed `pricing.input_per_mtok` from `4.0` to `5.0`.
Primary-source quote from facts.json:

> gpt-5.5$5.00$0.50$30.00$10.00$1.00$45.00

Source URL: https://developers.openai.com/api/docs/pricing

Accessed at: 2026-07-07T11:44:22Z

## Claude review checklist

- Re-verify quote against live source.
- Confirm effective date.
- Check whether external datasets still carry the old value.
```

## B6 injected summary

```powershell
Get-Content -Raw -LiteralPath 'ops\stories\summary-2026-07-07.md'
```

Output:
```text
# Story flywheel summary - 2026-07-07

Latest changelog release: 2026-07-07 0.6
Real value changes: 1

## Drafts emitted

- story-openai-gpt-5-5-pricing-input-per-mtok-2026-07-07.md

## Needs re-sourcing

- None
```

## C1 live-content contamination check

```powershell
git status --short -- content/articles site content/drafts ops/stories scripts/detect_stories.py ops/reports/story-flywheel-2026-07-07.md data/facts.json data/archive
```

Output:
```text
?? content/drafts/
?? ops/reports/story-flywheel-2026-07-07.md
?? ops/stories/
?? scripts/detect_stories.py
```

## C2 facts and archive unchanged check

```powershell
git status --short -- data/facts.json data/archive
```

Output:
```text
<no output>
```

