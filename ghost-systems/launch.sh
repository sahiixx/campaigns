#!/bin/bash
# Ghost Systems — 48-Hour Launch Script
set -e

echo "🚀 Ghost Systems Campaign Launch"
echo "================================="

CITY=${1:-Phoenix}
LEADS_FILE="leads/${CITY,,}_hvac_leads.csv"

echo "📍 Target: $CITY"
echo "📄 Leads: $LEADS_FILE"

if [ ! -f "$LEADS_FILE" ]; then
    echo "❌ Leads not found. Generating..."
    python3 scraper.py "$CITY" 50
fi

HIGH_PAIN=$(awk -F, 'NR>1 && $15>=2 {count++} END {print count+0}' "$LEADS_FILE")
TOTAL=$(awk -F, 'NR>1 {count++} END {print count+0}' "$LEADS_FILE")

echo ""
echo "📊 Lead Summary:"
echo "   Total: $TOTAL"
echo "   High Pain (score 2-3): $HIGH_PAIN"
echo ""
echo "📝 Next Steps:"
echo "   1. Review email_template.md — personalize {{fields}}"
echo "   2. Record Loom video using loom_script.md"
echo "   3. Load leads into tracker.csv"
echo "   4. Send batch 1 (high-pain leads only)"
echo "   5. Reply to 'SEND VIDEO' within 5 minutes"
echo ""
echo "💰 Pricing:"
echo "   Setup: $1,500 (50% off pilot)"
echo "   Monthly: $1,200"
echo "   Guarantee: 3+ jobs in 30 days or free"
echo ""
echo "Ready. Go make money."
