#!/usr/bin/env python3
"""ReviewReply Backend — OAuth, Stripe, OpenAI integration scaffold"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import os, json

app = FastAPI(title="ReviewReply API")

# In production, load from env
STRIPE_PK = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_...")
STRIPE_SK = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "sk-...")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

@app.get("/")
def home():
    return {"status": "ReviewReply API", "version": "0.1.0"}

@app.get("/config")
def config():
    """Public config for frontend."""
    return {"stripe_pk": STRIPE_PK, "google_client_id": GOOGLE_CLIENT_ID}

@app.post("/stripe/create-checkout")
def create_checkout():
    # TODO: integrate Stripe Checkout Session
    return {"url": "https://checkout.stripe.com/pay/cs_test_..."}

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    # TODO: verify signature, update subscription status
    return {"received": True}

@app.get("/auth/google/callback")
def google_auth_callback(code: str):
    # TODO: exchange code for tokens, fetch Google Business reviews
    return {"code": code, "status": "auth_received"}

@app.post("/reviews/generate-response")
async def generate_response(request: Request):
    body = await request.json()
    review_text = body.get("review_text", "")
    rating = body.get("rating", 5)
    # TODO: call OpenAI with brand voice prompt
    return {
        "review_text": review_text,
        "rating": rating,
        "generated_response": f"Thank you for your feedback! We're thrilled to hear about your experience and look forward to serving you again."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
