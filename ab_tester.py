#!/usr/bin/env python3
"""A/B Test Framework for Cold Email Subject Lines"""
import os, glob, random, json
from pathlib import Path

SUBJECT_VARIANTS = {
    "ghost-systems": [
        ("A", "Quick question about missed calls, {first_name}"),
        ("B", "Your after-hours HVAC leads are going to voicemail"),
        ("C", "{first_name} — are you losing emergency calls?"),
        ("D", "HVAC companies in {city} are using AI receptionists"),
    ],
    "plumbing-ghost": [
        ("A", "Quick question about missed calls, {first_name}"),
        ("B", "Your after-hours plumbing leads are going to voicemail"),
        ("C", "{first_name} — are you losing emergency calls?"),
    ],
    "dubai-voice": [
        ("A", "Your missed international inquiries, {first_name}"),
        ("B", "Dubai luxury agencies using AI concierge"),
        ("C", "{first_name} — are you capturing 2 AM calls?"),
    ],
    "micro-saas": [
        ("A", "{first_name} — still writing review replies by hand?"),
        ("B", "This agency cut 12 hours/week with one tool"),
        ("C", "Auto-respond to Google reviews in 3 seconds"),
    ]
}

def generate_tests(campaign, outdir="ab_tests"):
    meta = SUBJECT_VARIANTS.get(campaign, [])
    if not meta:
        return 0
    os.makedirs(outdir, exist_ok=True)
    files = sorted(glob.glob(f"{campaign}/outbox/*/*_email.md"))
    n = 0
    results = {"campaign": campaign, "variants": [v[0] for v in meta], "assignments": []}
    
    for path in files[:30]:  # test on first 30 emails
        email_id = Path(path).stem.replace("_email", "")
        body = open(path).read()
        first = "there"
        city = Path(path).parent.name.replace("_", " ").title()
        # pick random variant
        variant, subject_tpl = random.choice(meta)
        subject = subject_tpl.format(first_name=first, city=city)
        
        # rewrite subject line in email
        lines = body.split("\n")
        new_lines = []
        for line in lines:
            if line.startswith("Subject:"):
                new_lines.append(f"Subject: {subject}")
            else:
                new_lines.append(line)
        new_body = "\n".join(new_lines)
        
        out = f"{outdir}/{campaign}_{email_id}_{variant}.md"
        open(out, "w").write(new_body)
        results["assignments"].append({"email": email_id, "variant": variant, "subject": subject})
        n += 1
    
    json.dump(results, open(f"{outdir}/{campaign}_ab_plan.json", "w"), indent=2)
    print(f"{campaign:18} | {n} A/B test emails | {len(meta)} variants")
    return n

def main():
    print("="*55)
    print("  A/B TEST FRAMEWORK")
    print("="*55 + "\n")
    total = 0
    for campaign in SUBJECT_VARIANTS:
        total += generate_tests(campaign)
    print(f"\nTotal: {total} test emails generated in ab_tests/")
    print("Track opens/replies per variant to find winner.")

if __name__ == "__main__":
    main()
