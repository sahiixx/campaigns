#!/bin/bash
# Campaign War Room — Local Launch Script
# Starts: Ghost backend, Dashboard server, ReviewReply preview

cd "$(dirname "$0")"
echo "========================================"
echo "  CAMPAIGN WAR ROOM — LOCAL LAUNCH"
echo "========================================"

# 1. Ghost Systems Backend
if ! lsof -i:8000 >/dev/null 2>&1; then
    echo "[1/3] Starting Ghost Systems API on :8000 ..."
    cd ghost-systems/backend
    /home/sahiix/workspace/sovereign_swarm_enhanced/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 &
    cd ../..
    sleep 2
else
    echo "[1/3] Ghost API already running on :8000"
fi

# 2. Campaign Dashboard
if ! lsof -i:3000 >/dev/null 2>&1; then
    echo "[2/3] Starting War Room Dashboard on :3000 ..."
    python3 -m http.server 3000 &
    sleep 1
else
    echo "[2/3] Dashboard already running on :3000"
fi

# 3. ReviewReply Landing Page
if ! lsof -i:8080 >/dev/null 2>&1; then
    echo "[3/3] Starting ReviewReply preview on :8080 ..."
    cd micro-saas && python3 -m http.server 8080 &
    cd ..
    sleep 1
else
    echo "[3/3] ReviewReply already running on :8080"
fi

echo ""
echo "All services up:"
echo "  Ghost API      http://localhost:8000"
echo "  Dashboard      http://localhost:3000/index.html"
echo "  ReviewReply    http://localhost:8080/landing.html"
echo ""
echo "Stop all: pkill -f 'http.server|uvicorn main:app'"
