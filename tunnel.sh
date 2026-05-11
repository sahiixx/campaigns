#!/bin/bash
# Launch all services + expose via localtunnel for instant demos
set -e
cd "$(dirname "$0")"

echo "========================================"
echo "  CAMPAIGN TUNNEL LAUNCHER"
echo "========================================"

# Kill existing
pkill -f "uvicorn main:app" 2>/dev/null || true
pkill -f "http.server" 2>/dev/null || true
sleep 1

# Start services
echo "[1/4] Starting Ghost API on :8000 ..."
cd ghost-systems/backend
/home/sahiix/workspace/sovereign_swarm_enhanced/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 &
GHOST_PID=$!
cd ../..
sleep 2

echo "[2/4] Starting Dubai API on :8002 ..."
cd dubai-voice/backend
/home/sahiix/workspace/sovereign_swarm_enhanced/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8002 &
DUBAI_PID=$!
cd ../..
sleep 2

echo "[3/4] Starting static dashboards on :3000 & :8080 ..."
python3 -m http.server 3000 &
DASH_PID=$!
cd micro-saas && python3 -m http.server 8080 &
SAAS_PID=$!
cd ..
sleep 1

echo "[4/4] Exposing tunnels (requires npx localtunnel) ..."
if command -v npx >/dev/null 2>&1; then
    npx localtunnel --port 8000 --subdomain ghost-$(date +%s) &
    npx localtunnel --port 3000 --subdomain warroom-$(date +%s) &
    npx localtunnel --port 8080 --subdomain reviewreply-$(date +%s) &
    echo ""
    echo "Tunnels launching... URLs will appear above."
else
    echo "  ⚠️  npx not available — install Node.js or run locally only"
fi

echo ""
echo "========================================"
echo "  LOCAL SERVICES"
echo "========================================"
echo "  Ghost API      http://localhost:8000"
echo "  Dubai API      http://localhost:8002"
echo "  War Room       http://localhost:3000/index.html"
echo "  ReviewReply    http://localhost:8080/landing.html"
echo "  Pricing        http://localhost:8080/pricing.html"
echo ""
echo "Press Ctrl+C to stop all services."
echo "========================================"

wait
