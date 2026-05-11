#!/usr/bin/env python3
"""Ghost Systems — Follow-up Email Sequence Generator
Generates Day 3, Day 7, Day 14 follow-ups for each lead in outbox.
"""
import glob, os, sqlite3
from pathlib import Path
from datetime import datetime, timedelta

FOLLOWUPS = {
    3: """Subject: Re: {subject_prefix}

Hi {first_name},

Quick follow-up — I sent a note a few days ago about the missed calls and after-hours leads going to voicemail.

Wanted to check: are you open to a 5-minute call this week? I can show you exactly how much revenue you're leaving on the table (spoiler: it's usually $10K+/mo for HVAC companies your size).

Book a slot here: https://calendly.com/sahil/ghost-systems-demo

Best,
Sahil
Ghost Systems
""",
    7: """Subject: Last try — {subject_prefix}

{first_name},

I know you're busy. This is my last email on this.

One of your competitors in {city} just signed up. They're now capturing 100% of after-hours emergency calls while you're still sending them to voicemail.

If you want to see how it works before they lock up your area, reply with "DEMO" and I'll send a 2-minute Loom video.

No call needed.

Sahil
""",
    14: """Subject: {company} + Ghost Systems case study

{first_name},

Final piece of value before I stop reaching out:

I wrote a 1-page case study showing how a {city} HVAC company added $14,600/mo in recovered leads using an AI receptionist.

Reply "CASE STUDY" and I'll send it over.

If not, no worries — I won't email again.

Sahil
Ghost Systems
"""
}

def generate():
    os.makedirs("followups", exist_ok=True)
    conn = sqlite3.connect("send_live.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS followups (
        email_id TEXT, day INTEGER, path TEXT, created_at TEXT
    )""")
    
    files = sorted(glob.glob("outbox/*/*_email.md"))
    n = 0
    for path in files:
        email_id = Path(path).stem.replace("_email", "")
        city = Path(path).parent.name.replace("_", " ").title()
        
        # Derive first name and company from email content (best effort)
        body = open(path).read()
        first_name = "there"
        company = f"{city} HVAC"
        m = __import__('re').search(r"Hi\s+(\w+),", body)
        if m: first_name = m.group(1)
        
        for day, template in FOLLOWUPS.items():
            subj = "Your after-hours HVAC leads"
            content = template.format(
                first_name=first_name,
                company=company,
                city=city,
                subject_prefix=subj
            )
            out = f"followups/{email_id}_day{day}.md"
            with open(out, "w") as f:
                f.write(content)
            conn.execute("INSERT INTO followups VALUES (?,?,?,?)",
                (email_id, day, out, datetime.utcnow().isoformat()))
            n += 1
    
    conn.commit(); conn.close()
    print(f"Generated {n} follow-up emails ({len(files)} leads × 3 stages)")

if __name__ == "__main__":
    generate()
