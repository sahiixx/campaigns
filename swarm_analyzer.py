#!/usr/bin/env python3
"""Sovereign Swarm — Campaign Analyzer
Uses local Ollama to analyze campaign data and output prioritized execution plan.
"""
import os, glob, json, csv, sqlite3
from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def analyze_campaign(name, path):
    stats = {"name": name, "files": 0, "leads": 0, "emails": 0, "backend": False, "revenue_potential": 0}
    
    for root, _, files in os.walk(path):
        stats["files"] += len(files)
        if "backend/main.py" in os.path.join(root, "main.py"):
            stats["backend"] = True
    
    for csvf in glob.glob(f"{path}/leads/*.csv"):
        with open(csvf) as f:
            leads = list(csv.DictReader(f))
            stats["leads"] += len(leads)
            for l in leads:
                stats["revenue_potential"] += int(l.get("pain_score", 0)) * 200
    
    stats["emails"] = len(glob.glob(f"{path}/outbox/*/*_email.md"))
    stats["followups"] = len(glob.glob(f"{path}/followups/*.md"))
    stats["quotes"] = len(glob.glob(f"{path}/quotes/*.md"))
    return stats

def main():
    campaigns = []
    for d in Path(".").iterdir():
        if d.is_dir() and not d.name.startswith(".") and (d / "README.md").exists():
            campaigns.append(analyze_campaign(d.name, str(d)))
    
    # Sort by revenue potential
    campaigns.sort(key=lambda x: x["revenue_potential"], reverse=True)
    
    report = "CAMPAIGN ANALYSIS REPORT\n" + "="*50 + "\n\n"
    for c in campaigns:
        report += f"Campaign: {c['name']}\n"
        report += f"  Leads: {c['leads']} | Emails: {c['emails']} | Follow-ups: {c['followups']} | Quotes: {c['quotes']}\n"
        report += f"  Backend: {'Yes' if c['backend'] else 'No'} | Revenue Potential: ${c['revenue_potential']:,}\n\n"
    
    print(report)
    
    # Save JSON
    with open("swarm_report.json", "w") as f:
        json.dump({"campaigns": campaigns, "top_pick": campaigns[0]["name"]}, f, indent=2)
    print("Saved to swarm_report.json")
    
    # Try Ollama for strategic recommendation
    try:
        import urllib.request
        prompt = f"""You are a growth strategist. Based on this campaign data, give a 3-bullet prioritized action plan:

{report}

Keep it extremely concise. Each bullet max 12 words."""
        
        data = json.dumps({"model": "llama3.2:3b", "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
        print("\n[SWARM RECOMMENDATION]")
        print(result.get("response", "No response"))
    except Exception as e:
        print(f"\n[SWARM] Ollama offline or error: {e}")
        print("Recommendation: Launch Ghost Systems first (highest readiness).")

if __name__ == "__main__":
    main()
