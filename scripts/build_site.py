#!/usr/bin/env python3
import html
import json
import re
import secrets
import shutil
from collections import defaultdict
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://factquire.com"
SUBSCRIBE_ENDPOINT = "https://factquire-notify.pages.dev/subscribe"
FACTS_PATH = ROOT / "data" / "facts.json"
CHANGELOG_PATH = ROOT / "data" / "changelog.json"
AUDIT_PATH = ROOT / "data" / "audit.json"
CONTENT_DIR = ROOT / "content"
ARTICLES_DIR = CONTENT_DIR / "articles"
PAGES_DIR = CONTENT_DIR / "pages"
ROOTFILES_DIR = CONTENT_DIR / "rootfiles"
WELL_KNOWN_DIR = CONTENT_DIR / "well-known"
SITE_DIR = ROOT / "site"
MODELS_DIR = SITE_DIR / "models"
NEWS_DIR = SITE_DIR / "news"
WELL_KNOWN_SITE_DIR = SITE_DIR / ".well-known"
OPS_DIR = ROOT / "ops"
INDEXNOW_KEY_PATH = OPS_DIR / "indexnow-key.txt"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path, data):
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def sanitize_filename(value):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value))


def url_for(path):
    normalized = path if path.startswith("/") else f"/{path}"
    return f"{BASE_URL}{normalized}"


def escape(value):
    return html.escape("" if value is None else str(value), quote=True)


def text_value(value):
    if value is None:
        return "-"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}: {text_value(val)}" for key, val in value.items())
    return str(value)


def parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def rfc822(value):
    parsed = parse_date(value) or date.today()
    dt = datetime.combine(parsed, time(0, 0), tzinfo=timezone.utc)
    return format_datetime(dt, usegmt=True)


def json_ld(data):
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{payload}</script>'


def inline_markdown(text):
    escaped = escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{escape(match.group(2))}"'
            f'>{match.group(1)}</a>'
        ),
        escaped,
    )
    return escaped


def markdown_to_html(markdown):
    blocks = []
    paragraph = []
    in_list = False

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph = []

    def close_list():
        nonlocal in_list
        if in_list:
            blocks.append("</ul>")
            in_list = False

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            close_list()
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        bullet = re.match(r"^-\s+(.+)$", line)

        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
        elif bullet:
            flush_paragraph()
            if not in_list:
                blocks.append("<ul>")
                in_list = True
            blocks.append(f"<li>{inline_markdown(bullet.group(1))}</li>")
        else:
            paragraph.append(line)

    flush_paragraph()
    close_list()
    return "\n".join(blocks)


def parse_front_matter(path):
    text = path.read_text(encoding="utf-8")
    metadata = {}
    body = text
    if text.startswith("---\n"):
        _, front, body = text.split("---\n", 2)
        for line in front.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            value = value.strip().strip('"').strip("'")
            metadata[key.strip()] = value
    return metadata, body.strip()


