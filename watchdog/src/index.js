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

// ---------------------------------------------------------------------------
// Free model watchlist: registration endpoint + daily personalized alerts.
// Lives in this Worker (not the Pages project) so registration, the model
// snapshot, and the daily cron all share one KV binding in one runtime.
// ---------------------------------------------------------------------------

const ALLOWED_ORIGINS = new Set(["https://factquire.com", "https://www.factquire.com"]);
const MAX_MODELS = 3;
const MODEL_KEY_RE = /^[a-z0-9._-]+\/[A-Za-z0-9./:_-]{1,80}$/;
const WATCHED_FIELDS = [
  ["pricing.input_per_mtok", "Input price /1M", (m) => m.pricing && m.pricing.input_per_mtok],
  ["pricing.output_per_mtok", "Output price /1M", (m) => m.pricing && m.pricing.output_per_mtok],
  ["pricing.cached_input_per_mtok", "Cached input /1M", (m) => m.pricing && m.pricing.cached_input_per_mtok],
  ["context_window_tokens", "Context window", (m) => m.context_window_tokens],
  ["max_output_tokens", "Max output", (m) => m.max_output_tokens],
  ["status", "Status", (m) => m.status],
  ["deprecation_date", "Deprecation date", (m) => m.deprecation_date],
];

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.has(origin) ? origin : "https://factquire.com";
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };
}

function jsonReply(origin, status, body) {
  return new Response(JSON.stringify(body), { status, headers: corsHeaders(origin) });
}

async function handleWatchlistPost(request, env) {
  const origin = request.headers.get("Origin") || "";
  let payload;
  try {
    payload = await request.json();
  } catch {
    return jsonReply(origin, 400, { error: "Invalid request." });
  }
  if (payload.website) return jsonReply(origin, 200, { ok: true }); // honeypot

  const email = String(payload.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) {
    return jsonReply(origin, 400, { error: "Please enter a valid email address." });
  }
  const models = Array.isArray(payload.models)
    ? [...new Set(payload.models.map((m) => String(m).trim()))].filter((m) => MODEL_KEY_RE.test(m)).slice(0, MAX_MODELS)
    : [];
  if (!models.length) return jsonReply(origin, 400, { error: "Pick at least one model to watch." });

  const volumes = {};
  if (payload.volumes && typeof payload.volumes === "object") {
    for (const key of models) {
      const v = payload.volumes[key];
      if (v && typeof v === "object") {
        const inM = Number(v.inputMTok);
        const outM = Number(v.outputMTok);
        if (Number.isFinite(inM) && inM >= 0 && inM < 1e6 && Number.isFinite(outM) && outM >= 0 && outM < 1e6 && (inM || outM)) {
          volumes[key] = { inputMTok: inM, outputMTok: outM };
        }
      }
    }
  }

  await env.STATE.put(`watch:${email}`, JSON.stringify({ email, models, volumes, updatedAt: new Date().toISOString() }));

  if (env.RESEND_API_KEY && env.RESEND_AUDIENCE_ID) {
    await fetch(`https://api.resend.com/audiences/${env.RESEND_AUDIENCE_ID}/contacts`, {
      method: "POST",
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json", "User-Agent": UA },
      body: JSON.stringify({ email, unsubscribed: false }),
    }).catch(() => {});
  }
  return jsonReply(origin, 200, { ok: true, watching: models });
}

function modelSummary(model) {
  const out = {};
  for (const [key, , getter] of WATCHED_FIELDS) out[key] = getter(model) ?? null;
  return out;
}

function diffModel(prev, curr) {
  const changes = [];
  for (const [key, label] of WATCHED_FIELDS) {
    const before = prev ? prev[key] : undefined;
    const after = curr[key];
    if (before !== undefined && String(before) !== String(after)) {
      changes.push({ field: key, label, before, after });
    }
  }
  return changes;
}

function estimateMonthlyCost(model, volume) {
  if (!volume || !model.pricing) return null;
  const inP = model.pricing.input_per_mtok;
  const outP = model.pricing.output_per_mtok;
  if (inP == null || outP == null) return null;
  return volume.inputMTok * inP + volume.outputMTok * outP;
}

