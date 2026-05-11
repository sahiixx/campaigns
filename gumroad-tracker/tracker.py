#!/usr/bin/env python3
"""Gumroad → Notion sync."""
import os, requests, json
from datetime import datetime

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
GUMROAD_KEY = os.getenv("GUMROAD_API_KEY")

def get_gumroad_sales():
    url = "https://api.gumroad.com/v2/sales"
    r = requests.get(url, params={"access_token": GUMROAD_KEY})
    return r.json().get("sales", [])

def sync_to_notion(sales):
    print(f"Syncing {len(sales)} sales to Notion...")
    # TODO: implement Notion pages/database API calls
    return True

if __name__ == "__main__":
    sales = get_gumroad_sales()
    sync_to_notion(sales)
