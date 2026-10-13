// Cloudflare Worker: lets the GitHub Pages copy of the dashboard get Claude-written answers.
// The page sends {system, messages}; this Worker adds your Anthropic API key and returns {text}.
//
// Setup (about 5 minutes, free Cloudflare account):
//   1. dash.cloudflare.com → Workers & Pages → Create → Worker → paste this file → Deploy.
//   2. Worker → Settings → Variables and secrets → add a Secret named ANTHROPIC_API_KEY.
//   3. Copy the Worker URL (https://<name>.<account>.workers.dev) into ANALYST_ENDPOINT in index.html.
// The key stays on Cloudflare; it is never sent to the browser.

const ALLOWED_ORIGINS = ["https://nacurobert23-tech.github.io"]; // add http://localhost:8000 for local testing
const MODEL = "claude-sonnet-5-5";
const MAX_INPUT_CHARS = 200000; // the page sends ~100 KB of computed data per question

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "content-type",
      "Vary": "Origin",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST" || !ALLOWED_ORIGINS.includes(origin)) {
      return new Response("Forbidden", { status: 403, headers: cors });
    }

    let body;
    try { body = await request.json(); } catch { return json({ error: "bad_json" }, 400, cors); }
    const { system, messages } = body || {};
    if (typeof system !== "string" || !Array.isArray(messages) || messages.length > 20) {
      return json({ error: "bad_request" }, 400, cors);
    }
    if (JSON.stringify(body).length > MAX_INPUT_CHARS) return json({ error: "too_large" }, 413, cors);

    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({ model: MODEL, max_tokens: 1200, system, messages }),
    });
    if (!r.ok) return json({ error: "upstream", status: r.status }, 502, cors);
    const data = await r.json();
    const text = (data.content || []).filter(c => c.type === "text").map(c => c.text).join("");
    return json({ text }, 200, cors);
  },
};

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status, headers: { ...headers, "content-type": "application/json" } });
}