def page(title, description, path, body, current=None, extra_head="", jsonld=None):
    canonical = url_for(path)
    jsonld_markup = json_ld(jsonld) if jsonld else ""
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(description)}">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" type="application/rss+xml" title="FactQuire RSS" href="{BASE_URL}/rss.xml">
    <link rel="icon" href="/favicon.ico" sizes="32x32">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
    <link rel="apple-touch-icon" href="/assets/favicon-512.png">
    <meta property="og:title" content="{escape(title)}">
    <meta property="og:description" content="{escape(description)}">
    <meta property="og:image" content="{BASE_URL}/assets/og-card.png">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="/styles.css">
    {jsonld_markup}
    {extra_head}
  </head>
  <body>
    <header class="topbar">
      <div>
        <a href="/" style="display:inline-block;line-height:0;">
          <img src="/assets/logo.png" alt="FactQuire" height="48" style="height:48px;width:auto;">
        </a>
      </div>
      <nav>
        {nav_link("Models", "/models/", current == "models")}
        {nav_link("News", "/news/", current == "news")}
        {nav_link("Changelog", "/changelog.html", current == "changelog")}
        {nav_link("Audit", "/audit.html", current == "audit")}
        {nav_link("About", "/about.html", current == "about")}
      </nav>
    </header>
    <main>
{body}
    </main>
    <section class="subscribe" id="subscribe">
      <div class="subscribe-inner">
        <strong>Price &amp; deprecation alerts</strong>
        <p>One weekly email when any tracked model changes price or limits, or gets deprecated. Every change source-verified. No spam, unsubscribe anytime.
        Want per-model alerts within a day? <a href="/watchlist.html">Create a free watchlist →</a></p>
        <form id="subscribe-form" action="{SUBSCRIBE_ENDPOINT}" method="post">
          <input type="email" name="email" required placeholder="you@company.com" aria-label="Email address">
          <input type="text" name="website" tabindex="-1" autocomplete="off" class="hp-field" aria-hidden="true">
          <button type="submit">Subscribe</button>
        </form>
        <p id="subscribe-status" role="status"></p>
      </div>
    </section>
    <script>
    (function () {{
      var form = document.getElementById("subscribe-form");
      if (!form) return;
      var status = document.getElementById("subscribe-status");
      form.addEventListener("submit", function (ev) {{
        ev.preventDefault();
        var email = form.email.value.trim();
        if (!email) return;
        status.textContent = "Subscribing…";
        fetch(form.action, {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ email: email, website: form.website.value }})
        }}).then(function (r) {{ return r.json().catch(function () {{ return {{}}; }}).then(function (d) {{ return {{ ok: r.ok, data: d }}; }}); }})
          .then(function (res) {{
            if (res.ok) {{
              status.textContent = "Subscribed. You’ll get the next weekly digest.";
              form.reset();
            }} else {{
              status.textContent = res.data && res.data.error ? res.data.error : "Something went wrong — please try again later.";
            }}
          }})
          .catch(function () {{ status.textContent = "Network error — please try again later."; }});
      }});
    }})();
    </script>
    <footer class="site-footer">
      <a href="/corrections.html">corrections</a> |
      <a href="/editorial.html">editorial</a> |
      <a href="/cite.html">cite</a>
    </footer>
  </body>
