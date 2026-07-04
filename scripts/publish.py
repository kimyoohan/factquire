#!/usr/bin/env python3
"""
FactQuire publish tool — one command from data change to live + indexed.

Usage:
  py scripts/publish.py                 # build, commit, push, wait deploy, ping changed URLs
  py scripts/publish.py -m "메시지"      # custom commit message
  py scripts/publish.py --dry-run       # build + show what would be published (no push)
  py scripts/publish.py --skip-build    # site/ already built; just publish
  py scripts/publish.py --full-ping     # ping ALL sitemap URLs instead of changed only

Pipeline:
  1. build   — regenerate site/ from data/facts.json (build_site.py)
  2. diff    — git detects which site/ files actually changed
  3. push    — commit + push to GitHub Pages
  4. verify  — poll live site until deploy is confirmed (content hash check)
  5. ping    — submit only the changed/added URLs to IndexNow
"""

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# Korean Windows console is cp949; force UTF-8 so arrows/dashes never crash prints
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://factquire.com"
SITE_DIR = ROOT / "site"

# site/ file → live URL mapping; files that don't map to indexable pages
NON_PAGE_SUFFIXES = {".css", ".png", ".ico", ".svg", ".jpg", ".webp"}


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", **kw)


def step(msg: str):
    print(f"\n=== {msg} ===")


def build_site():
    step("1/5 Build site")
    r = run([sys.executable, str(ROOT / "scripts" / "build_site.py")])
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit("build_site.py failed — aborting.")
    print(r.stdout.strip())


def changed_site_files() -> list[str]:
    """Paths (relative to repo root) of changed/added files under site/."""
    r = run(["git", "status", "--porcelain", "--", "site/"])
    files = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        status, path = line[:2], line[3:].strip().strip('"')
        if status.strip() in {"D"}:  # deletions have no URL to ping
            continue
        files.append(path)
    return files


def file_to_url(rel_path: str) -> str | None:
    """Map a site/-relative repo path to its live URL, or None if not a page."""
    p = Path(rel_path)
    if p.parts[0] != "site":
        return None
    if p.suffix in NON_PAGE_SUFFIXES:
        return None
    url_path = "/".join(p.parts[1:])
    if url_path == "index.html":
        return f"{BASE_URL}/"
    if url_path.endswith("/index.html"):
        return f"{BASE_URL}/{url_path[: -len('index.html')]}"
    return f"{BASE_URL}/{url_path}"


def git_publish(message: str) -> bool:
    step("3/5 Commit + push")
    run(["git", "add", "-A"])
    r = run(["git", "commit", "-m", message])
    if "nothing to commit" in r.stdout + r.stderr:
        print("Nothing to commit — working tree clean.")
        return False
    print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else "committed")
    r = run(["git", "push"])
    if r.returncode != 0:
        print(r.stderr)
        sys.exit("git push failed — aborting. Fix and rerun with --skip-build.")
    print("Pushed to origin.")
    return True


def rerun_failed_pages_run():
    """GitHub Pages deploys fail transiently; rerun the latest run if it failed."""
    r = run(["gh", "run", "list", "--limit", "1", "--json", "databaseId,conclusion"])
    try:
        runs = json.loads(r.stdout)
        if runs and runs[0].get("conclusion") == "failure":
            run_id = str(runs[0]["databaseId"])
            print(f"  Pages run {run_id} failed (transient) - rerunning...")
            run(["gh", "run", "rerun", run_id])
            return True
    except (json.JSONDecodeError, KeyError, IndexError):
        pass
    return False


def wait_deploy(probe_url: str, expect_local: Path, timeout_s: int = 420) -> bool:
    """Poll live URL until it matches the local file (deploy landed)."""
    step("4/5 Wait for GitHub Pages deploy")
    expected = expect_local.read_bytes()
    deadline = time.time() + timeout_s
    attempt = 0
    rerun_done = False
    while time.time() < deadline:
        attempt += 1
        if attempt > 4 and not rerun_done:
            rerun_done = rerun_failed_pages_run()
        try:
            # Cloudflare 403s the default Python-urllib User-Agent
            req = urllib.request.Request(
                probe_url,
                headers={"Cache-Control": "no-cache", "User-Agent": "FactQuire-publish/1.0"},
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                live = resp.read()
            if live == expected:
                print(f"Deploy confirmed after {attempt} check(s): {probe_url}")
                return True
        except Exception as e:
            print(f"  probe error ({e}); retrying...")
        time.sleep(15)
    print(f"WARNING: deploy not confirmed within {timeout_s}s. IndexNow ping skipped.")
    print("Run later:  py scripts/indexnow.py --new")
    return False


def ping_indexnow(urls: list[str] | None):
    """urls=None → full sitemap ping via indexnow.py; else ping the given list."""
    step("5/5 IndexNow ping")
    script = str(ROOT / "scripts" / "indexnow.py")
    if urls is not None and urls:
        r = run([sys.executable, script] + urls)
        print((r.stdout + r.stderr).strip())
        if r.returncode != 0:
            print("WARNING: IndexNow ping failed. Retry:  py scripts/indexnow.py --new")
    elif urls is None:
        r = run([sys.executable, script])
        print((r.stdout + r.stderr).strip())
    # Catch pages committed before this run (e.g. by a Codex task): never-submitted URLs
    r = run([sys.executable, script, "--new"])
    out = (r.stdout + r.stderr).strip()
    if "Nothing new" not in out:
        print(out)


def main():
    parser = argparse.ArgumentParser(description="Build, deploy, and index factquire.com in one command")
    parser.add_argument("-m", "--message", default=None, help="Commit message")
    parser.add_argument("--dry-run", action="store_true", help="Build + diff only; no commit/push/ping")
    parser.add_argument("--skip-build", action="store_true", help="Skip build_site.py step")
    parser.add_argument("--full-ping", action="store_true", help="Ping entire sitemap instead of changed URLs")
    args = parser.parse_args()

    if not args.skip_build:
        build_site()
    else:
        step("1/5 Build site (skipped)")

    step("2/5 Detect changes")
    changed = changed_site_files()
    urls = sorted({u for f in changed if (u := file_to_url(f))})
    print(f"{len(changed)} site file(s) changed → {len(urls)} indexable URL(s)")
    for u in urls[:10]:
        print(f"  {u}")
    if len(urls) > 10:
        print(f"  ... and {len(urls) - 10} more")

    if args.dry_run:
        print("\n[DRY RUN] Stopping before commit/push/ping.")
        return

    n_models = "?"
    feed = SITE_DIR / "feed.json"
    if feed.exists():
        try:
            n_models = len(json.loads(feed.read_text(encoding="utf-8")).get("models", []))
        except Exception:
            pass
    message = args.message or f"Publish: {len(urls)} page(s) updated ({n_models} models)"

    pushed = git_publish(message)
    if not pushed and not urls:
        print("\nNothing published. Done.")
        return

    # Probe with a small always-regenerated file; fall back to homepage
    probe_rel = "feed.json" if feed.exists() else "index.html"
    ok = wait_deploy(f"{BASE_URL}/{probe_rel}", SITE_DIR / probe_rel)
    if ok:
        ping_indexnow(None if args.full_ping else urls)

    print("\nPublish complete.")


if __name__ == "__main__":
    main()
