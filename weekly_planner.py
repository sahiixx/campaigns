#!/usr/bin/env python3
"""Weekly Execution Planner — Generates prioritized task list."""
import json, os
from datetime import datetime, timedelta

PLAN = {
    "Monday": [
        "Send 10 cold emails (dry-run first)",
        "Post LinkedIn content from content/social_media.md",
        "Check all API health (campaigns-cli status)"
    ],
    "Tuesday": [
        "Follow up on Monday emails (Day 3 sequence)",
        "Record 1 Loom demo (ghost-systems or dubai-voice)",
        "Update War Room dashboard"
    ],
    "Wednesday": [
        "Send 10 more cold emails (next city)",
        "A/B test subject lines from ab_tests/",
        "Engage with 5 HVAC/roofing LinkedIn posts"
    ],
    "Thursday": [
        "Follow up on Wednesday emails",
        "Calendly call with 1 warm lead",
        "Publish SEO blog post"
    ],
    "Friday": [
        "Weekly analytics: open rates, reply rates, bookings",
        "Update revenue_projection.json with actuals",
        "Plan next week's city target"
    ],
    "Saturday": [
        "Optional: Record batch of Loom demos",
        "Optional: Expand to new industry vertical"
    ],
    "Sunday": [
        "Rest. Systems are running.",
        "Read market_map.json for next week's target city"
    ]
}

def generate():
    today = datetime.now().strftime("%A")
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    
    print(f"\n{'='*55}")
    print(f"  WEEKLY PLANNER — Week of {week_start}")
    print(f"  Today is {today}")
    print(f"{'='*55}\n")
    
    for day, tasks in PLAN.items():
        marker = ">>>" if day == today else "   "
        print(f"{marker} {day}")
        for t in tasks:
            print(f"    • {t}")
        print()
    
    with open(f"weekly_plan_{week_start}.md", "w") as f:
        f.write(f"# Weekly Plan — {week_start}\n\n")
        for day, tasks in PLAN.items():
            f.write(f"## {day}\n")
            for t in tasks:
                f.write(f"- [ ] {t}\n")
            f.write("\n")
    print(f"Saved to weekly_plan_{week_start}.md")

if __name__ == "__main__":
    generate()
