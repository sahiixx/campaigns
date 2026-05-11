# Campaign War Room

Multi-vertical AI agency infrastructure. Built for launch.

## Status
- **8 campaigns** built (7 ready, 1 WIP)
- **420 leads** in unified CRM
- **$107,790** projected Year 1 revenue
- **8 services** running via systemd

## Services

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Ghost API | 8000 | http://localhost:8000 | HVAC AI receptionist backend |
| Dubai API | 8002 | http://localhost:8002 | Trilingual real estate concierge |
| Gumroad API | 8003 | http://localhost:8003 | Sales tracker dashboard |
| Telegram Bot | 8004 | http://localhost:8004 | Campaign notifications |
| CRM API | 8005 | http://localhost:8005 | Unified lead management |
| API Gateway | 8006 | http://localhost:8006 | Aggregated health + stats |
| War Room Dashboard | 3000 | http://localhost:3000 | Live HTML dashboard |
| ReviewReply Landing | 8080 | http://localhost:8080 | SaaS landing + pricing |

## Quick Commands

```bash
# Check everything
cd ~/campaigns
./campaigns-cli status

# Sync CRM
./campaigns-cli sync

# Stop / start all
./campaigns-cli stop
./campaigns-cli start

# View logs
./campaigns-cli logs ghost-api
```

## Campaigns

### Ready to Launch
1. **ghost-systems** — HVAC AI Receptionist ($1,200/mo)
2. **plumbing-ghost** — Plumbing AI Receptionist ($1,200/mo)
3. **roofing-ghost** — Roofing AI Receptionist ($1,800/mo)
4. **electrical-ghost** — Electrical AI Receptionist ($1,200/mo)
5. **locksmith-ghost** — Locksmith AI Receptionist ($800/mo)
6. **towing-ghost** — Towing AI Receptionist ($900/mo)
7. **dubai-voice** — Trilingual Real Estate Concierge ($2,000/mo)
8. **micro-saas** — ReviewReply AI Review Responses ($49-$199/mo)

### WIP
- **gumroad-tracker** — Notion Sales Sync (internal tool)

## Revenue Projection

| Campaign | Customers | Setup | MRR M1 | Year Total |
|----------|-----------|-------|--------|------------|
| locksmith-ghost | 6 | $6,000 | $4,800 | $22,800 |
| towing-ghost | 5 | $6,000 | $4,500 | $19,500 |
| plumbing-ghost | 4 | $6,000 | $4,800 | $18,000 |
| electrical-ghost | 4 | $6,000 | $4,800 | $18,000 |
| roofing-ghost | 3 | $6,000 | $5,400 | $16,800 |
| ghost-systems | 3 | $4,500 | $3,600 | $11,700 |
| micro-saas | 4 | $0 | $396 | $990 |
| dubai-voice | 0 | $0 | $0 | $0 |
| **TOTAL** | | | | **$107,790** |

## External Setup Required

Before launching, configure:

- [ ] **Vapi**: dashboard.vapi.ai → upload `vapi_assistant.json` → buy phone number ($1/mo)
- [ ] **SendGrid**: verify domain → add API key → update `.env`
- [ ] **Stripe**: connect account → add `STRIPE_SECRET_KEY` → test checkout
- [ ] **Google Places API**: add key to `ghost-systems/.env` for real leads
- [ ] **Cloudflare / Vercel**: deploy landing pages
- [ ] **Telegram**: @BotFather → get token → set webhook to `http://your-server:8004/webhook/telegram`
- [ ] **Calendly**: set booking link across all campaigns
- [ ] **Domain**: buy `tryghostsystems.com`, `reviewreply.io`, etc.

## Architecture

```
Campaigns/
├── ghost-systems/          # HVAC AI Receptionist
│   ├── backend/            # FastAPI + SQLite
│   ├── leads/              # 50 leads
│   ├── outbox/             # 74 emails
│   ├── followups/          # 222 follow-ups
│   ├── quotes/             # 70 proposals
│   ├── vapi_assistant.json # Voice agent config
│   ├── contract.md         # Service agreement
│   └── loom_script.md      # Demo video script
├── dubai-voice/            # Dubai real estate
├── micro-saas/             # ReviewReply SaaS
├── gumroad-tracker/        # Notion sync
├── crm/                    # Unified CRM
├── ab_tests/               # A/B test emails
├── content/                # Blog + social posts
├── index.html              # War Room dashboard
├── campaigns-cli           # Service manager
├── revenue_calculator.py   # Revenue model
├── market_map.py           # Opportunity scoring
├── weekly_planner.py       # Execution planner
└── docker-compose.yml      # One-command deploy
```

## Auto-Start on Boot

All services are enabled via systemd user units. They start automatically on login.

```bash
systemctl --user enable ghost-api dubai-api gumroad-api crm-api campaign-dashboard saas-landing telegram-bot gateway
```

## License
Proprietary — Ghost Systems / Sahil Khan
