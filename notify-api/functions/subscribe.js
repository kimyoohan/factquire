// POST /subscribe — adds an email to the FactQuire weekly-alerts audience (Resend).
// Env vars (set on the Cloudflare Pages project, never in code):
//   RESEND_API_KEY     — Resend secret key
//   RESEND_AUDIENCE_ID — Resend audience UUID
const ALLOWED_ORIGINS = new Set([
  "https://factquire.com",
  "https://www.factquire.com",
]);

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.has(origin) ? origin : "https://factquire.com";
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };
}

function reply(origin, status, body) {
  return new Response(JSON.stringify(body), { status, headers: corsHeaders(origin) });
}

export async function onRequestOptions(context) {
  return new Response(null, { status: 204, headers: corsHeaders(context.request.headers.get("Origin") || "") });
}

export async function onRequestPost(context) {
  const origin = context.request.headers.get("Origin") || "";
  const { env } = context;

  if (!env.RESEND_API_KEY || !env.RESEND_AUDIENCE_ID) {
    return reply(origin, 503, { error: "Subscriptions are not open yet — please try again soon." });
  }

  let payload;
  try {
    payload = await context.request.json();
  } catch {
    return reply(origin, 400, { error: "Invalid request." });
  }

  // Honeypot: real users never fill this hidden field.
  if (payload.website) {
    return reply(origin, 200, { ok: true });
  }

  const email = String(payload.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) {
    return reply(origin, 400, { error: "Please enter a valid email address." });
  }

  const res = await fetch(`https://api.resend.com/audiences/${env.RESEND_AUDIENCE_ID}/contacts`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, unsubscribed: false }),
  });

  if (res.ok || res.status === 409) {
    return reply(origin, 200, { ok: true });
  }
  console.log("resend error", res.status, await res.text());
  return reply(origin, 502, { error: "Could not subscribe right now — please try again later." });
}
