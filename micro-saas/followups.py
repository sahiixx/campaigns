#!/usr/bin/env python3
import os, glob
from pathlib import Path

SEQ = {
    3: "Subject: Re: Review reply automation\n\nHi {first_name},\n\nQuick follow-up — I sent a note about cutting review response time from hours to seconds.\n\nOne agency using ReviewReply saved 12 hours/week and landed 2 new clients because their response rate jumped to 100%.\n\nReply DEMO for a 2-min Loom.\n\nSahil",
    7: "Subject: Last try — {company}\n\n{first_name},\n\nLast email on this.\n\nYour competitor {city} Digital just signed up for ReviewReply Growth. They're white-labeling responses for 8 clients.\n\nIf you want to see the demo, reply YES. Otherwise, I'll stop reaching out.\n\nSahil",
    14: "Subject: Free tool: Review response template library\n\n{first_name},\n\nFinal value-add: I built a free Notion library of 50 review response templates for agencies.\n\nReply TEMPLATES and I'll send the link. No pitch.\n\nSahil"
}

def generate():
    os.makedirs("followups", exist_ok=True)
    files = sorted(glob.glob("outbox/*/*_email.md"))
    n = 0
    for path in files:
        lead_id = Path(path).stem.replace("_email", "")
        city = Path(path).parent.name.replace("_", " ").title()
        for day, tmpl in SEQ.items():
            open(f"followups/{lead_id}_day{day}.md", "w").write(
                tmpl.format(first_name="there", company="Your Agency", city=city))
            n += 1
    print(f"Generated {n} follow-ups")

if __name__ == "__main__":
    generate()
