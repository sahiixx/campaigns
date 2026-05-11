#!/usr/bin/env python3
"""Ghost Systems — Live Email Sender
Reads outbox/*.md and sends via SMTP. Tracks state in sent.db to avoid duplicates.
Usage:
  export SMTP_HOST=smtp.sendgrid.net
  export SMTP_PORT=587
  export SMTP_USER=apikey
  export SMTP_PASS=SG.xxx
  export FROM_EMAIL=sahil@ghostsystems.io
  python send_live.py --dry-run   # preview only
  python send_live.py --live      # actually send
"""
import os, sys, sqlite3, glob, re, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime

DB = Path(__file__).with_suffix('.db')

def init():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS sent (
        id TEXT PRIMARY KEY, to_email TEXT, subject TEXT,
        sent_at TEXT, status TEXT, error TEXT
    )''')
    conn.commit(); conn.close()

def already_sent(email_id: str) -> bool:
    conn = sqlite3.connect(DB)
    row = conn.execute("SELECT 1 FROM sent WHERE id = ?", (email_id,)).fetchone()
    conn.close()
    return row is not None

def mark_sent(email_id, to_email, subject, status="sent", error=None):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT OR REPLACE INTO sent (id, to_email, subject, sent_at, status, error) VALUES (?,?,?,?,?,?)",
        (email_id, to_email, subject, datetime.utcnow().isoformat(), status, error))
    conn.commit(); conn.close()

def extract_subject(body: str) -> str:
    m = re.search(r"Subject:\s*(.+)", body)
    if m: return m.group(1).strip()
    m = re.search(r"`(.+?)`", body)
    if m: return m.group(1).strip()
    return "Quick question about missed calls"

def extract_to(email_id: str, body: str) -> str:
    # Derive fake email for demo; in production, leads CSV would have real emails
    fake = email_id.split("_")[0].lower().replace("hvac-", "") + "@example.com"
    return fake

def send_one(smtp, from_addr, email_id, body, dry=True):
    to_addr = extract_to(email_id, body)
    subject = extract_subject(body)
    
    if already_sent(email_id):
        print(f"  SKIP {email_id} — already sent")
        return
    
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    if dry:
        print(f"  [DRY] {email_id:20} → {to_addr:30} | {subject[:50]}")
        mark_sent(email_id, to_addr, subject, status="dry_run")
        return
    
    try:
        smtp.sendmail(from_addr, [to_addr], msg.as_string())
        print(f"  [SENT] {email_id:20} → {to_addr}")
        mark_sent(email_id, to_addr, subject, status="sent")
    except Exception as e:
        print(f"  [FAIL] {email_id:20} → {to_addr} | {e}")
        mark_sent(email_id, to_addr, subject, status="failed", error=str(e))

def main():
    dry = "--live" not in sys.argv
    init()
    
    host = os.getenv("SMTP_HOST", "localhost")
    port = int(os.getenv("SMTP_PORT", "1025"))
    user = os.getenv("SMTP_USER", "")
    pw = os.getenv("SMTP_PASS", "")
    from_addr = os.getenv("FROM_EMAIL", "sahil@ghostsystems.io")
    
    files = sorted(glob.glob("outbox/*/*_email.md"))
    if not files:
        print("No emails in outbox/")
        sys.exit(1)
    
    print(f"Mode: {'DRY RUN' if dry else 'LIVE'}")
    print(f"SMTP: {host}:{port}")
    print(f"Emails: {len(files)}")
    print()
    
    smtp = None
    if not dry:
        smtp = smtplib.SMTP(host, port)
        smtp.starttls()
        if user:
            smtp.login(user, pw)
    
    sent = 0
    for path in files:
        email_id = Path(path).stem.replace("_email", "")
        body = open(path).read()
        send_one(smtp, from_addr, email_id, body, dry=dry)
        sent += 1
    
    if smtp:
        smtp.quit()
    
    print(f"\nDone. {sent} processed.")
    print(f"Run 'sqlite3 {DB} \"SELECT status, COUNT(*) FROM sent GROUP BY status;\"' for stats.")

if __name__ == "__main__":
    main()
