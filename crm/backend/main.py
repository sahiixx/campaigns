#!/usr/bin/env python3
"""Unified CRM — Aggregates leads from all campaigns."""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3, os, glob, csv, uuid
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), "crm.db")
app = FastAPI(title="Campaign CRM")

def init():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS leads (
        id TEXT PRIMARY KEY, campaign TEXT, company_name TEXT,
        contact_first TEXT, phone TEXT, address TEXT, city TEXT,
        pain_score INTEGER, status TEXT DEFAULT 'new', notes TEXT,
        last_contact TEXT, created_at TEXT
    )''')
    conn.commit(); conn.close()

init()

def sync_leads():
    conn = sqlite3.connect(DB)
    imported = 0
    for csvf in glob.glob("../../*/leads/*.csv"):
        campaign = csvf.split("/")[-3]
        with open(csvf) as f:
            for row in csv.DictReader(f):
                lead_id = row.get("id", str(uuid.uuid4())[:8].upper())
                # skip duplicates
                exists = conn.execute("SELECT 1 FROM leads WHERE id = ?", (lead_id,)).fetchone()
                if not exists:
                    conn.execute("INSERT INTO leads VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        (lead_id, campaign, row.get("company_name",""), row.get("contact_first",""),
                         row.get("phone",""), row.get("address",""), row.get("city",""),
                         int(row.get("pain_score",0)), "new", "", None, datetime.utcnow().isoformat()))
                    imported += 1
    conn.commit(); conn.close()
    return imported

@app.post("/sync")
def do_sync():
    n = sync_leads()
    return {"imported": n}

@app.get("/leads")
def list_leads(campaign: str = None, status: str = None):
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    query = "SELECT * FROM leads WHERE 1=1"
    params = []
    if campaign:
        query += " AND campaign = ?"; params.append(campaign)
    if status:
        query += " AND status = ?"; params.append(status)
    query += " ORDER BY pain_score DESC, created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.patch("/leads/{lid}/status")
def update_status(lid: str, status: str):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE leads SET status = ?, last_contact = ? WHERE id = ?",
        (status, datetime.utcnow().isoformat(), lid))
    conn.commit(); conn.close()
    return {"id": lid, "status": status}

@app.get("/stats")
def stats():
    conn = sqlite3.connect(DB)
    total = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    by_campaign = conn.execute("SELECT campaign, COUNT(*) FROM leads GROUP BY campaign").fetchall()
    by_status = conn.execute("SELECT status, COUNT(*) FROM leads GROUP BY status").fetchall()
    high_pain = conn.execute("SELECT COUNT(*) FROM leads WHERE pain_score >= 2").fetchone()[0]
    conn.close()
    return {"total": total, "high_pain": high_pain, "by_campaign": dict(by_campaign), "by_status": dict(by_status)}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    s = stats()
    rows = ""
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    for r in conn.execute("SELECT * FROM leads ORDER BY pain_score DESC LIMIT 10").fetchall():
        rows += f"<tr><td>{r['id']}</td><td>{r['campaign']}</td><td>{r['company_name']}</td><td>{r['city']}</td><td>{r['pain_score']}</td><td><span class='badge'>{r['status']}</span></td></tr>"
    conn.close()
    return f"""<html><head><meta charset="utf-8"><title>Campaign CRM</title>
<style>body{{font-family:system-ui;background:#0a0a0f;color:#e0e0e0;padding:2rem;max-width:900px;margin:0 auto}}
.card{{background:#12121a;border:1px solid #1f1f2e;border-radius:12px;padding:1.5rem;margin-bottom:1rem}}
h1{{margin:0}} h1 span{{color:#00f0ff}}
.stats{{display:flex;gap:2rem;margin:1rem 0}}
.stat strong{{display:block;font-size:2rem;color:#fff}}
table{{width:100%;border-collapse:collapse;margin-top:1rem;font-size:.9rem}}
th{{text-align:left;color:#888;padding:.5rem}} td{{padding:.5rem;border-top:1px solid #1f1f2e}}
.badge{{background:#00ff88;color:#000;padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:700}}
</style></head><body>
<h1>Campaign <span>CRM</span></h1>
<div class="stats">
  <div class="stat"><strong>{s['total']}</strong>Total Leads</div>
  <div class="stat"><strong>{s['high_pain']}</strong>High Pain</div>
</div>
<div class="card"><h3>Top Leads</h3><table><tr><th>ID</th><th>Campaign</th><th>Company</th><th>City</th><th>Pain</th><th>Status</th></tr>{rows}</table></div>
<p style="color:#666;font-size:.8rem">API: GET /leads | PATCH /leads/{{id}}/status | POST /sync</p>
</body></html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
