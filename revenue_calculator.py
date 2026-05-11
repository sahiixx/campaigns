#!/usr/bin/env python3
"""Revenue Calculator — Projected income across all campaigns."""
import json, os

CAMPAIGNS = {
    "ghost-systems": {"leads": 60, "price_mo": 1200, "setup": 1500, "close_rate": 0.05, "churn_mo": 0.05},
    "plumbing-ghost": {"leads": 110, "price_mo": 1200, "setup": 1500, "close_rate": 0.04, "churn_mo": 0.05},
    "roofing-ghost": {"leads": 110, "price_mo": 1800, "setup": 2000, "close_rate": 0.03, "churn_mo": 0.04},
    "electrical-ghost": {"leads": 110, "price_mo": 1200, "setup": 1500, "close_rate": 0.04, "churn_mo": 0.05},
    "locksmith-ghost": {"leads": 110, "price_mo": 800, "setup": 1000, "close_rate": 0.06, "churn_mo": 0.06},
    "towing-ghost": {"leads": 110, "price_mo": 900, "setup": 1200, "close_rate": 0.05, "churn_mo": 0.07},
    "dubai-voice": {"leads": 40, "price_mo": 2000, "setup": 5000, "close_rate": 0.02, "churn_mo": 0.03},
    "micro-saas": {"leads": 50, "price_mo": 99, "setup": 0, "close_rate": 0.08, "churn_mo": 0.10},
}

def project(name, meta, months=12):
    customers = int(meta["leads"] * meta["close_rate"])
    setup_rev = customers * meta["setup"]
    mrr = 0
    total_recurring = 0
    active = customers
    for m in range(1, months+1):
        mrr = active * meta["price_mo"]
        total_recurring += mrr
        active = int(active * (1 - meta["churn_mo"]))
    return {
        "name": name,
        "customers": customers,
        "setup_revenue": setup_rev,
        "mrr_month_1": customers * meta["price_mo"],
        "mrr_month_12": active * meta["price_mo"],
        "year_recurring": total_recurring,
        "year_total": setup_rev + total_recurring
    }

def main():
    results = [project(n, m) for n, m in CAMPAIGNS.items()]
    results.sort(key=lambda x: x["year_total"], reverse=True)
    
    print("\n" + "="*70)
    print("  REVENUE PROJECTION — 12 MONTHS")
    print("="*70 + "\n")
    print(f"  {'Campaign':18} | {'Customers':9} | {'Setup':10} | {'MRR M1':8} | {'Year Total':11}")
    print("  " + "-"*65)
    
    total = 0
    for r in results:
        print(f"  {r['name']:18} | {r['customers']:9} | ${r['setup_revenue']:>8,} | ${r['mrr_month_1']:>6,} | ${r['year_total']:>9,}")
        total += r["year_total"]
    
    print("  " + "-"*65)
    print(f"  {'TOTAL':18} | {'':9} | {'':10} | {'':8} | ${total:>9,}")
    print(f"\n  Estimated first-year revenue: ${total:,}")
    print(f"  Assumes close rates and churn as modeled.")
    
    with open("revenue_projection.json", "w") as f:
        json.dump({"campaigns": results, "total_year_1": total}, f, indent=2)
    print(f"\n  Saved to revenue_projection.json")

if __name__ == "__main__":
    main()
