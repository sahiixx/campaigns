#!/usr/bin/env python3
"""Generate follow-ups and quotes for any campaign."""
import os, sys, glob, csv
from pathlib import Path

FOLLOWUP_TEMPLATES = {
    3: """Subject: Re: {subject}

Hi {first_name},

Quick follow-up on my note about missed calls and after-hours leads.

Are you open to a 5-minute call this week? I can show you exactly how much revenue you're leaving on the table.

Book a slot: https://calendly.com/sahil/demo

Best,
Sahil
""",
    7: """Subject: Last try — {company}

{first_name},

I know you're busy. This is my last email on this.

One of your competitors just signed up. They're now capturing 100% of after-hours calls while you're still sending them to voicemail.

If you want to see how it works, reply with "DEMO" and I'll send a 2-minute Loom video.

Sahil
""",
    14: """Subject: {company} + case study

{first_name},

Final piece of value before I stop reaching out:

I wrote a 1-page case study showing how a company like yours added $14,600/mo in recovered leads using an AI receptionist.

Reply "CASE STUDY" and I'll send it over.

If not, no worries — I won't email again.

Sahil
"""
}

def generate_extras(campaign):
    base = Path(campaign)
    if not base.exists():
        print(f"Campaign {campaign} not found")
        return
    
    os.makedirs(base / "followups", exist_ok=True)
    os.makedirs(base / "quotes", exist_ok=True)
    
    # Generate followups from outbox emails
    files = sorted(glob.glob(f"{campaign}/outbox/*/*_email.md"))
    n = 0
    for path in files:
        email_id = Path(path).stem.replace("_email", "")
        city = Path(path).parent.name.replace("_", " ").title()
        for day, tmpl in FOLLOWUP_TEMPLATES.items():
            out = base / "followups" / f"{email_id}_day{day}.md"
            with open(out, "w") as f:
                f.write(tmpl.format(
                    first_name="there",
                    company=f"{city} Business",
                    subject="missed calls",
                    city=city
                ))
            n += 1
    print(f"[{campaign}] {n} follow-ups generated")
    
    # Generate quotes from leads
    total = 0
    for csvf in glob.glob(f"{campaign}/leads/*.csv"):
        with open(csvf) as f:
            for lead in csv.DictReader(f):
                if int(lead["pain_score"]) >= 2:
                    setup = 1500
                    monthly = 1200
                    if "roofing" in campaign:
                        setup = 2000
                        monthly = 1800
                    elif "locksmith" in campaign:
                        setup = 1000
                        monthly = 800
                    elif "towing" in campaign:
                        setup = 1200
                        monthly = 900
                    
                    q = f"""# Proposal for {lead['company_name']}

**Service:** AI Receptionist
**Setup:** ${setup:,}
**Monthly:** ${monthly:,}

Guarantee: 3+ additional jobs in 30 days or month 2 free.

— Sahil
"""
                    out = base / "quotes" / f"{lead['id']}_quote.md"
                    with open(out, "w") as f:
                        f.write(q)
                    total += 1
    print(f"[{campaign}] {total} quotes generated")

if __name__ == "__main__":
    for campaign in sys.argv[1:] or ["plumbing-ghost", "roofing-ghost", "electrical-ghost", "locksmith-ghost", "towing-ghost", "dubai-voice", "micro-saas"]:
        generate_extras(campaign)
