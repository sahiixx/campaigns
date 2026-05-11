# Gumroad → Notion Sales Tracker

Auto-sync Gumroad sales to a Notion database for revenue tracking and cohort analysis.

## Setup
```bash
cp .env.example .env
# Edit .env with your tokens
pip install requests
python notion_sync.py
```

## Features
- Hourly sync from Gumroad API
- Auto-creates Notion pages with product, price, buyer, date, status
- Tracks refunds and disputes
- Revenue dashboard in Notion

## Cron (run every hour)
```bash
0 * * * * cd ~/campaigns/gumroad-tracker && /usr/bin/python3 notion_sync.py >> sync.log 2>&1
```
