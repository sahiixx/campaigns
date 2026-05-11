#!/usr/bin/env python3
"""Gumroad → Notion sync with real Notion API."""
import os, requests, json
from datetime import datetime

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
GUMROAD_KEY = os.getenv("GUMROAD_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID")

def get_gumroad_sales():
    url = "https://api.gumroad.com/v2/sales"
    r = requests.get(url, params={"access_token": GUMROAD_KEY})
    return r.json().get("sales", [])

def create_notion_page(sale):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Product": {"title": [{"text": {"content": sale.get("product_name", "Unknown")}}]},
            "Buyer": {"rich_text": [{"text": {"content": sale.get("email", "")}}]},
            "Price": {"number": float(sale.get("price", 0))},
            "Date": {"date": {"start": sale.get("created_at", datetime.utcnow().isoformat())}},
            "Status": {"select": {"name": sale.get("refunded", False) and "Refunded" or "Paid"}}
        }
    }
    r = requests.post(url, headers=headers, json=payload)
    return r.json()

def sync():
    sales = get_gumroad_sales()
    print(f"Found {len(sales)} Gumroad sales")
    for sale in sales:
        result = create_notion_page(sale)
        if result.get("object") == "page":
            print(f"  ✓ Synced: {sale.get('product_name')} — {sale.get('email')}")
        else:
            print(f"  ✗ Failed: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    if not all([NOTION_TOKEN, GUMROAD_KEY, NOTION_DB_ID]):
        print("Missing env vars. Set NOTION_TOKEN, GUMROAD_API_KEY, NOTION_DATABASE_ID")
        exit(1)
    sync()
