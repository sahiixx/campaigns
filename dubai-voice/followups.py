#!/usr/bin/env python3
import os, glob
from pathlib import Path

SEQUENCE = {
    3: "Subject: Re: Missed international inquiries\n\nHi {first_name},\n\nQuick follow-up on my note about after-hours calls from international buyers.\n\nDubai's luxury market never sleeps — calls come in at 2 AM from London, 6 AM from Mumbai. Are you capturing them?\n\nReply DEMO and I'll send a 2-minute video of Layan handling a viewing booking in real time.\n\nSahil",
    7: "Subject: Last try — {company}\n\n{first_name},\n\nThis is my last email.\n\nOne of your competitors in {city} just deployed a trilingual concierge. They're now booking viewings while you sleep.\n\nIf you want to see the demo before they lock your area, reply YES.\n\nSahil",
    14: "Subject: Dubai market report + your competitor analysis\n\n{first_name},\n\nFinal value-add: I compiled a 1-page report showing which Dubai agencies are using AI concierge and which aren't.\n\nReply REPORT and I'll send it.\n\nNo pitch attached.\n\nSahil"
}

def generate():
    os.makedirs("followups", exist_ok=True)
    files = sorted(glob.glob("outbox/*/*_email.md"))
    n = 0
    for path in files:
        lead_id = Path(path).stem.replace("_email", "")
        body = open(path).read()
        first = "there"
        company = "Your Agency"
        city = Path(path).parent.name.replace("_", " ").title()
        for day, tmpl in SEQUENCE.items():
            out = f"followups/{lead_id}_day{day}.md"
            open(out, "w").write(tmpl.format(first_name=first, company=company, city=city))
            n += 1
    print(f"Generated {n} follow-up emails")

if __name__ == "__main__":
    generate()
