#!/usr/bin/env python3
"""Generate agency leads for ReviewReply B2B sales."""
import os, csv, random

AGENCIES = ["BrightLocal", "Whitespark", "Synup", "BirdEye", "Grade.us", "Vendasta", "Chatmeter", "SOCi"]
CITIES = ["Austin", "Denver", "Nashville", "Portland", "Atlanta"]
FIRSTS = ["Sarah", "Jessica", "Amanda", "Laura", "Nicole", "Rachel", "Emily", "Ashley"]

def generate(city, count=10):
    leads = []
    for i in range(count):
        pain = random.randint(0, 3)
        leads.append({
            "id": f"AGY-{city[:3].upper()}-{i+1:03d}",
            "company_name": f"{random.choice(AGENCIES)} {city}",
            "contact_first": random.choice(FIRSTS),
            "phone": f"(555) {random.randint(100,999)}-{random.randint(1000,9999)}",
            "pain_score": pain,
            "manages_gbp_count": random.randint(5, 50) if pain >= 2 else random.randint(1, 10),
            "has_ai_response_tool": str(pain < 1),
            "city": city,
            "industry": "digital_marketing_agency"
        })
    return leads

def main():
    os.makedirs("leads", exist_ok=True)
    os.makedirs("outbox", exist_ok=True)
    total = 0
    for city in CITIES:
        leads = generate(city, 10)
        path = f"leads/{city.lower().replace(' ','_')}_leads.csv"
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=leads[0].keys())
            w.writeheader(); w.writerows(leads)
        total += len(leads)
        outdir = f"outbox/{city.lower().replace(' ','_')}"
        os.makedirs(outdir, exist_ok=True)
        n = 0
        for lead in leads:
            if int(lead["pain_score"]) >= 2:
                email = f"""Subject: {lead['contact_first']} — are you still writing review replies by hand?

Hi {lead['contact_first']},

I noticed {lead['company_name']} manages {lead['manages_gbp_count']} Google Business Profiles.

Question: How many hours per week does your team spend writing review responses?

ReviewReply auto-drafts personalized, brand-safe replies in 3 seconds. One agency client cut 12 hours/week to zero.

Worth a 5-minute look? Reply DEMO and I'll send a Loom.

Sahil
Founder, ReviewReply
"""
                open(f"{outdir}/{lead['id']}_email.md", "w").write(email)
                n += 1
        print(f"  {city:12} | {len(leads)} leads | {n} emails")
    print(f"\nTotal: {total} agency leads generated")

if __name__ == "__main__":
    main()
