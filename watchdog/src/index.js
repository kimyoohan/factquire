// FactQuire watchdog — daily change detection with NO AI.
//
// Every 4 hours (cron) it takes the next batch of source URLs cited in the
// public feed and re-fetches each page. For every model fact sourced from that
// page it checks whether the stored verbatim quote segments still appear in
// the page text.
//
//   segment found -> fact still backed by the live page (state "found")
//   segment never seen since baseline -> page is JS-rendered for this quote,
//     mark "invisible" once and stay silent (raw fetch can't verify it)
//   segment WAS found before and now missing -> the page changed under the
//     fact: price change, restructure, or removal -> ALERT (email to admin,
//     flag stored in KV for the weekly AI run to pick up)
//
// This never edits facts on its own — it only detects and flags. Interpretation
// stays with the AI pipeline, so a silent regex mis-parse can never ship.

// raw.githubusercontent bypasses our own Cloudflare proxy (same-account Worker
// subrequests to factquire.com intermittently fail with error 1042)
const FEED_URL = "https://raw.githubusercontent.com/kimyoohan/factquire/main/site/feed.json";
const FEED_FALLBACK = "https://factquire.com/feed.json";
const BATCH_SIZE = 25;
const ALERT_TO = "azij@naver.com";
const ALERT_FROM = "FactQuire Watchdog <alerts@notify.factquire.com>";
const UA = "FactQuireWatchdog/1.0 (+https://factquire.com; daily source re-verification)";
const MIN_SEGMENT_LEN = 12;

function normalize(text) {
  return text
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&#x27;|&#39;|&rsquo;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&nbsp;/g, " ")
    .replace(/[‘’]/g, "'")
    .replace(/[“”]/g, '"')
    .replace(/\s+/g, " ")
    .trim();
}

function segmentsOf(quote) {
  return normalize(quote)
    .split("...")
    .map((s) => s.trim())
    .filter((s) => s.length >= MIN_SEGMENT_LEN);
}

async function fnv1a(text) {
  // tiny non-crypto hash for page snapshots
  let hash = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
  }
  return (hash >>> 0).toString(16);
}

function buildWatchlist(feed) {
  // url -> [{model, segments:[...]}]
  const map = new Map();
  for (const model of feed.models || []) {
    for (const source of model.sources || []) {
      if (!map.has(source.url)) map.set(source.url, []);
      const segs = segmentsOf(source.quote || "");
      if (segs.length) {
        map.get(source.url).push({ model: `${model.provider}/${model.model_id}`, segments: segs });
      }
    }
  }
  return [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

async function checkUrl(url, expectations, env) {
  const stateKey = `url:${url}`;
  const prev = (await env.STATE.get(stateKey, "json")) || { seg: {}, hash: null };
  const next = { seg: {}, hash: prev.hash, checkedAt: new Date().toISOString() };
  const alerts = [];

  let pageText = null;
  try {
    const res = await fetch(url, { headers: { "User-Agent": UA }, redirect: "follow" });
    if (res.ok) pageText = normalize(await res.text());
    else alerts.push({ url, kind: "fetch", detail: `HTTP ${res.status}` });
  } catch (err) {
    alerts.push({ url, kind: "fetch", detail: String(err).slice(0, 120) });
  }

  if (pageText === null) {
    // Keep previous segment states on fetch failure. Alert ONLY on a good->bad
    // transition; a host that has never succeeded from the CF edge (bot-blocked,
    // e.g. OpenAI/Groq 403) is baselined silently — those pages stay covered by
    // the local weekly AI verification instead.
    next.seg = prev.seg;
    next.fetchFailed = true;
    await env.STATE.put(stateKey, JSON.stringify(next));
    return prev.fetchFailed === false ? alerts : [];
  }
  next.fetchFailed = false;
  next.hash = await fnv1a(pageText);

  for (const { model, segments } of expectations) {
    for (let i = 0; i < segments.length; i++) {
      const segKey = `${model}#${i}`;
      const found = pageText.includes(segments[i]);
      const prevState = prev.seg[segKey];
      if (found) {
        next.seg[segKey] = "found";
      } else if (prevState === "found") {
        next.seg[segKey] = "missing";
        alerts.push({ url, kind: "fact", model, detail: `quote segment no longer on page: "${segments[i].slice(0, 80)}"` });
      } else if (prevState === "missing" || prevState === "invisible") {
        next.seg[segKey] = prevState; // already known — stay silent
      } else {
        next.seg[segKey] = "invisible"; // baseline: raw fetch never saw it (JS-rendered) — silent
      }
    }
  }

  await env.STATE.put(stateKey, JSON.stringify(next));
  return alerts;
}

async function sendAlertEmail(alerts, env) {
  const rows = alerts
    .map((a) => `<li><b>${a.kind === "fact" ? a.model : "page"}</b> — ${a.detail}<br><a href="${a.url}">${a.url}</a></li>`)
    .join("");
  const html = `<p>FactQuire watchdog detected ${alerts.length} change(s) needing AI review:</p><ul>${rows}</ul>
<p>Next step: run the update/verify pipeline for the affected providers, then publish.</p>`;
  await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json", "User-Agent": UA },
    body: JSON.stringify({
      from: ALERT_FROM,
      to: [ALERT_TO],
      subject: `[FactQuire watchdog] ${alerts.length} source change(s) detected`,
      html,
    }),
  });
}

async function runBatch(env) {
  let feedRes = await fetch(FEED_URL, { headers: { "User-Agent": UA } });
  if (!feedRes.ok) feedRes = await fetch(FEED_FALLBACK, { headers: { "User-Agent": UA } });
  if (!feedRes.ok) return { error: `feed fetch HTTP ${feedRes.status}` };
  const watchlist = buildWatchlist(await feedRes.json());

  const cursor = parseInt((await env.STATE.get("cursor")) || "0", 10) % Math.max(watchlist.length, 1);
  const batch = [];
  for (let i = 0; i < Math.min(BATCH_SIZE, watchlist.length); i++) {
    batch.push(watchlist[(cursor + i) % watchlist.length]);
  }
  await env.STATE.put("cursor", String((cursor + batch.length) % watchlist.length));

  const alerts = [];
  for (const [url, expectations] of batch) {
    alerts.push(...(await checkUrl(url, expectations, env)));
  }

  if (alerts.length) {
    await env.STATE.put(`alerts:${new Date().toISOString()}`, JSON.stringify(alerts), { expirationTtl: 60 * 60 * 24 * 30 });
    if (env.RESEND_API_KEY) await sendAlertEmail(alerts, env);
  }
  return { checked: batch.length, from: cursor, total: watchlist.length, alerts };
}

export default {
  async scheduled(_event, env, ctx) {
    ctx.waitUntil(runBatch(env));
  },
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/run" && env.RUN_KEY && url.searchParams.get("key") === env.RUN_KEY) {
      const result = await runBatch(env);
      return new Response(JSON.stringify(result, null, 1), { headers: { "Content-Type": "application/json" } });
    }
    return new Response("factquire-watchdog", { status: 200 });
  },
};