</html>
"""


def nav_link(label, href, active=False):
    current = ' aria-current="page"' if active else ""
    return f'<a href="{href}"{current}>{label}</a>'


def field_table(entry):
    rows = []
    for key, value in entry.items():
        if key == "sources":
            continue
        rows.append(
            "<tr>"
            f"<th>{escape(key)}</th>"
            f"<td><code>{escape(json.dumps(value, ensure_ascii=False))}</code></td>"
            "</tr>"
        )
    return "<table class=\"fact-table\"><tbody>" + "\n".join(rows) + "</tbody></table>"


def source_list(sources):
    if not sources:
        return "<p>No sources recorded.</p>"
    items = []
    for source in sources:
        fields = ", ".join(source.get("fields", []))
        items.append(
            "<li>"
            f"<p><a href=\"{escape(source.get('url'))}\">{escape(source.get('url'))}</a></p>"
            f"<p><strong>Accessed:</strong> {escape(source.get('accessed_at'))}</p>"
            f"<p><strong>Fields:</strong> {escape(fields)}</p>"
            f"<blockquote>{escape(source.get('quote'))}</blockquote>"
            "</li>"
        )
    return "<ol class=\"source-list\">" + "\n".join(items) + "</ol>"


def entry_line(entry):
    model = f"{entry.get('provider')}/{entry.get('model_id')}"
    change_type = entry.get("type", "changed")
    if change_type == "added":
        return f"{model} added"
    if change_type == "removed":
        return f"{model} removed"
    field = entry.get("field", "field")
    old = text_value(entry.get("old"))
    new = text_value(entry.get("new"))
    return f"{model} {field} changed from {old} to {new}"


def model_history(changelog, provider, model_id):
    matches = []
    for release in changelog.get("releases", []):
        for entry in release.get("entries", []):
            if entry.get("provider") == provider and entry.get("model_id") == model_id:
                matches.append((release, entry))
    if not matches:
        return "<p>No changelog entries for this model.</p>"
    items = []
    for release, entry in matches:
        items.append(
            "<li>"
            f"<strong>{escape(release.get('date'))} v{escape(release.get('version'))}</strong>: "
            f"{escape(entry_line(entry))}"
            "</li>"
        )
    return "<ul class=\"changes\">" + "\n".join(items) + "</ul>"


def make_model_permalink(entry):
    provider = sanitize_filename(entry["provider"])
    model_id = sanitize_filename(entry["model_id"])
    return f"/models/{provider}/{model_id}.html"


def build_model_pages(facts, changelog):
    by_provider = defaultdict(list)
    for entry in facts:
        by_provider[entry["provider"]].append(entry)

    for provider, entries in by_provider.items():
        for entry in sorted(entries, key=lambda item: item["model_id"]):
            augmented = dict(entry)
            augmented["permalink"] = make_model_permalink(entry)
            provider_dir = MODELS_DIR / sanitize_filename(provider)
            model_name = sanitize_filename(entry["model_id"])
            title = f"{entry.get('display_name') or entry['model_id']} - FactQuire"
            description = f"Source-verified LLM API facts for {entry['provider']}/{entry['model_id']}."
            body = f"""      <article class="model-detail">
        <p class="eyebrow">{escape(entry["provider"])}</p>
        <h1>{escape(entry.get("display_name") or entry["model_id"])}</h1>
        <p><code>{escape(entry["model_id"])}</code></p>
        <h2>Fields</h2>
        {field_table(augmented)}
        <h2>Sources</h2>
        {source_list(entry.get("sources", []))}
        <h2>Verified At</h2>
        <p>{escape(entry.get("verified_at"))}</p>
        <h2>Changelog History</h2>
        {model_history(changelog, entry["provider"], entry["model_id"])}
      </article>"""
            dataset = {
                "@context": "https://schema.org",
                "@type": "Dataset",
                "name": f"FactQuire facts for {entry['provider']}/{entry['model_id']}",
                "url": url_for(augmented["permalink"]),
                "dateModified": entry.get("verified_at"),
                "creator": {"@type": "Organization", "name": "FactQuire"},
            }
            write_text(
                provider_dir / f"{model_name}.html",
                page(title, description, augmented["permalink"], body, "models", jsonld=dataset),
            )
            write_json(provider_dir / f"{model_name}.json", augmented)

    sections = []
    for provider in sorted(by_provider):
        links = []
        for entry in sorted(by_provider[provider], key=lambda item: item["model_id"]):
            permalink = make_model_permalink(entry)
            links.append(
                f'<li><a href="{permalink}">{escape(entry["model_id"])}</a> '
                f'<span class="muted">{escape(entry.get("status"))}</span></li>'
            )
        sections.append(f"<section><h2>{escape(provider)}</h2><ul>{''.join(links)}</ul></section>")
    body = "      <h1>Models</h1>\n" + "\n".join(sections)
    write_text(
        MODELS_DIR / "index.html",
        page(
            "Models - FactQuire",
            "All source-verified LLM API model fact pages grouped by provider.",
            "/models/",
            body,
            "models",
        ),
    )


def build_feed(facts, changelog, generated_at):
    latest_version = changelog.get("releases", [{}])[0].get("version", "0.1")
    models = []
    for entry in facts:
        augmented = dict(entry)
        augmented["permalink"] = make_model_permalink(entry)
        models.append(augmented)
    feed = {
        "generated_at": generated_at,
        "count": len(models),
        "version": latest_version,
        "models": models,
    }
    write_json(SITE_DIR / "feed.json", feed)
    write_json(SITE_DIR / "changelog.json", changelog)
    if AUDIT_PATH.exists():
        write_json(SITE_DIR / "audit.json", load_json(AUDIT_PATH))
    return feed


def build_articles():
    articles = []
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        meta, body_md = parse_front_matter(path)
        slug = meta.get("slug") or sanitize_filename(path.stem)
        article = {
            "title": meta.get("title", slug.replace("-", " ").title()),
            "date": meta.get("date", ""),
            "slug": slug,
            "summary": meta.get("summary", ""),
            "html": markdown_to_html(body_md),
        }
        articles.append(article)

    articles.sort(key=lambda item: item.get("date", ""), reverse=True)

    for article in articles:
        path = f"/news/{sanitize_filename(article['slug'])}.html"
        body = f"""      <article class="article">
        <h1>{escape(article["title"])}</h1>
        <p class="muted">{escape(article.get("date"))}</p>
        {article["html"]}
      </article>"""
        ld = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": article["title"],
            "datePublished": article.get("date"),
            "description": article.get("summary"),
            "url": url_for(path),
            "publisher": {"@type": "Organization", "name": "FactQuire"},
        }
        write_text(
            NEWS_DIR / f"{sanitize_filename(article['slug'])}.html",
            page(article["title"], article.get("summary", ""), path, body, "news", jsonld=ld),
        )

    if articles:
        items = "\n".join(
            f'<li><a href="/news/{sanitize_filename(article["slug"])}.html">'
            f'{escape(article["title"])}</a> <span class="muted">{escape(article.get("date"))}</span>'
            f'<p>{escape(article.get("summary"))}</p></li>'
            for article in articles
        )
    else:
        items = "<li>No news articles yet.</li>"
    body = f"      <h1>News</h1>\n      <ul class=\"article-list\">{items}</ul>"
    write_text(
        NEWS_DIR / "index.html",
        page("News - FactQuire", "FactQuire news and release notes.", "/news/", body, "news"),
    )
    return articles


def changelog_items(changelog):
    items = []
    for release in sorted(changelog.get("releases", []), key=lambda item: item.get("date", ""), reverse=True):
        changes = "".join(f"<li>{escape(entry_line(entry))}</li>" for entry in release.get("entries", []))
        items.append(
            f'<section class="release"><h2>v{escape(release.get("version"))} - '
            f'{escape(release.get("date"))}</h2><p>{escape(release.get("summary"))}</p>'
            f'<ul class="changes">{changes}</ul></section>'
        )
    return "\n".join(items)


def build_core_pages(facts, changelog):
    rows = []
    for entry in sorted(facts, key=lambda item: (item["provider"], item["model_id"])):
        pricing = entry.get("pricing", {})
        rows.append(
            "<tr>"
            f"<td>{escape(entry['provider'])}</td>"
            f"<td><a href=\"{make_model_permalink(entry)}\"><code>{escape(entry['model_id'])}</code></a></td>"
            f"<td><span class=\"badge {escape(entry.get('status'))}\">{escape(entry.get('status'))}</span></td>"
            f"<td>{escape(text_value(pricing.get('input_per_mtok')))}</td>"
            f"<td>{escape(text_value(pricing.get('output_per_mtok')))}</td>"
            f"<td>{escape(text_value(entry.get('context_window_tokens')))}</td>"
            f"<td>{escape(text_value(entry.get('max_output_tokens')))}</td>"
            "</tr>"
        )
    index_body = f"""      <section class="intro">
        <h1>FactQuire</h1>
        <p>Source-verified facts about commercial LLM APIs: pricing, limits, lifecycle, and primary-source quotes.</p>
      </section>
      <section class="table-wrap">
        <table>
          <thead><tr><th>Provider</th><th>Model ID</th><th>Status</th><th>Input $/1M</th><th>Output $/1M</th><th>Context</th><th>Max Output</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </section>"""
    organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "FactQuire",
        "url": BASE_URL,
        "sameAs": [],
    }
    write_text(
        SITE_DIR / "index.html",
        page(
            "FactQuire - Verified LLM API Facts",
            "Source-verified facts about commercial LLM APIs: pricing, token limits, lifecycle status, and primary-source quotes.",
            "/",
            index_body,
            "models",
            jsonld=organization,
        ),
    )

    write_text(
        SITE_DIR / "changelog.html",
        page(
            "Changelog - FactQuire",
            "Versioned release history for the FactQuire verified LLM API facts feed.",
            "/changelog.html",
            f"      <h1>Changelog</h1>\n{changelog_items(changelog)}",
            "changelog",
        ),
    )

    audit_body = "      <h1>Audit</h1>\n"
    if AUDIT_PATH.exists():
        audit = load_json(AUDIT_PATH)
        audit_body += "<p>Independent comparison vs LiteLLM and models.dev.</p>"
        audit_body += f"<pre>{escape(json.dumps(audit, indent=2, ensure_ascii=False))}</pre>"
    else:
        audit_body += "<p>No audit data is available yet.</p>"
    write_text(
        SITE_DIR / "audit.html",
        page(
            "Audit - FactQuire",
            "Independent comparison of FactQuire facts against external LLM metadata datasets.",
            "/audit.html",
            audit_body,
            "audit",
        ),
    )

    about_body = """      <h1>About</h1>
      <p>FactQuire is a machine-readable, source-verified facts feed for commercial LLM APIs.</p>
      <p>The dataset tracks model identifiers, pricing, lifecycle status, token limits, modalities, source evidence, and changelog history.</p>"""
    write_text(
        SITE_DIR / "about.html",
        page(
            "About - FactQuire",
            "About the FactQuire source-verified LLM API facts feed.",
            "/about.html",
            about_body,
            "about",
        ),
    )


def build_trust_pages(changelog):
    corrections = []
    for release in changelog.get("releases", []):
        for entry in release.get("entries", []):
            if entry.get("type") == "corrected":
                corrections.append((release, entry))
    corrections.sort(key=lambda item: item[0].get("date", ""), reverse=True)
    if corrections:
        items = []
        for release, entry in corrections:
            items.append(
                "<li>"
                f"<strong>{escape(release.get('date'))} v{escape(release.get('version'))}</strong>: "
                f"{escape(entry_line(entry))}"
                "</li>"
            )
        corrections_body = f"      <h1>Corrections</h1>\n      <ul>{''.join(items)}</ul>"
    else:
        corrections_body = (
            '      <h1>Corrections</h1>\n'
            '      <p>No corrections to date. Correction policy: '
            '<a href="/editorial.html">editorial standards</a>.</p>'
        )
    write_text(
        SITE_DIR / "corrections.html",
        page(
            "Corrections - FactQuire",
            "FactQuire corrections and correction policy.",
            "/corrections.html",
            corrections_body,
        ),
    )

    editorial_path = PAGES_DIR / "editorial-standards.md"
    if editorial_path.exists():
        _, editorial_md = parse_front_matter(editorial_path)
        editorial_body = "      " + markdown_to_html(editorial_md).replace("\n", "\n      ")
    else:
        editorial_body = """      <h1>Editorial Standards</h1>
      <p>FactQuire uses primary sources only: official provider docs, pricing pages, changelogs, and official blogs.</p>
      <p>Every sourced value includes a verbatim quote, source URL, accessed timestamp, and covered fields.</p>
      <p>Collection and review are split: collectors gather evidence and reviewers check normalization, source coverage, and changelog impact before publication.</p>"""
    write_text(
        SITE_DIR / "editorial.html",
        page(
            "Editorial Standards - FactQuire",
            "FactQuire sourcing, verification, and review policy.",
            "/editorial.html",
            editorial_body,
        ),
    )

    cite_body = """      <h1>Cite This Feed</h1>
      <h2>Stable URLs</h2>
      <ul>
        <li><code>https://factquire.com/feed.json</code></li>
        <li><code>https://factquire.com/models/&lt;provider&gt;/&lt;model_id&gt;.html</code></li>
        <li><code>https://factquire.com/models/&lt;provider&gt;/&lt;model_id&gt;.json</code></li>
      </ul>
      <h2>BibTeX</h2>
      <pre>@misc{factquire,
  title = {FactQuire Verified LLM API Facts Feed},
  howpublished = {https://factquire.com/feed.json},
  note = {Cite both FactQuire and the primary source evidence for each fact}
}</pre>
      <h2>JSON</h2>
      <pre>{
  "dataset": "FactQuire Verified LLM API Facts Feed",
  "url": "https://factquire.com/feed.json",
  "note": "Cite both FactQuire and the primary source evidence for each fact."
}</pre>
      <p>Cite both FactQuire and the primary source for any fact you reuse.</p>"""
    write_text(
        SITE_DIR / "cite.html",
        page("Cite This Feed - FactQuire", "Citation guide for FactQuire facts.", "/cite.html", cite_body),
    )


def build_watchlist_page(facts):
    model_keys = sorted(f"{entry.get('provider')}/{entry.get('model_id')}" for entry in facts)
    options = "\n".join(f'<option value="{escape(key)}"></option>' for key in model_keys)
    picker_rows = []
    for index in range(1, 11):
        picker_rows.append(f"""
      <div class="watch-row">
        <input list="model-keys" class="watch-model" id="watch-model-{index}" placeholder="{'provider/model-id (e.g. openai/gpt-5.6-terra)' if index == 1 else 'optional'}" aria-label="Model {index}">
        <input type="number" class="watch-vol-in" min="0" step="0.1" placeholder="input Mtok/mo" aria-label="Model {index} monthly input million tokens">
        <input type="number" class="watch-vol-out" min="0" step="0.1" placeholder="output Mtok/mo" aria-label="Model {index} monthly output million tokens">
      </div>""")
    body = f"""      <h1>Free model watchlist</h1>
      <p>Pick up to 10 models. Whenever a watched model's <strong>price, token limits, status, or deprecation date</strong>
      changes in our source-verified data, you get an email within a day — with the provider's own quote backing the change.</p>
      <p>Optionally add your monthly volume (millions of tokens) and the alert includes your estimated monthly cost impact.</p>
      <datalist id="model-keys">
{options}
      </datalist>
      <form id="watchlist-form">
        {''.join(picker_rows)}
        <div class="watch-row">
          <input type="email" id="watch-email" required placeholder="you@company.com" aria-label="Email address">
          <input type="text" id="watch-hp" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
          <button type="submit">Start watching</button>
        </div>
        <p id="watchlist-status" role="status"></p>
      </form>
      <p class="watch-note">Free — 3 models per email, checked daily, unsubscribe anytime. Data source: the same
      <a href="/audit.html">audited</a> facts feed that powers this site.</p>
      <script>
      (function () {{
        var form = document.getElementById("watchlist-form");
        var status = document.getElementById("watchlist-status");
        form.addEventListener("submit", function (ev) {{
          ev.preventDefault();
          var models = [];
          var volumes = {{}};
          document.querySelectorAll(".watch-row").forEach(function (row) {{
            var m = row.querySelector(".watch-model");
            if (!m || !m.value.trim()) return;
            var key = m.value.trim();
            models.push(key);
            var vin = parseFloat((row.querySelector(".watch-vol-in") || {{}}).value);
            var vout = parseFloat((row.querySelector(".watch-vol-out") || {{}}).value);
            if (!isNaN(vin) || !isNaN(vout)) {{
              volumes[key] = {{ inputMTok: isNaN(vin) ? 0 : vin, outputMTok: isNaN(vout) ? 0 : vout }};
            }}
          }});
          if (!models.length) {{ status.textContent = "Pick at least one model."; return; }}
          status.textContent = "Saving…";
          fetch("https://factquire-watchdog.azij.workers.dev/watchlist", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ email: document.getElementById("watch-email").value.trim(), models: models, volumes: volumes, website: document.getElementById("watch-hp").value }})
          }}).then(function (r) {{ return r.json().catch(function () {{ return {{}}; }}).then(function (d) {{ return {{ ok: r.ok, data: d }}; }}); }})
            .then(function (res) {{
              status.textContent = res.ok
                ? "Watching " + (res.data.watching || []).join(", ") + ". You'll get an email when any of them changes."
                : (res.data && res.data.error) || "Something went wrong — please try again.";
            }})
            .catch(function () {{ status.textContent = "Network error — please try again."; }});
        }});
      }})();
      </script>"""
    write_text(
        SITE_DIR / "watchlist.html",
        page(
            "Model watchlist - FactQuire",
            "Watch up to 3 LLM API models for free. Get a source-verified email within a day of any price, limit, or lifecycle change.",
            "/watchlist.html",
            body,
        ),
    )


def build_rss(articles, changelog):
    rss_items = []
    for article in articles:
        path = f"/news/{sanitize_filename(article['slug'])}.html"
        rss_items.append(
            {
                "title": article["title"],
                "link": url_for(path),
                "guid": url_for(path),
                "pubDate": rfc822(article.get("date")),
                "description": article.get("summary", ""),
            }
        )
    for release in changelog.get("releases", []):
        link = url_for(f"/changelog.html#v{quote(str(release.get('version', '')))}")
        rss_items.append(
            {
                "title": f"FactQuire v{release.get('version')}: {release.get('summary')}",
                "link": link,
                "guid": link,
                "pubDate": rfc822(release.get("date")),
                "description": release.get("summary", ""),
            }
        )
    if not rss_items:
        link = url_for("/changelog.html#v0.1")
        rss_items.append(
            {
                "title": "FactQuire v0.1",
                "link": link,
                "guid": link,
                "pubDate": rfc822(date.today()),
                "description": "Initial release placeholder.",
            }
        )

    items_xml = []
    for item in rss_items:
        items_xml.append(
            "    <item>\n"
            f"      <title>{escape(item['title'])}</title>\n"
            f"      <link>{escape(item['link'])}</link>\n"
            f"      <guid>{escape(item['guid'])}</guid>\n"
            f"      <pubDate>{escape(item['pubDate'])}</pubDate>\n"
            f"      <description>{escape(item['description'])}</description>\n"
            "    </item>"
        )
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>FactQuire</title>
    <link>{BASE_URL}/</link>
    <description>Source-verified LLM API fact changes and news.</description>
{chr(10).join(items_xml)}
  </channel>
</rss>
"""
    write_text(SITE_DIR / "rss.xml", rss)


