#!/usr/bin/env python3
"""Dubai Voice Agent Backend — Trilingual Concierge API"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import sqlite3, os, json, uuid

DB = os.path.join(os.path.dirname(__file__), "dubai.db")

def init():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS viewings (
        id TEXT PRIMARY KEY, customer_name TEXT, phone TEXT,
        nationality TEXT, budget_aed TEXT, property_type TEXT,
        area TEXT, preferred_date TEXT, notes TEXT,
        status TEXT DEFAULT 'booked', created_at TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS calls (
        id TEXT PRIMARY KEY, caller_number TEXT, duration_seconds INTEGER,
        language TEXT, transcript TEXT, outcome TEXT, created_at TEXT
    )''')
    conn.commit(); conn.close()
init()

app = FastAPI(title="Dubai Voice Agent API")

@app.post("/webhook/vapi")
async def vapi_webhook(request: Request):
    body = await request.json()
    msg = body.get("message", {})
    if msg.get("type") == "function-call":
        call = msg.get("functionCall", {})
        fn = call.get("name")
        p = call.get("parameters", {})
        if fn == "bookViewing":
            vid = str(uuid.uuid4())[:8].upper()
            conn = sqlite3.connect(DB)
            conn.execute("INSERT INTO viewings VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (vid, p.get("customerName"), p.get("phone"), p.get("nationality"),
                 p.get("budgetAED"), p.get("propertyType"), p.get("area"),
                 p.get("preferredDate"), p.get("notes"), "booked", datetime.utcnow().isoformat()))
            conn.commit(); conn.close()
            return {"result": "viewing_booked", "id": vid}
        if fn == "sendWhatsAppSummary":
            return {"result": "whatsapp_queued", "to": p.get("brokerNumber")}
        if fn == "escalateToHuman":
            return {"result": "escalated", "priority": p.get("priority", "standard")}
    return {"result": "ignored"}

@app.get("/viewings")
def list_viewings():
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM viewings ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/", response_class=HTMLResponse)
def dashboard():
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    v = conn.execute("SELECT COUNT(*) as c FROM viewings").fetchone()["c"]
    c = conn.execute("SELECT COUNT(*) as c FROM calls").fetchone()["c"]
    recent = conn.execute("SELECT * FROM viewings ORDER BY created_at DESC LIMIT 5").fetchall()
    conn.close()
    rows = "".join(f"<tr><td>{r['id']}</td><td>{r['customer_name']}</td><td>{r['area']}</td><td>{r['budget_aed']}</td><td>{r['status']}</td></tr>" for r in recent)
    return f"""<html><head><meta charset="utf-8"><title>Dubai Voice Agent</title>
<style>body{{font-family:system-ui;background:#0a0a0f;color:#e0e0e0;padding:2rem;max-width:900px;margin:0 auto}}
.card{{background:#12121a;border:1px solid #1f1f2e;border-radius:12px;padding:1.5rem;margin-bottom:1rem}}
h1{{margin:0}} h1 span{{color:#ffd700}}
.stats{{display:flex;gap:2rem;margin:1rem 0}}
.stat strong{{display:block;font-size:2rem;color:#fff}}
table{{width:100%;border-collapse:collapse;margin-top:1rem;font-size:.9rem}}
th{{text-align:left;color:#888;padding:.5rem}} td{{padding:.5rem;border-top:1px solid #1f1f2e}}
</style></head><body>
<h1>Dubai <span>Voice Agent</span></h1><p style="color:#888">Luxury real estate concierge — EN / AR / HI</p>
<div class="stats"><div class="stat"><strong>{v}</strong>Viewings</div><div class="stat"><strong>{c}</strong>Calls</div></div>
<div class="card"><h3>Recent Viewings</h3><table><tr><th>ID</th><th>Customer</th><th>Area</th><th>Budget (AED)</th><th>Status</th></tr>{rows}</table></div>
</body></html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
