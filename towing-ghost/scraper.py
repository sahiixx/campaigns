#!/usr/bin/env python3
"""Ghost Systems — HVAC Lead Scraper
Scrapes Google Maps for HVAC companies in target cities.
Outputs: leads.csv with name, phone, website, hours, gbp_url, notes
"""
import csv, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

def search_places(query, api_key=None):
    """Search for places using Google Places API (needs API key)
    Falls back to mock data generator for demo/testing."""
    if not api_key:
        return None
    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        f"query={urllib.parse.quote(query)}&key={api_key}"
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"API error: {e}")
        return None

def generate_sample_leads(city="Phoenix", count=20):
    """Generate realistic sample HVAC leads for immediate testing."""
    templates = [
        ("{name} Heating & Cooling", "heatingandcooling.com"),
        ("{name} HVAC Services", "hvacservices.com"),
        ("{name} Air Conditioning", "acrepair.com"),
        ("{name} Climate Control", "climatecontrol.com"),
        ("{name} Comfort Solutions", "comfortsolutions.com"),
    ]
    first_names = ["Mike", "John", "Dave", "Chris", "Ryan", "Tom", "Alex", "Sam",
                   "Jose", "Carlos", "Robert", "Bill", "Dan", "Steve", "Joe"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Miller", "Davis", "Rodriguez", "Martinez"]
    streets = ["Main St", "1st Ave", "Washington St", "Jefferson Blvd",
               "Oak St", "Pine Ave", "Cedar Rd", "Maple Dr"]
    
    leads = []
    for i in range(count):
        fn = first_names[i % len(first_names)]
        ln = last_names[i % len(last_names)]
        biz = templates[i % len(templates)][0].format(name=fn)
        domain = templates[i % len(templates)][1]
        street = streets[i % len(streets)]
        num = 100 + i * 50
        phone = f"(602) {555 + i:03d}-{1000 + i:04d}"
        
        # Randomize "pain signals"
        has_voicemail = i % 3 != 0  # 66% have after-hours voicemail
        has_posts = i % 4 == 0      # 25% have recent GBP posts
        has_qa = i % 5 == 0         # 20% have Q&A
        
        pain_score = (1 if has_voicemail else 0) + (0 if has_posts else 1) + (0 if has_qa else 1)
        
        leads.append({
            "id": f"HVAC-{city[:3].upper()}-{i+1:03d}",
            "company_name": biz,
            "contact_first": fn,
            "contact_last": ln,
            "email": f"info@{fn.lower()}{ln.lower()}.{domain}",
            "phone": phone,
            "address": f"{num} {street}, {city}, AZ",
            "website": f"https://{fn.lower()}{ln.lower()}.{domain}",
            "gbp_url": "",
            "hours": "8AM-5PM M-F" if i % 2 == 0 else "7AM-6PM M-Sat",
            "has_voicemail_after_hours": has_voicemail,
            "has_recent_gbp_posts": has_posts,
            "has_qa_section": has_qa,
            "pain_score": pain_score,
            "status": "NEW",
            "email_sent_date": "",
            "reply": "",
            "notes": ""
        })
    return leads

def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "Phoenix"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    api_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"[GHOST SYSTEMS] Generating {count} HVAC leads for {city}...")
    
    if api_key:
        results = search_places(f"HVAC companies in {city}", api_key)
        # TODO: parse real API results
        leads = []
    else:
        print("[INFO] No Google Places API key provided. Using sample data.")
        print("[INFO] Add API key: python scraper.py 'Phoenix' 50 'YOUR_API_KEY'")
        leads = generate_sample_leads(city, count)
    
    out_path = Path(f"leads/{city.lower().replace(' ', '_')}_hvac_leads.csv")
    out_path.parent.mkdir(exist_ok=True)
    
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
    
    print(f"[DONE] {len(leads)} leads written to {out_path}")
    high_pain = [l for l in leads if l["pain_score"] >= 2]
    print(f"[HIGH PAIN] {len(high_pain)} leads with score 2-3 (prioritize these)")

if __name__ == "__main__":
    main()
