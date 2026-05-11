#!/usr/bin/env python3
"""Ghost Systems — Email Personalizer & Sender Prep
Reads leads.csv + email_template.md, outputs personalized emails ready to send.
"""
import csv, re
from pathlib import Path
from datetime import datetime

def personalize(template, lead):
    """Replace {{fields}} with lead data."""
    text = template
    text = text.replace("{{Company_Name}}", lead["company_name"])
    text = text.replace("{{First_Name}}", lead["contact_first"])
    text = text.replace("{{Your_Name}}", "Sahil")
    text = text.replace("{{Your_Title}}", "Founder")
    text = text.replace("{{Phone_Number}}", "+1-555-GHOST")
    text = text.replace("{{Website}}", "ghostsystems.io")
    
    # Personalize the pain point based on scraper data
    pain_lines = []
    if lead["has_voicemail_after_hours"] == "True":
        pain_lines.append("I called after 6 PM and hit voicemail — that's emergency revenue walking away.")
    if lead["has_recent_gbp_posts"] == "False":
        pain_lines.append("Zero Google posts in 30 days means Google is burying you in search.")
    if lead["has_qa_section"] == "False":
        pain_lines.append("No Q&A section, so common questions go unanswered publicly.")
    
    pain_block = "\n".join(f"- {line}" for line in pain_lines) if pain_lines else "- Your after-hours calls are going to voicemail."
    text = text.replace("**Here's what I found:**\n- Your profile says \"open\" but I called after 6 PM and hit voicemail\n- No \"24/7 emergency service\" badge — your competitors have it\n- Zero posts in the last 30 days (Google drops inactive profiles in search)\n- No Q&A section, so prospects ask \"do you do commercial?\" and nobody answers publicly",
        "**Here's what I found:**\n" + pain_block)
    
    return text

def main():
    template_path = Path("email_template.md")
    template = template_path.read_text()
    
    for csv_file in Path("leads").glob("*_hvac_leads.csv"):
        city = csv_file.stem.replace("_hvac_leads", "").replace("_", " ").title()
        out_dir = Path(f"outbox/{city.lower().replace(' ', '_')}")
        out_dir.mkdir(parents=True, exist_ok=True)
        
        with open(csv_file) as f:
            leads = list(csv.DictReader(f))
        
        high_pain = [l for l in leads if int(l["pain_score"]) >= 2]
        print(f"[{city}] {len(high_pain)} high-pain leads out of {len(leads)}")
        
        for lead in high_pain[:10]:  # Prep first 10 per city
            email = personalize(template, lead)
            out_file = out_dir / f"{lead['id']}_email.md"
            out_file.write_text(email)
        
        print(f"[{city}] {min(len(high_pain), 10)} personalized emails in {out_dir}/")

if __name__ == "__main__":
    main()