def build_llms_files(facts, changelog):
    llms = """# FactQuire
> Source-verified facts about commercial LLM APIs -- pricing, limits, lifecycle, with primary-source quotes.

## Data
- [Verified model facts feed](https://factquire.com/feed.json): JSON feed, 40+ models, 7+ providers
- [Full dataset as plain text](https://factquire.com/llms-full.txt): human+machine readable

## Updates
- [Changelog](https://factquire.com/changelog.html): versioned release history
- [RSS feed](https://factquire.com/rss.xml): subscribe to fact changes and news

## Trust
- [Editorial standards](https://factquire.com/editorial.html): sourcing and verification policy
- [Corrections](https://factquire.com/corrections.html): all corrections with before/after values
- [Cite this feed](https://factquire.com/cite.html): citation guide
- [Audit](https://factquire.com/audit.html): independent comparison vs LiteLLM and models.dev
"""
    write_text(SITE_DIR / "llms.txt", llms)

    lines = ["# FactQuire full dataset", ""]
    by_provider = defaultdict(list)
    for entry in facts:
        by_provider[entry["provider"]].append(entry)
    for provider in sorted(by_provider):
        lines.append(f"## {provider}")
        lines.append("model_id\tinput_usd_per_1m\toutput_usd_per_1m\tcontext\tmax_output\tstatus")
        for entry in sorted(by_provider[provider], key=lambda item: item["model_id"]):
            pricing = entry.get("pricing", {})
            lines.append(
                "\t".join(
                    [
                        text_value(entry.get("model_id")),
                        text_value(pricing.get("input_per_mtok")),
                        text_value(pricing.get("output_per_mtok")),
                        text_value(entry.get("context_window_tokens")),
                        text_value(entry.get("max_output_tokens")),
                        text_value(entry.get("status")),
                    ]
                )
            )
        lines.append("")
    lines.append("## Changelog")
    for release in changelog.get("releases", []):
        lines.append(f"{release.get('date')}\tv{release.get('version')}\t{release.get('summary')}")
    write_text(SITE_DIR / "llms-full.txt", "\n".join(lines) + "\n")