async function runDaily(env) {
  let feedRes = await fetch(FEED_URL, { headers: { "User-Agent": UA } });
  if (!feedRes.ok) feedRes = await fetch(FEED_FALLBACK, { headers: { "User-Agent": UA } });
  if (!feedRes.ok) return { error: `feed fetch HTTP ${feedRes.status}` };
  const feed = await feedRes.json();

  const current = {};
  for (const m of feed.models || []) current[`${m.provider}/${m.model_id}`] = m;

  const prevSnapshot = (await env.STATE.get("snapshot:models", "json")) || {};
  const changedModels = {};
  for (const [key, model] of Object.entries(current)) {
    const changes = diffModel(prevSnapshot[key], modelSummary(model));
    if (prevSnapshot[key] && changes.length) changedModels[key] = changes;
  }

  const emailed = [];
  if (Object.keys(changedModels).length) {
    const watchers = await env.STATE.list({ prefix: "watch:" });
    for (const k of watchers.keys) {
      const entry = await env.STATE.get(k.name, "json");
      if (!entry) continue;
      const hits = (entry.models || []).filter((m) => changedModels[m]);
      if (!hits.length) continue;

      const sections = hits.map((m) => {
        const rows = changedModels[m]
          .map((c) => `<li>${c.label}: <s>${c.before ?? "—"}</s> → <b>${c.after ?? "—"}</b></li>`)
          .join("");
        const cost = estimateMonthlyCost(current[m], (entry.volumes || {})[m]);
        const costLine = cost != null ? `<p style="margin:4px 0;color:#444;">Your est. monthly cost for this model: <b>$${cost.toFixed(2)}</b></p>` : "";
        const safe = m.replace(/[^a-zA-Z0-9_/-]/g, "_").replace("/", "/");
        return `<h3 style="margin:14px 0 4px;font-size:15px;">${m}</h3><ul style="margin:4px 0;">${rows}</ul>${costLine}
<p style="margin:4px 0;font-size:13px;"><a href="https://factquire.com/models/${m.split("/")[0]}/${encodeURIComponent(m.split("/").slice(1).join("/").replace(/[^a-zA-Z0-9_-]/g, "_"))}.html">source-verified details →</a></p>`;
      });

      const html = `<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#1c1c1c;">
<p style="margin:0 0 4px;"><a href="https://factquire.com" style="color:#1c1c1c;font-weight:700;font-size:17px;text-decoration:none;">FactQuire</a> — watchlist alert</p>
<p style="margin:0 0 12px;color:#666;font-size:13px;">A model you watch changed. Every value below is verified against the provider's own page.</p>
${sections.join("")}
<p style="color:#999;font-size:12px;margin-top:20px;">You watch ${entry.models.length} model(s) at factquire.com. Reply to change or stop.</p></div>`;

      await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json", "User-Agent": UA },
        body: JSON.stringify({
          from: "FactQuire Alerts <alerts@notify.factquire.com>",
          to: [entry.email],
          subject: `[FactQuire] ${hits.join(", ")} changed`,
          html,
        }),
      });
      emailed.push({ email: entry.email, models: hits });
    }
  }

  const newSnapshot = {};
  for (const [key, model] of Object.entries(current)) newSnapshot[key] = modelSummary(model);
  await env.STATE.put("snapshot:models", JSON.stringify(newSnapshot));

  return { models: Object.keys(current).length, changed: changedModels, emailed };
}

export default {
  async scheduled(event, env, ctx) {
    if (event.cron === "30 22 * * *") ctx.waitUntil(runDaily(env));
    else ctx.waitUntil(runBatch(env));
  },
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/watchlist" && request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(request.headers.get("Origin") || "") });
    }
    if (url.pathname === "/watchlist" && request.method === "POST") {
      return handleWatchlistPost(request, env);
    }
    if (url.pathname === "/run" && env.RUN_KEY && url.searchParams.get("key") === env.RUN_KEY) {
      const result = url.searchParams.get("daily") === "1" ? await runDaily(env) : await runBatch(env);
      return new Response(JSON.stringify(result, null, 1), { headers: { "Content-Type": "application/json" } });
    }
    return new Response("factquire-watchdog", { status: 200 });
  },
};
