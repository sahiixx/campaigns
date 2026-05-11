# Gumroad Tracker Setup Checklist

- [ ] Create Notion integration at notion.so/my-integrations
- [ ] Create database with columns: Product (title), Buyer (rich_text), Price (number), Date (date), Status (select)
- [ ] Share database with integration
- [ ] Copy database ID from URL
- [ ] Get Gumroad API key from gumroad.com/settings
- [ ] Fill .env file
- [ ] Run `python notion_sync.py` to test
- [ ] Set up cron for hourly sync
