#!/usr/bin/env python3
"""Service Monitor — Polls all services every 60s, alerts via Telegram if down."""
import time, requests, os
from datetime import datetime

SERVICES = {
    "ghost-api": "http://localhost:8000",
    "dubai-api": "http://localhost:8002",
    "gumroad-api": "http://localhost:8003",
    "telegram-bot": "http://localhost:8004",
    "crm-api": "http://localhost:8005",
    "gateway": "http://localhost:8006",
    "dashboard": "http://localhost:3000/index.html",
    "saas-landing": "http://localhost:8080/landing.html",
}

def alert(msg):
    print(f"[ALERT] {datetime.now().isoformat()} {msg}")
    # In production: send Telegram message
    # bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    # if bot_token:
    #     requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
    #         json={"chat_id": os.getenv("ADMIN_CHAT_ID"), "text": msg})

def check():
    for name, url in SERVICES.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 200:
                alert(f"{name} returned HTTP {r.status_code}")
            else:
                print(f"[OK] {name}")
        except Exception as e:
            alert(f"{name} DOWN: {e}")

def main():
    print("Monitor started. Checking every 60s.")
    while True:
        check()
        time.sleep(60)

if __name__ == "__main__":
    main()
