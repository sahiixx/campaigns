#!/usr/bin/env python3
import os, csv, random
from pathlib import Path

CITIES = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"]
NAMES = ["LuxEstate", "PrimeProperties", "DubaiHomes", "RoyalRealty", "EliteLiving", "PalmResidences", "MarinaViews", "BurjEstates"]
FIRSTS = ["Omar", "Khalid", "Faisal", "Rashid", "Samir", "Hassan", "Tariq", "Zayed"]

def generate(city, count=10):
    leads = []
    for i in range(count):
        pain = random.randint(0, 3)
        leads.append({
            "id": f"DUB-{city[:3].upper()}-{i+1:03d}",
            "company_name": f"{random.choice(NAMES)} {city}",
            "contact_first": random.choice(FIRSTS),
            "phone": f"+971-50-{random.randint(1000000,9999999)}",
            "address": f"{random.randint(1,999)} {city} Street",
            "pain_score": pain,
            "has_24_7_call_center": str(pain < 1),
            "has_multilingual_support": str(pain < 2),
            "has_whatsapp_integration": str(pain < 1),
            "city": city,
            "industry": "real_estate"
        })
    return leads

def main():
    os.makedirs("leads", exist_ok=True)
    os.makedirs("outbox", exist_ok=True)
    os.makedirs("followups", exist_ok=True)
    os.makedirs("quotes", exist_ok=True)
    
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
            pain = int(lead["pain_score"])
            if pain >= 2:
                email = f"Subject: Your missed international inquiries, {lead['contact_first']}\n\nHi {lead['contact_first']},\n\nI noticed {lead['company_name']} handles luxury properties but may be missing after-hours calls from international buyers.\n\nDubai Voice Agent (Layan) answers in English, Arabic, and Hindi 24/7.\n\nWorth a 5-minute conversation?\n\nSahil\n"
                open(f"{outdir}/{lead['id']}_email.md", "w").write(email)
                n += 1
                setup = 5000 if pain == 3 else 3750
                quote = f"# Proposal for {lead['company_name']}\n\n**Service:** Dubai Voice Agent — Trilingual AI Concierge\n**Setup:** AED {setup:,} (~${setup:,} USD)\n**Monthly:** AED 7,400 (~$2,000 USD)\n\nGuarantee: 5 viewings in 30 days or month 2 free.\n\n— Sahil\n"
                open(f"quotes/{lead['id']}_quote.md", "w").write(quote)
        print(f"  {city:12} | {len(leads)} leads | {n} emails")
    
    print(f"\nTotal: {total} leads generated")

if __name__ == "__main__":
    main()
