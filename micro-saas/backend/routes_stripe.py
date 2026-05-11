#!/usr/bin/env python3
"""Stripe routes for ReviewReply backend."""
from fastapi import APIRouter, Request, HTTPException
from stripe_integration import create_checkout_session, handle_webhook

router = APIRouter(prefix="/stripe")

@router.post("/checkout")
async def checkout(request: Request):
    body = await request.json()
    return create_checkout_session(body["plan"], body.get("email", ""))

@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    return handle_webhook(payload, sig)
