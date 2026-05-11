#!/bin/bash
# Cloudflare Tunnel launcher (requires `cloudflared tunnel login` first)
TUNNEL_DIR="$HOME/.cloudflared"

echo "========================================"
echo "  CLOUDFLARE TUNNEL SETUP"
echo "========================================"
echo ""
echo "This creates public URLs for your local services."
echo ""
echo "Step 1: Authenticate (one-time)"
echo "  /tmp/cloudflared tunnel login"
echo ""
echo "Step 2: Create a tunnel"
echo "  /tmp/cloudflared tunnel create campaigns"
echo ""
echo "Step 3: Route traffic"
echo "  /tmp/cloudflared tunnel route dns campaigns campaigns.yourdomain.com"
echo ""
echo "Step 4: Run tunnel with config:"
cat << 'INNEREOF'
# ~/.cloudflared/config.yml
tunnel: <TUNNEL_ID>
credentials-file: ~/.cloudflared/<TUNNEL_ID>.json
ingress:
  - hostname: ghost.yourdomain.com
    service: http://localhost:8000
  - hostname: dubai.yourdomain.com
    service: http://localhost:8002
  - hostname: dashboard.yourdomain.com
    service: http://localhost:3000
  - hostname: reviewreply.yourdomain.com
    service: http://localhost:8080
  - hostname: crm.yourdomain.com
    service: http://localhost:8005
  - service: http_status:404
