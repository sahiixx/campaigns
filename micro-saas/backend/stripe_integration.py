#!/usr/bin/env python3
"""Stripe Checkout integration for ReviewReply."""
import os, stripe
from fastapi import Request

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

PRICES = {
    "starter": {"monthly": 4900, "name": "Starter"},
    "growth": {"monthly": 9900, "name": "Growth"},
    "agency": {"monthly": 19900, "name": "Agency"}
}

def create_checkout_session(plan: str, customer_email: str):
    price_cents = PRICES[plan]["monthly"]
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": f"ReviewReply {PRICES[plan]['name']}"},
                "unit_amount": price_cents,
                "recurring": {"interval": "month"}
            },
            "quantity": 1,
        }],
        mode="subscription",
        success_url="https://reviewreply.io/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://reviewreply.io/cancel",
        customer_email=customer_email,
        metadata={"plan": plan}
    )
    return {"url": session.url, "session_id": session.id}

def handle_webhook(payload: bytes, sig: str):
    event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: activate subscription in database
        return {"status": "activated", "customer": session["customer_email"], "plan": session["metadata"]["plan"]}
    elif event["type"] == "invoice.payment_failed":
        # TODO: notify customer of failed payment
        return {"status": "payment_failed"}
    return {"status": "ignored"}
