#!/usr/bin/env python3
"""Ghost Systems Backend — Vapi Webhook Handler + Appointment API"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3, os, json, uuid

DB = os.path.join(os.path.dirname(__file__), "ghost.db")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id TEXT PRIMARY KEY,
        customer_name TEXT, phone TEXT, address TEXT,
        service_type TEXT, property_type TEXT, urgency TEXT,
        preferred_date TEXT, notes TEXT,
        status TEXT DEFAULT 'booked',
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS calls (
        id TEXT PRIMARY KEY,
        caller_number TEXT, duration_seconds INTEGER,
        transcript TEXT, outcome TEXT, created_at TEXT
    )''')
    conn.commit(); conn.close()

init_db()
app = FastAPI(title="Ghost Systems API")

class AppointmentIn(BaseModel):
    customer_name: str
    phone: str
    address: str
    service_type: str
    property_type: str
    urgency: str
    preferred_date: Optional[str] = None
    notes: Optional[str] = None

@app.post("/webhook/vapi")
async def vapi_webhook(request: Request):
    body = await request.json()
    message = body.get("message", {})
    msg_type = message.get("type")
    
    if msg_type == "function-call":
        call = message.get("functionCall", {})
        fn_name = call.get("name")
        params = call.get("parameters", {})
        
        if fn_name == "bookAppointment":
            aid = str(uuid.uuid4())[:8].upper()
            conn = sqlite3.connect(DB)
            conn.execute("""INSERT INTO appointments
                (id, customer_name, phone, address, service_type, property_type, urgency, preferred_date, notes, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (aid, params.get("customerName"), params.get("phone"), params.get("address"),
                 params.get("serviceType"), params.get("propertyType"), params.get("urgency"),
                 params.get("preferredDate"), params.get("notes"), datetime.utcnow().isoformat()))
            conn.commit(); conn.close()
            return {"result": "booked", "appointmentId": aid}
        
        elif fn_name == "sendTextSummary":
            return {"result": "sms_queued", "to": params.get("technicianPhone")}
        
        elif fn_name == "checkAvailability":
            return {"result": "available_slots", "slots": [
                "Today 2:00 PM", "Today 4:00 PM", "Tomorrow 9:00 AM"
            ]}
    
    elif msg_type == "end-of-call-report":
        cid = str(uuid.uuid4())[:8].upper()
        call_info = message.get("call", {})
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO calls (id, caller_number, duration_seconds, transcript, outcome, created_at) VALUES (?,?,?,?,?,?)",
            (cid, call_info.get("customer",{}).get("number"),
             call_info.get("durationSeconds"),
             json.dumps(call_info.get("transcript",[])),
             call_info.get("status"),
             datetime.utcnow().isoformat()))
        conn.commit(); conn.close()
        return {"result": "logged"}
    
    return {"result": "ignored"}

@app.get("/appointments")
def list_appointments(status: Optional[str] = None):
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    if status:
        rows = conn.execute("SELECT * FROM appointments WHERE status = ? ORDER BY created_at DESC", (status,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM appointments ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/appointments/{aid}")
def get_appointment(aid: str):
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM appointments WHERE id = ?", (aid,)).fetchone()
    conn.close()
    if not row: return JSONResponse({"error": "not found"}, 404)
    return dict(row)

@app.patch("/appointments/{aid}/status")
def update_status(aid: str, status: str):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, aid))
    conn.commit(); conn.close()
    return {"id": aid, "status": status}

@app.get("/calls")
def list_calls():
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM calls ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/", response_class=HTMLResponse)
def dashboard():
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    appts = conn.execute("SELECT COUNT(*) as c FROM appointments").fetchone()["c"]
    calls = conn.execute("SELECT COUNT(*) as c FROM calls").fetchone()["c"]
    recent = conn.execute("SELECT * FROM appointments ORDER BY created_at DESC LIMIT 5").fetchall()
    conn.close()
    rows = "".join(f"<tr><td>{r['id']}</td><td>{r['customer_name']}</td><td>{r['service_type']}</td><td>{r['urgency']}</td><td><span class='badge'>{r['status']}</span></td></tr>" for r in recent)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Ghost Systems Dashboard</title>
<style>
body{{font-family:system-ui;background:#0a0a0f;color:#e0e0e0;padding:2rem;max-width:900px;margin:0 auto}}
.card{{background:#12121a;border:1px solid #1f1f2e;border-radius:12px;padding:1.5rem;margin-bottom:1rem}}
h1{{margin:0}} h1 span{{color:#00f0ff}}
.stats{{display:flex;gap:2rem;margin:1rem 0}}
.stat strong{{display:block;font-size:2rem;color:#fff}}
table{{width:100%;border-collapse:collapse;margin-top:1rem;font-size:.9rem}}
th{{text-align:left;color:#888;padding:.5rem}} td{{padding:.5rem;border-top:1px solid #1f1f2e}}
.badge{{background:#00ff88;color:#000;padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:700}}
</style></head>
<body>
<h1>Ghost <span>Systems</span></h1>
<p style="color:#888">Live appointment dashboard</p>
<div class="stats">
  <div class="stat"><strong>{appts}</strong>Appointments</div>
  <div class="stat"><strong>{calls}</strong>Calls</div>
</div>
<div class="card">
  <h3>Recent Appointments</h3>
  <table><tr><th>ID</th><th>Customer</th><th>Service</th><th>Urgency</th><th>Status</th></tr>{rows}</table>
</div>
<p style="color:#666;font-size:.8rem">API: POST /webhook/vapi | GET /appointments | GET /calls</p>
</body></html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
