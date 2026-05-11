#!/usr/bin/env python3
import sys, os, glob, csv, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

CAMPAIGNS = {
    "ghost-systems": {"name": "Ghost Systems", "dir": "ghost-systems", "stages": ["leads","emails","preview","launch"]},
    "micro-saas": {"name": "ReviewReply", "dir": "micro-saas", "stages": ["deploy","preview","launch"]},
    "dubai-voice": {"name": "Dubai Voice Agent", "dir": "dubai-voice", "stages": ["config","preview","launch"]},
    "gumroad-tracker": {"name": "Gumroad Tracker", "dir": "gumroad-tracker", "stages": ["build","preview","launch"]}
}

def banner(t):
    print(f"\n{'='*55}\n  {t}\n{'='*55}\n")

def list_all():
    banner("CAMPAIGN WAR ROOM")
    for k,m in CAMPAIGNS.items():
        ok = os.path.exists(m["dir"])
        n = sum(len(fs) for _,_,fs in os.walk(m["dir"])) if ok else 0
        print(f"  {k:18} | {'🟢' if ok else '🔴'} | {n:3d} files | {m['name']}")
    print()

def run_ghost(stage):
    spec = importlib.util.spec_from_file_location("scraper", "ghost-systems/scraper.py")
    scraper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scraper)
    
    if stage == "leads":
        banner("GENERATING HVAC LEADS")
        total = 0
        for city in ["Phoenix","Houston","Miami","Las Vegas","Dallas"]:
            leads = scraper.generate_sample_leads(city, 10)
            path = f"ghost-systems/leads/{city.lower().replace(' ','_')}_hvac_leads.csv"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=leads[0].keys())
                w.writeheader(); w.writerows(leads)
            hp = sum(1 for l in leads if int(l["pain_score"]) >= 2)
            print(f"  {city:12} | {len(leads):3d} leads | {hp:2d} high-pain")
            total += len(leads)
        print(f"\n  TOTAL: {total} leads generated")
    
    elif stage == "emails":
        banner("GENERATING OUTBOX")
        spec2 = importlib.util.spec_from_file_location("send", "ghost-systems/send.py")
        sender = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(sender)
        template = open("ghost-systems/email_template.md").read()
        n = 0
        for csvf in glob.glob("ghost-systems/leads/*_hvac_leads.csv"):
            city = os.path.basename(csvf).replace("_hvac_leads.csv","").replace("_"," ").title()
            outdir = f"ghost-systems/outbox/{city.lower().replace(' ','_')}"
            os.makedirs(outdir, exist_ok=True)
            with open(csvf) as f:
                leads = list(csv.DictReader(f))
            for lead in leads:
                if int(lead["pain_score"]) >= 2:
                    email = sender.personalize(template, lead)
                    open(f"{outdir}/{lead['id']}_email.md","w").write(email)
                    n += 1
        print(f"  Generated {n} personalized emails")
    
    elif stage == "preview":
        banner("OUTBOX PREVIEW")
        files = sorted(glob.glob("ghost-systems/outbox/*/*_email.md"))[:5]
        if not files:
            print("  Empty. Run: python run.py ghost-systems emails")
            return
        for f in files:
            print(f"\n--- {f} ---")
            for line in open(f).readlines()[:10]:
                print(line.rstrip())
    
    elif stage == "launch":
        banner("LAUNCH CHECKLIST")
        print("  [ ] Google Places API key → ghost-systems/.env")
        print("  [ ] SMTP creds → ghost-systems/.env")
        print("  [ ] Upload vapi_assistant.json → dashboard.vapi.ai")
        print("  [ ] Buy Vapi number ($1/mo) + record Loom")
        print("  [ ] Set calendly.com/sahil")

def run_micro(stage):
    banner("MICRO-SAAS")
    if stage == "deploy":
        print("  Vercel:    npm i -g vercel && vercel --prod")
        print("  Cloudflare: npx wrangler pages deploy micro-saas/")
    elif stage == "launch":
        print("  [ ] Stripe $49/mo  [ ] Google OAuth  [ ] OpenAI key  [ ] Deploy")
    else:
        print("  python -m http.server 8080 --directory micro-saas")

def main():
    if len(sys.argv) < 2:
        list_all()
        print("Usage: python run.py <campaign> <stage>")
        return
    camp, stage = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "preview"
    if camp not in CAMPAIGNS:
        print(f"Unknown: {camp}"); list_all(); sys.exit(1)
    {"ghost-systems": run_ghost, "micro-saas": run_micro}.get(camp, lambda s: print(f"Manual: {CAMPAIGNS[camp]['dir']}/"))(stage)

if __name__ == "__main__":
    main()
