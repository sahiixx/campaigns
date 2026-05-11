#!/usr/bin/env python3
"""Market Map — Competitive density and opportunity scoring per city."""
import csv, json, glob
from collections import defaultdict

def analyze():
    cities = defaultdict(lambda: {"industries": set(), "total_leads": 0, "high_pain": 0, "avg_rating": 0, "total_reviews": 0})
    
    for csvf in glob.glob("*/leads/*.csv"):
        with open(csvf) as f:
            for lead in csv.DictReader(f):
                city = lead.get("city", "Unknown")
                cities[city]["industries"].add(lead.get("industry", "unknown"))
                cities[city]["total_leads"] += 1
                if int(lead.get("pain_score", 0)) >= 2:
                    cities[city]["high_pain"] += 1
                cities[city]["avg_rating"] += float(lead.get("rating", 0) or 0)
                cities[city]["total_reviews"] += int(lead.get("review_count", 0) or 0)
    
    results = []
    for city, data in cities.items():
        n = data["total_leads"]
        if n == 0:
            continue
        avg_rating = data["avg_rating"] / n
        pain_ratio = data["high_pain"] / n
        # Opportunity score: high pain + low reviews + low rating = desperate need
        opportunity = (pain_ratio * 50) + max(0, (4.5 - avg_rating) * 20) + max(0, (100 - data["total_reviews"]/n) * 0.1)
        results.append({
            "city": city,
            "leads": n,
            "industries": len(data["industries"]),
            "high_pain": data["high_pain"],
            "avg_rating": round(avg_rating, 2),
            "avg_reviews": round(data["total_reviews"]/n, 0),
            "opportunity_score": round(opportunity, 1)
        })
    
    results.sort(key=lambda x: x["opportunity_score"], reverse=True)
    
    print("\n" + "="*80)
    print("  MARKET OPPORTUNITY MAP")
    print("="*80 + "\n")
    print(f"  {'City':15} | {'Leads':5} | {'Industries':10} | {'High Pain':9} | {'Avg Rating':10} | {'Opportunity':11}")
    print("  " + "-"*75)
    for r in results[:15]:
        print(f"  {r['city']:15} | {r['leads']:5} | {r['industries']:10} | {r['high_pain']:9} | {r['avg_rating']:10} | {r['opportunity_score']:11.1f}")
    
    with open("market_map.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved to market_map.json")

if __name__ == "__main__":
    analyze()
