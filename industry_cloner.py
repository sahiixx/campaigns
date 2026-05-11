#!/usr/bin/env python3
"""Industry Cloner — Replicate Ghost Systems for any trade.
Usage: python industry_cloner.py <industry> <price> <setup_fee>
Example: python industry_cloner.py plumbing 1200 1500
"""
import sys, shutil, os, re

INDUSTRIES = {
    "plumbing": {"emoji": "🚰", "pain": "burst pipes, leaks, no hot water", "avg_job": 650, "peak": "evenings & weekends"},
    "roofing": {"emoji": "🏠", "pain": "storm damage, leaks, emergency tarp", "avg_job": 3500, "peak": "after storms"},
    "electrical": {"emoji": "⚡", "pain": "outages, panel upgrades, safety issues", "avg_job": 800, "peak": "evenings"},
    "locksmith": {"emoji": "🔑", "pain": "locked out, broken keys, security", "avg_job": 150, "peak": "24/7 always"},
    "towing": {"emoji": "🚗", "pain": "breakdowns, accidents, flat tires", "avg_job": 200, "peak": "nights & weekends"},
}

def clone(industry, price, setup):
    src = "ghost-systems"
    dst = f"{industry}-ghost"
    if os.path.exists(dst):
        print(f"{dst}/ already exists — skipping")
        return
    
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.db", "__pycache__"))
    meta = INDUSTRIES.get(industry, {"emoji": "🏢", "pain": "missed calls", "avg_job": 500, "peak": "after hours"})
    
    # Patch template
    tmpl = f"{dst}/email_template.md"
    if os.path.exists(tmpl):
        text = open(tmpl).read()
        text = text.replace("HVAC", industry.title()).replace("heating and cooling", meta["pain"])
        open(tmpl, "w").write(text)
    
    # Patch README
    readme = f"{dst}/README.md"
    if os.path.exists(readme):
        text = open(readme).read()
        text = re.sub(r"\$1,200", f"${price:,}", text)
        text = re.sub(r"\$1,500", f"${setup:,}", text)
        text = text.replace("HVAC", industry.title())
        open(readme, "w").write(text)
    
    # Patch Vapi config firstMessage
    vapi = f"{dst}/vapi_assistant.json"
    if os.path.exists(vapi):
        text = open(vapi).read()
        text = text.replace("HVAC", industry.title())
        text = text.replace("Aria", f"Aria-{industry[:3].title()}")
        open(vapi, "w").write(text)
    
    print(f"{meta['emoji']} {dst}/ cloned from Ghost Systems")
    print(f"   Pricing: ${price:,}/mo + ${setup:,} setup")
    print(f"   Avg job: ${meta['avg_job']}, Peak: {meta['peak']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python industry_cloner.py <industry> [price] [setup_fee]")
        print("Industries:", ", ".join(INDUSTRIES.keys()))
        sys.exit(1)
    
    industry = sys.argv[1].lower()
    price = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    setup = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    clone(industry, price, setup)
