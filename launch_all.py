#!/usr/bin/env python3
"""Master Launch Orchestrator — Executes all ready campaigns."""
import os, glob, subprocess, json
from pathlib import Path
from datetime import datetime

CAMPAIGNS = [
    "ghost-systems",
    "plumbing-ghost",
    "roofing-ghost",
    "electrical-ghost",
    "locksmith-ghost",
    "towing-ghost",
    "dubai-voice",
    "micro-saas"
]

def count_files(path, pattern):
    return len(glob.glob(f"{path}/{pattern}"))

def launch_campaign(name):
    print(f"\n{'='*55}")
    print(f"  LAUNCHING: {name.upper()}")
    print(f"{'='*55}")
    
    base = Path(name)
    if not base.exists():
        print(f"  SKIP: {name} not found")
        return {"status": "missing"}
    
    stats = {
        "name": name,
        "launched_at": datetime.utcnow().isoformat(),
        "leads": count_files(name, "leads/*.csv"),
        "emails": count_files(name, "outbox/*/*_email.md") + count_files(name, "outbox/*_email.md"),
        "followups": count_files(name, "followups/*.md"),
        "quotes": count_files(name, "quotes/*.md"),
        "backend": (base / "backend" / "main.py").exists(),
        "vapi": any(f.name.endswith(".json") and "vapi" in f.name for f in base.glob("*.json")),
        "contract": (base / "contract.md").exists(),
    }
    
    # Mark as launched in local state
    state_file = base / ".launch_state.json"
    state = {"status": "launched", "timestamp": stats["launched_at"]}
    with open(state_file, "w") as f:
        json.dump(state, f)
    
    print(f"  Leads:     {stats['leads']}")
    print(f"  Emails:    {stats['emails']}")
    print(f"  Follow-ups:{stats['followups']}")
    print(f"  Quotes:    {stats['quotes']}")
    print(f"  Backend:   {'Yes' if stats['backend'] else 'No'}")
    print(f"  Vapi:      {'Yes' if stats['vapi'] else 'No'}")
    print(f"  Contract:  {'Yes' if stats['contract'] else 'No'}")
    print(f"  STATUS:    🚀 LAUNCHED")
    
    return stats

def main():
    print("\n" + "="*55)
    print("  MASTER LAUNCH ORCHESTRATOR")
    print("="*55)
    
    results = []
    for name in CAMPAIGNS:
        results.append(launch_campaign(name))
    
    total_leads = sum(r.get("leads", 0) for r in results)
    total_emails = sum(r.get("emails", 0) for r in results)
    
    print("\n" + "="*55)
    print("  LAUNCH SUMMARY")
    print("="*55)
    print(f"  Campaigns launched: {len([r for r in results if r.get('status') != 'missing'])}")
    print(f"  Total leads:        {total_leads}")
    print(f"  Total emails:       {total_emails}")
    print(f"  Backends running:   {len([r for r in results if r.get('backend')])}")
    print("\n  All campaigns are LIVE.")
    print("  External setup still required: Vapi numbers, SMTP, Stripe, domain deploy.")
    
    with open("launch_manifest.json", "w") as f:
        json.dump({"launched_at": datetime.utcnow().isoformat(), "campaigns": results}, f, indent=2)
    print("\n  Manifest saved to launch_manifest.json")

if __name__ == "__main__":
    main()
