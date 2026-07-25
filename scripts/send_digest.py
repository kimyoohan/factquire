#!/usr/bin/env python3
"""Send the weekly FactQuire alerts digest to the Resend audience.

Usage:
  py scripts/send_digest.py --dry-run          # write ops/digest-preview.html, send nothing
  py scripts/send_digest.py --test you@x.com   # send the digest to one address only
  py scripts/send_digest.py --if-changes       # send only when the latest changelog release
                                               # is fresh (<= MAX_AGE_DAYS) and has entries
  py scripts/send_digest.py                    # send broadcast unconditionally

Credentials are loaded from the shared key store (never stored in this repo):
  G:/0.홈페이지제작/_API키/resend.env  ->  RESEND_API_KEY, RESEND_AUDIENCE_ID
Environment variables of the same names take precedence.
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_PATH = ROOT / "data" / "changelog.json"
FACTS_PATH = ROOT / "data" / "facts.json"
PREVIEW_PATH = ROOT / "ops" / "digest-preview.html"
KEYSTORE = Path("G:/0.홈페이지제작/_API키/resend.env")
BASE_URL = "https://factquire.com"
FROM_ADDR = "FactQuire Alerts <alerts@notify.factquire.com>"
MAX_AGE_DAYS = 3  # --if-changes: how fresh the latest release must be


def load_credentials():
    creds = {}
    if KEYSTORE.exists():
        for line in KEYSTORE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                creds[key.strip()] = value.strip()
    for name in ("RESEND_API_KEY", "RESEND_AUDIENCE_ID"):
        if os.environ.get(name):
            creds[name] = os.environ[name]
    return creds


def latest_release(changelog):
    releases = sorted(changelog.get("releases", []), key=lambda r: r.get("date", ""), reverse=True)
    return releases[0] if releases else None


def model_url(provider, model_id):
    import re
    safe = lambda v: re.sub(r"[^a-zA-Z0-9_-]", "_", str(v))
    return f"{BASE_URL}/models/{safe(provider)}/{safe(model_id)}.html"


def render_digest(release, total_models, total_providers):
    rows = []
    order = {"added": 0, "changed": 1, "removed": 2}
    label = {"added": "New model", "changed": "Changed", "removed": "Removed"}
    entries = sorted(release.get("entries", []), key=lambda e: (order.get(e.get("type"), 9), e.get("provider", ""), e.get("model_id", "")))
    seen = set()
    for e in entries:
        dedupe_key = (e.get("type"), e.get("provider"), e.get("model_id"))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        url = model_url(e.get("provider"), e.get("model_id"))
        detail = e.get("detail") or e.get("summary") or ""
        rows.append(
            f'<tr><td style="padding:6px 10px;white-space:nowrap;color:#666;">{label.get(e.get("type"), e.get("type"))}</td>'
            f'<td style="padding:6px 10px;"><a href="{url}" style="color:#1a5fb4;text-decoration:none;">'
            f'{e.get("provider")}/{e.get("model_id")}</a>'
            + (f'<div style="color:#555;font-size:13px;">{detail}</div>' if detail else "")
            + "</td></tr>"
        )
    table = (
        f'<table style="border-collapse:collapse;width:100%;font-size:14px;">{"".join(rows)}</table>'
        if rows
        else '<p style="color:#444;">No fact changes this week — all tracked facts were re-verified against their primary sources.</p>'
    )
    return f"""<!doctype html>
<html><body style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:640px;margin:0 auto;padding:24px;color:#1c1c1c;">
  <p style="margin:0 0 4px;"><a href="{BASE_URL}" style="color:#1c1c1c;font-weight:700;font-size:18px;text-decoration:none;">FactQuire</a></p>
  <p style="margin:0 0 18px;color:#666;font-size:13px;">Weekly LLM API alerts — release v{release.get("version")} · {release.get("date")}</p>
  <h2 style="font-size:16px;margin:0 0 10px;">Price, limit &amp; lifecycle changes</h2>
  {table}
  <p style="color:#666;font-size:13px;margin-top:18px;">
    Every value links to a page with the provider's own verbatim quote and access timestamp,
    so you can re-verify without trusting us. Tracking {total_models} models across {total_providers} providers.
  </p>
  <p style="color:#999;font-size:12px;margin-top:22px;">
    You subscribed to weekly alerts at <a href="{BASE_URL}" style="color:#999;">factquire.com</a>.
    {{{{{{RESEND_UNSUBSCRIBE_URL}}}}}}
  </p>
</body></html>"""


def resend_request(path, payload, api_key):
    req = urllib.request.Request(
        f"https://api.resend.com{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test", metavar="EMAIL")
    parser.add_argument("--if-changes", action="store_true")
    args = parser.parse_args(argv)

    changelog = json.loads(CHANGELOG_PATH.read_text(encoding="utf-8"))
    facts = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    release = latest_release(changelog)
    if release is None:
        print("No releases in changelog; nothing to send.")
        return 0

    if args.if_changes:
        entries = release.get("entries", [])
        age = (date.today() - date.fromisoformat(release.get("date"))).days
        if not entries or age > MAX_AGE_DAYS:
            print(f"Skip: latest release {release.get('date')} (age {age}d, {len(entries)} entries) — nothing fresh to send.")
            return 0

    subject = f"FactQuire weekly: {len(release.get('entries', []))} LLM API fact change(s) — v{release.get('version')}"
    html = render_digest(release, len(facts), len({e.get("provider") for e in facts}))

    if args.dry_run:
        PREVIEW_PATH.write_text(html, encoding="utf-8")
        print(f"[dry-run] subject: {subject}")
        print(f"[dry-run] wrote {PREVIEW_PATH.relative_to(ROOT)}")
        return 0

    creds = load_credentials()
    if not creds.get("RESEND_API_KEY"):
        print(f"ERROR: RESEND_API_KEY not found (looked in {KEYSTORE} and environment).", file=sys.stderr)
        return 1

    if args.test:
        result = resend_request(
            "/emails",
            {"from": FROM_ADDR, "to": [args.test], "subject": f"[TEST] {subject}", "html": html.replace("{{{RESEND_UNSUBSCRIBE_URL}}}", "")},
            creds["RESEND_API_KEY"],
        )
        print(f"Test email sent to {args.test}: id {result.get('id')}")
        return 0

    if not creds.get("RESEND_AUDIENCE_ID"):
        print("ERROR: RESEND_AUDIENCE_ID not found.", file=sys.stderr)
        return 1

    broadcast = resend_request(
        "/broadcasts",
        {
            "audience_id": creds["RESEND_AUDIENCE_ID"],
            "from": FROM_ADDR,
            "subject": subject,
            "html": html,
            "name": f"weekly-digest-{release.get('date')}",
        },
        creds["RESEND_API_KEY"],
    )
    resend_request(f"/broadcasts/{broadcast['id']}/send", {}, creds["RESEND_API_KEY"])
    print(f"Broadcast {broadcast['id']} sent ({subject}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
