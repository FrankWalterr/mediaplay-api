from __future__ import annotations
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["__playground__"])

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Mediaplay Playground</title>
  <style>
    body { font-family: ui-sans-serif, system-ui, -apple-system; margin: 24px; }
    button { padding: 8px 12px; margin-right: 8px; }
    pre { background:#111; color:#0f0; padding:12px; border-radius:8px; overflow:auto; }
    input, textarea { width: 480px; max-width: 90vw; padding:8px; margin:6px 0; }
    .row { margin-bottom: 12px; }
  </style>
</head>
<body>
  <h1>Mediaplay – Test Playground</h1>
  <p>Use os botões abaixo para disparar requests contra a API.</p>

  <div class="row">
    <button onclick="hit('/health')">GET /health</button>
    <button onclick="hit('/__debug__/db')">GET /__debug__/db</button>
    <button onclick="hit('/__debug__/smoke')">GET /__debug__/smoke</button>
  </div>

  <h3>Request livre</h3>
  <div class="row">
    <input id="path" placeholder="/users/1" />
  </div>
  <div class="row">
    <textarea id="body" rows="5" placeholder='{"email":"test@example.com"}'></textarea>
  </div>
  <div class="row">
    <input id="token" placeholder="Bearer &lt;token&gt; (opcional)" />
  </div>
  <div class="row">
    <button onclick="custom('GET')">GET</button>
    <button onclick="custom('POST')">POST</button>
    <button onclick="custom('PUT')">PUT</button>
    <button onclick="custom('DELETE')">DELETE</button>
  </div>

  <h3>Resultado</h3>
  <pre id="out"></pre>

<script>
const BASE = window.location.origin;

async function hit(path) {
  const res = await fetch(BASE + path, { method: 'GET' });
  const txt = await res.text();
  document.getElementById('out').textContent = res.status + " " + res.statusText + "\\n\\n" + txt;
}

async function custom(method) {
  const path = document.getElementById('path').value || "/";
  const body = document.getElementById('body').value;
  const token = document.getElementById('token').value;

  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = token;

  const init = { method, headers };
  if (method !== "GET" && method !== "DELETE" && body.trim()) {
    init.body = body;
  }

  const res = await fetch(BASE + path, init);
  const txt = await res.text();
  document.getElementById('out').textContent = res.status + " " + res.statusText + "\\n\\n" + txt;
}
</script>
</body>
</html>
"""

@router.get("/__playground__", response_class=HTMLResponse)
def playground() -> HTMLResponse:
    return HTMLResponse(HTML)