def build_robots():
    robots = """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Bytespider
Allow: /
User-agent: CCBot
Allow: /
User-agent: Yeti
Allow: /

Sitemap: https://factquire.com/sitemap.xml
"""
    write_text(SITE_DIR / "robots.txt", robots)


def collect_site_urls(facts, articles):
    urls = [
        ("/", "daily", "1.0"),
        ("/models/", "daily", "0.9"),
        ("/news/", "weekly", "0.7"),
        ("/changelog.html", "daily", "0.8"),
        ("/audit.html", "weekly", "0.7"),
        ("/about.html", "monthly", "0.5"),
        ("/watchlist.html", "monthly", "0.7"),
        ("/corrections.html", "daily", "0.7"),
        ("/editorial.html", "monthly", "0.6"),
        ("/cite.html", "monthly", "0.6"),
        ("/feed.json", "daily", "0.8"),
        ("/rss.xml", "daily", "0.7"),
        ("/llms.txt", "daily", "0.8"),
        ("/llms-full.txt", "daily", "0.8"),
    ]
    for entry in facts:
        permalink = make_model_permalink(entry)
        urls.append((permalink, "weekly", "0.7"))
        urls.append((permalink.replace(".html", ".json"), "weekly", "0.6"))
    for article in articles:
        urls.append((f"/news/{sanitize_filename(article['slug'])}.html", "monthly", "0.6"))
    return urls


