#!/usr/bin/env python3
import os, csv, random, re
from pathlib import Path

INDUSTRIES = {
    "plumbing": {"names": ["FlowRight", "PipePro", "DrainMasters", "AquaFix", "HydroFlow", "LeakStop", "Prime Plumbing", "BlueLine"], "pain": "burst pipes, sewage backups, no hot water", "avg_job": 650, "first_names": ["Mike", "Dave", "Tom", "Chris", "Alex", "Ryan", "John", "Steve"]},
    "roofing": {"names": ["TopShield", "SkyGuard", "PeakRoof", "StormProof", "EliteRoofing", "CoverAll", "Apex Roofing"], "pain": "storm damage, leaks, missing shingles", "avg_job": 3500, "first_names": ["Jake", "Matt", "Dan", "Rob", "Eric", "Nick", "Paul", "Sam"]},
    "electrical": {"names": ["VoltTech", "PowerPro", "BrightWire", "CircuitMax", "AmpFlow", "SparkLine", "LiveWire"], "pain": "outages, panel upgrades, faulty wiring", "avg_job": 800, "first_names": ["Kevin", "Brian", "Joe", "Mark", "Tim", "Greg", "Scott", "Andy"]},
    "locksmith": {"names": ["KeyMaster", "LockPro", "SafeGuard", "AccessNow", "SwiftKey", "SecureEntry", "PrimeLock"], "pain": "lockouts, broken keys, security upgrades", "avg_job": 150, "first_names": ["Tony", "Leo", "Vic", "Max", "Ben", "Ray", "Al", "Lou"]},
    "towing": {"names": ["RapidTow", "RoadRescue", "AutoHaul", "FastTow", "CityTowing", "EliteRecovery", "24/7 Tow"], "pain": "breakdowns, accidents, flat tires", "avg_job": 200, "first_names": ["Frank", "Bill", "Walt", "Dean", "Carl", "Phil", "Stan", "Earl"]}
}

def generate_leads(industry, city, count=10):
    meta = INDUSTRIES[industry]
    leads = []
    for i in range(count):
        pain = random.randint(0, 3)
        leads.append({
            "id": f"{industry[:3].upper()}-{city[:3].upper()}-{i+1:03d}",
            "company_name": f"{random.choice(meta['names'])} {city}",
            "contact_first": random.choice(meta["first_names"]),
            "phone": f"(555) {random.randint(100,999)}-{random.randint(1000,9999)}",
            "address": f"{random.randint(100,9999)} {city} St",
            "rating": round(random.uniform(3.0, 5.0), 1),
            "review_count": random.randint(0, 200),
            "pain_score": pain,
            "has_voicemail_after_hours": str(pain >= 2),
            "has_recent_gbp_posts": str(pain < 2),
            "has_qa_section": str(pain < 1),
            "city": city,
            "industry": industry
        })
    return leads

def regenerate(industry):
    base = f"{industry}-ghost"
    if not os.path.exists(base):
        return
    meta = INDUSTRIES[industry]
    os.makedirs(f"{base}/leads", exist_ok=True)
    total = 0
    for city in ["Phoenix", "Houston", "Miami", "Las Vegas", "Dallas"]:
        leads = generate_leads(industry, city, 10)
        path = f"{base}/leads/{city.lower().replace(' ','_')}_leads.csv"
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=leads[0].keys())
            w.writeheader(); w.writerows(leads)
        total += len(leads)
    print(f"{industry:12} | {total} leads generated")
    
    tmpl_path = f"{base}/email_template.md"
    if os.path.exists(tmpl_path):
        tmpl = open(tmpl_path).read()
        os.makedirs(f"{base}/outbox", exist_ok=True)
        n = 0
        for csvf in [f for f in os.listdir(f"{base}/leads") if f.endswith(".csv")]:
            city = csvf.replace("_leads.csv", "").replace("_", " ").title()
            outdir = f"{base}/outbox/{city.lower().replace(' ','_')}"
            os.makedirs(outdir, exist_ok=True)
            with open(f"{base}/leads/{csvf}") as f:
                for lead in csv.DictReader(f):
                    if int(lead["pain_score"]) >= 2:
                        email = tmpl.replace("{{Company_Name}}", lead["company_name"])
                        email = email.replace("{{First_Name}}", lead["contact_first"])
                        email = email.replace("{{Your_Name}}", "Sahil")
                        email = email.replace("{{Your_Title}}", "Founder")
                        email = email.replace("{{Phone_Number}}", f"+1-555-{industry[:4].upper()}")
                        email = email.replace("{{Website}}", f"{industry}ghost.io")
                        open(f"{outdir}/{lead['id']}_email.md", "w").write(email)
                        n += 1
        print(f"{industry:12} | {n} emails written")
    
    readme = f"{base}/README.md"
    if os.path.exists(readme):
        text = open(readme).read()
        text = re.sub(r"Avg job: \$[\d,]+", f"Avg job: ${meta['avg_job']:,}", text)
        open(readme, "w").write(text)

if __name__ == "__main__":
    for industry in INDUSTRIES:
        regenerate(industry)
    print("\nAll industries regenerated with unique data.")
