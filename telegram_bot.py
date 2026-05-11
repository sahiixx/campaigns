#!/usr/bin/env python3
"""Campaign Telegram Bot — Webhook handler for Hermes/Telegram integration.
Usage: Set BOT_TOKEN env var, run webhook server, point Telegram to /webhook/telegram
"""
from fastapi import FastAPI, Request
import os, requests, json
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
app = FastAPI(title="Campaign Telegram Bot")

def send_message(chat_id, text):
    if not BOT_TOKEN:
        return {"error": "No BOT_TOKEN"}
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    return requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).json()

def get_ghost_stats():
    try:
        r = requests.get("http://localhost:8000/appointments", timeout=5)
        appts = r.json()
        return f"📞 *Ghost Systems*\nAppointments: {len(appts)}\nLast: {appts[0]['customer_name'] if appts else 'None'}"
    except Exception as e:
        return f"📞 *Ghost Systems*\nError: {e}"

def get_dubai_stats():
    try:
        r = requests.get("http://localhost:8002/viewings", timeout=5)
        views = r.json()
        return f"🏙️ *Dubai Voice*\nViewings: {len(views)}\nLast: {views[0]['customer_name'] if views else 'None'}"
    except Exception as e:
        return f"🏙️ *Dubai Voice*\nError: {e}"

def get_revenue():
    try:
        with open("revenue_projection.json") as f:
            data = json.load(f)
        return f"💰 *Revenue Projection*\nYear 1 Total: ${data['total_year_1']:,}\nTop Campaign: {data['campaigns'][0]['name']}"
    except:
        return "💰 Revenue data unavailable"

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    body = await request.json()
    msg = body.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "").strip().lower()
    
    if text == "/start":
        send_message(chat_id, "🚀 *Campaign War Room Bot*\nCommands:\n/status — All campaigns\n/ghost — Ghost Systems stats\n/dubai — Dubai Voice stats\n/revenue — Revenue projection\n/help — This message")
    elif text == "/status":
        ghost = get_ghost_stats()
        dubai = get_dubai_stats()
        rev = get_revenue()
        send_message(chat_id, f"{ghost}\n\n{dubai}\n\n{rev}")
    elif text == "/ghost":
        send_message(chat_id, get_ghost_stats())
    elif text == "/dubai":
        send_message(chat_id, get_dubai_stats())
    elif text == "/revenue":
        send_message(chat_id, get_revenue())
    elif text == "/help":
        send_message(chat_id, "Commands: /start /status /ghost /dubai /revenue /help")
    else:
        send_message(chat_id, f"Unknown command: {text}\nTry /help")
    
    return {"ok": True}

@app.get("/")
def home():
    return {"status": "Campaign Telegram Bot", "webhook": "/webhook/telegram"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