def build_sitemap(facts, articles, lastmod):
    url_entries = []
    for path, changefreq, priority in collect_site_urls(facts, articles):
        url_entries.append(
            "  <url>\n"
            f"    <loc>{escape(url_for(path))}</loc>\n"
            f"    <lastmod>{escape(lastmod)}</lastmod>\n"
            f"    <changefreq>{escape(changefreq)}</changefreq>\n"
            f"    <priority>{escape(priority)}</priority>\n"
            "  </url>"
        )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_entries)}
</urlset>
"""
    write_text(SITE_DIR / "sitemap.xml", sitemap)


def ensure_indexnow_key():
    OPS_DIR.mkdir(exist_ok=True)
    key = ""
    if INDEXNOW_KEY_PATH.exists():
        key = INDEXNOW_KEY_PATH.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9a-f]{32}", key):
        key = secrets.token_hex(16)
        write_text(INDEXNOW_KEY_PATH, key + "\n")
    write_text(SITE_DIR / f"{key}.txt", key)
    return key


def build_indexnow_script():
    script = '''#!/usr/bin/env python3
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://factquire.com"
KEY_PATH = ROOT / "ops" / "indexnow-key.txt"
SITEMAP_PATH = ROOT / "site" / "sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"


def main():
    key = KEY_PATH.read_text(encoding="utf-8").strip()
    tree = ET.parse(SITEMAP_PATH)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in tree.findall(".//sm:loc", ns) if node.text]
    payload = {
        "host": "factquire.com",
        "key": key,
        "keyLocation": f"{BASE_URL}/{key}.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        print(f"IndexNow response: {response.status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
    write_text(ROOT / "scripts" / "ping_indexnow.py", script)


def copy_passthrough_files():
    for directory in (ARTICLES_DIR, PAGES_DIR, ROOTFILES_DIR, WELL_KNOWN_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    for path in ROOTFILES_DIR.iterdir():
        if path.is_file():
            shutil.copy2(path, SITE_DIR / path.name)
    WELL_KNOWN_SITE_DIR.mkdir(parents=True, exist_ok=True)
    for path in WELL_KNOWN_DIR.iterdir():
        if path.is_file():
            shutil.copy2(path, WELL_KNOWN_SITE_DIR / path.name)


def main():
    facts = load_json(FACTS_PATH)
    changelog = load_json(CHANGELOG_PATH)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    lastmod = generated_at[:10]

    SITE_DIR.mkdir(exist_ok=True)
    copy_passthrough_files()
    build_feed(facts, changelog, generated_at)
    build_model_pages(facts, changelog)
    articles = build_articles()
    build_core_pages(facts, changelog)
    build_watchlist_page(facts)
    build_trust_pages(changelog)
    build_rss(articles, changelog)
    build_llms_files(facts, changelog)
    build_robots()
    build_sitemap(facts, articles, lastmod)
    key = ensure_indexnow_key()
    build_indexnow_script()

    print(f"Wrote site/feed.json with {len(facts)} models")
    print(f"Wrote {len(facts)} model pages")
    print(f"Wrote {len(articles)} news articles")
    print(f"Wrote IndexNow key {key}")


if __name__ == "__main__":
    main()
