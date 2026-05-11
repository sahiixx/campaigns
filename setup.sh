#!/bin/bash
# Campaign War Room — One-Command Installer
set -e

echo "========================================"
echo "  CAMPAIGN WAR ROOM INSTALLER"
echo "========================================"

# 1. Install deps
sudo apt-get update && sudo apt-get install -y python3-pip python3-venv nodejs npm curl git sqlite3

# 2. Create venv
if [ ! -d "venv" ]; then
    echo "[1/5] Creating Python venv..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q fastapi uvicorn httpx requests

# 3. Install systemd services
mkdir -p ~/.config/systemd/user
cp *.service ~/.config/systemd/user/ 2>/dev/null || true
cp ghost-systems/backend/*.service ~/.config/systemd/user/ 2>/dev/null || true
cp dubai-voice/backend/*.service ~/.config/systemd/user/ 2>/dev/null || true
cp gumroad-tracker/backend/*.service ~/.config/systemd/user/ 2>/dev/null || true
cp crm/backend/*.service ~/.config/systemd/user/ 2>/dev/null || true

# Fix paths in service files
sed -i "s|/home/sahiix/workspace/sovereign_swarm_enhanced/venv|$PWD/venv|g" ~/.config/systemd/user/*.service
systemctl --user daemon-reload

# 4. Sync CRM
python3 crm/backend/main.py &
sleep 2
curl -s -X POST http://localhost:8005/sync >/dev/null || true
pkill -f "crm/backend/main.py" || true

# 5. Start services
echo "[2/5] Starting services..."
for svc in ghost-api dubai-api gumroad-api crm-api campaign-dashboard saas-landing telegram-bot gateway; do
    systemctl --user start $svc 2>/dev/null || echo "  $svc skipped"
done

# 6. Verify
echo "[3/5] Health check..."
sleep 2
for port in 8000 8002 8003 8004 8005 8006 3000 8080; do
    code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/ 2>/dev/null || echo "000")
    [ "$code" = "200" ] && echo "  Port $port: OK" || echo "  Port $port: FAIL"
done

echo ""
echo "[4/5] Install complete."
echo "[5/5] Open http://localhost:3000 for War Room dashboard."
echo ""
echo "Next steps:"
echo "  ./campaigns-cli status    # Check services"
echo "  ./campaigns-cli deploy    # Show deploy checklist"
echo "  python3 status.py         # Campaign readiness"
