# Ghost Systems

AI receptionist for HVAC companies. Answers calls 24/7, books appointments, texts technicians.

**Status:** Pre-launch (leads generated, backend tested, ready to deploy)  
**Pricing:** $1,200/mo + $1,500 setup (discounts available)  
**Stack:** Vapi (voice), FastAPI (backend), SQLite (data), SendGrid (email)

---

## Quick Start (Local)

```bash
# 1. Start backend API + dashboard
pip install fastapi uvicorn
cd backend
uvicorn main:app --reload

# 2. In another terminal — generate leads & emails
cd ..
python run.py ghost-systems leads
python run.py ghost-systems emails

# 3. Preview outbox
python run.py ghost-systems preview

# 4. Dry-run email sender
python send_live.py --dry-run

# 5. Live send (add SMTP creds first)
export SMTP_HOST=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USER=apikey
export SMTP_PASS=SG.xxx
python send_live.py --live
```

## File Map

| File | Purpose |
|------|---------|
| `scraper.py` | Generate HVAC leads (sample data or Google Places API) |
| `send.py` | Personalize emails from template + lead data |
| `send_live.py` | SMTP sender with duplicate protection |
| `followups.py` | Day 3 / 7 / 14 follow-up sequence generator |
| `quote_generator.py` | Dynamic proposals based on pain score |
| `test_call.py` | Simulate Vapi call flow for demos |
| `vapi_assistant.json` | Vapi assistant config (upload to dashboard.vapi.ai) |
| `backend/main.py` | FastAPI: webhooks, appointments, calls, dashboard |
| `backend/Dockerfile` | Container for Render/Railway deploy |
| `loom_script.md` | 5-minute demo video script |
| `contract.md` | Service agreement template |
| `onboarding.md` | Client go-live checklist |

## Deploy Backend

```bash
# Render (free tier)
cd backend
git init && git add . && git commit -m "init"
# Push to GitHub, then connect repo on render.com

# Or Railway
railway login
railway init
railway up
```

## Vapi Setup
1. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
2. Create assistant → Import JSON → paste `vapi_assistant.json`
3. Buy phone number ($1/mo)
4. Set webhook URL: `https://your-api.com/webhook/vapi`
5. Test with `test_call.py`

## Metrics
- **50 leads** across 5 cities (Phoenix, Houston, Miami, Las Vegas, Dallas)
- **74 personalized cold emails** in outbox/
- **222 follow-ups** (3-stage sequence) in followups/
- **70 custom proposals** in quotes/
- Backend tested: webhook → booking → dashboard in <2s

## License
Proprietary — Ghost Systems LLC
