#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os, json

app = FastAPI(title="Gumroad Tracker")
DB_FILE = os.path.join(os.path.dirname(__file__), "sync_log.json")

def load_stats():
    if not os.path.exists(DB_FILE):
        return {"total_sales": 0, "total_revenue": 0.0, "last_sync": None, "products": {}}
    return json.load(open(DB_FILE))

@app.get("/")
def home():
    return {"status": "Gumroad Tracker", "stats": load_stats()}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    s = load_stats()
    return f"""<html><head><meta charset="utf-8"><title>Gumroad Tracker</title>
<style>body{{font-family:system-ui;background:#0a0a0f;color:#e0e0e0;padding:2rem;max-width:600px;margin:0 auto}}
.card{{background:#12121a;border:1px solid #1f1f2e;border-radius:12px;padding:1.5rem;margin-bottom:1rem}}
h1{{margin:0}} h1 span{{color:#ffd700}}
.stat strong{{display:block;font-size:2.5rem;color:#fff}}
.stats{{display:flex;gap:2rem;margin:1rem 0}}
</style></head><body>
<h1>Gumroad <span>Tracker</span></h1>
<div class="stats">
  <div class="stat"><strong>{s['total_sales']}</strong>Sales</div>
  <div class="stat"><strong>${s['total_revenue']:,.2f}</strong>Revenue</div>
</div>
<div class="card"><p>Last sync: {s['last_sync'] or 'Never'}</p><p>Run <code>python notion_sync.py</code> to sync.</p></div>
</body></html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
