#!/bin/bash
# Campaign Deploy Script
set -e

cd "$(dirname "$0")"
echo "========================================"
echo "  CAMPAIGN DEPLOYMENT PIPELINE"
echo "========================================"

# 1. ReviewReply → Cloudflare Pages
if command -v npx >/dev/null 2>&1; then
    echo ""
    echo "[1/3] Deploy ReviewReply to Cloudflare Pages..."
    echo "  Running: npx wrangler pages deploy micro-saas/"
    echo "  (You will be prompted to login if not authenticated)"
    npx wrangler pages deploy micro-saas/ --project-name reviewreply-landing || echo "  ⚠️  ReviewReply deploy failed — check wrangler auth"
else
    echo "  ⚠️  npx not available — cannot deploy ReviewReply"
fi

# 2. Ghost Systems Backend → Render (via Docker)
if command -v docker >/dev/null 2>&1; then
    echo ""
    echo "[2/3] Building Ghost Systems backend image..."
    cd ghost-systems/backend
    docker build -t ghost-systems-api:latest .
    echo "  Image built. Push to Render/Railway manually or run:"
    echo "    docker run -p 8000:8000 ghost-systems-api:latest"
    cd ../..
else
    echo "  ⚠️  Docker not available — skipping backend build"
fi

# 3. Dubai Voice Backend
if command -v docker >/dev/null 2>&1; then
    echo ""
    echo "[3/3] Building Dubai Voice backend image..."
    cd dubai-voice/backend
    docker build -t dubai-voice-api:latest .
    cd ../..
fi

echo ""
echo "========================================"
echo "  DEPLOY COMPLETE (or ready to push)"
echo "========================================"
echo ""
echo "Manual steps still needed:"
echo "  [ ] Cloudflare: npx wrangler login"
echo "  [ ] Render: connect GitHub repo at render.com"
echo "  [ ] Vapi: upload vapi_assistant.json + buy number"
echo "  [ ] SendGrid: verify domain + get API key"
echo "  [ ] Stripe: connect account for ReviewReply billing"
