#!/usr/bin/env python3
"""Ghost Systems — Dynamic Quote Generator
Generates custom proposals based on lead pain score and city.
"""
import csv, os

def generate_quote(lead):
    pain = int(lead["pain_score"])
    city = lead.get("city", "Your City")
    
    base = 1200
    setup = 1500
    
    if pain >= 3:
        setup = 750  # 50% off for high-pain (urgent need)
        urgency_note = "URGENT: High pain signals detected — offering 50% off setup to lock in fast."
    elif pain == 2:
        setup = 1125  # 25% off
        urgency_note = "Moderate pain detected — 25% setup discount applied."
    else:
        urgency_note = "Standard pricing."
    
    quote = f"""# Ghost Systems Proposal for {lead['company_name']}

**Date:** 2026-05-11  
**Prepared for:** {lead['contact_first']} at {lead['company_name']}  
**Location:** {city}

---

## The Problem
{urgency_note}

Based on our analysis:
- After-hours calls going to voicemail: ~$8,000–$14,000/mo lost
- No 24/7 booking capability: competitors capturing emergency market
- Manual follow-up fatigue: staff burning out on repetitive calls

## The Solution
**Ghost Systems AI Receptionist**
- Answers 100% of calls 24/7/365
- Books appointments directly into your calendar
- Texts technician with job details instantly
- Speaks English + Spanish

## Pricing
| Item | Monthly | Setup (one-time) |
|------|---------|------------------|
| AI Receptionist | $1,200 | — |
| Setup & Training | — | ~~$1,500~~ **${setup:,}** |
| **Total Year 1** | **$14,400** | **${setup:,}** |

## ROI Guarantee
If Ghost doesn't book at least 3 additional jobs in your first 30 days, **month 2 is free**.

## Next Steps
1. Reply "YES" to lock in the setup discount
2. 15-min onboarding call to train Aria on your booking flow
3. Go live within 48 hours

**This quote expires in 7 days.**

—
Sahil Khan  
Founder, Ghost Systems  
sahil@ghostsystems.io | (555) GHOST-01
"""
    return quote

def main():
    os.makedirs("quotes", exist_ok=True)
    total = 0
    for csvf in [f for f in os.listdir("leads") if f.endswith(".csv")]:
        with open(f"leads/{csvf}") as f:
            for lead in csv.DictReader(f):
                if int(lead["pain_score"]) >= 2:
                    q = generate_quote(lead)
                    path = f"quotes/{lead['id']}_quote.md"
                    with open(path, "w") as fh:
                        fh.write(q)
                    total += 1
    print(f"Generated {total} custom proposals in quotes/")

if __name__ == "__main__":
    main()
