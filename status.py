#!/usr/bin/env python3
"""Campaign Launch Readiness Report"""
import os, glob, json
from pathlib import Path

def check_campaign(name, path):
    r = {"name": name, "dir": path, "score": 0, "max": 100, "checks": {}}
    
    def ok(cond, points=10):
        return ("✅", points) if cond else ("❌", 0)
    
    # Core files
    r["checks"]["README"] = ok(Path(path, "README.md").exists())
    r["checks"]["Backend"] = ok(Path(path, "backend/main.py").exists(), 20)
    r["checks"]["Vapi Config"] = ok(any(f.name.endswith(".json") and "vapi" in f.name for f in Path(path).glob("*.json")), 15)
    r["checks"]["Contract"] = ok(Path(path, "contract.md").exists(), 10)
    r["checks"]["Demo Script"] = ok(Path(path, "loom_script.md").exists(), 10)
    
    # Data
    leads = len(glob.glob(f"{path}/leads/*.csv"))
    r["checks"]["Leads"] = ok(leads > 0, 10)
    emails = len(glob.glob(f"{path}/outbox/*/*_email.md"))
    r["checks"]["Emails"] = ok(emails > 0, 10)
    quotes = len(glob.glob(f"{path}/quotes/*.md"))
    r["checks"]["Quotes"] = ok(quotes > 0, 10)
    followups = len(glob.glob(f"{path}/followups/*.md"))
    r["checks"]["Follow-ups"] = ok(followups > 0, 10)
    onboarding = Path(path, "onboarding.md").exists()
    r["checks"]["Onboarding"] = ok(onboarding, 5)
    
    # Deployment ready
    docker = Path(path, "backend/Dockerfile").exists()
    r["checks"]["Dockerfile"] = ok(docker, 10)
    
    r["score"] = sum(v[1] for v in r["checks"].values())
    r["emails"] = emails
    r["leads"] = leads * 10  # rough
    return r

def main():
    results = []
    for d in Path(".").iterdir():
        if d.is_dir() and not d.name.startswith(".") and (d / "README.md").exists():
            results.append(check_campaign(d.name, str(d)))
    
    results.sort(key=lambda x: x["score"], reverse=True)
    
    print("\n" + "="*70)
    print("  CAMPAIGN LAUNCH READINESS")
    print("="*70 + "\n")
    print(f"  {'Campaign':20} | {'Score':5} | {'Leads':6} | {'Emails':6} | {'Status'}")
    print("  " + "-"*66)
    
    for r in results:
        status = "🟢 READY" if r["score"] >= 80 else "🟡 ALMOST" if r["score"] >= 50 else "🔴 WIP"
        print(f"  {r['name']:20} | {r['score']:3d}/100 | {r['leads']:5d} | {r['emails']:5d} | {status}")
    
    top = results[0]
    print(f"\n  🚀 TOP PICK: {top['name']} ({top['score']}/100)")
    print(f"  Missing to launch:")
    for k, v in top["checks"].items():
        if v[0] == "❌":
            print(f"    - {k}")
    
    with open("launch_readiness.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved detailed report to launch_readiness.json")

if __name__ == "__main__":
    main()
