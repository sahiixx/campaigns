# Email Deliverability Setup — Ghost Systems

Without proper DNS records, your cold emails land in spam. Set these up BEFORE sending.

## 1. Domain
Buy a dedicated domain for cold email (never use your main domain).
- `ghostsystems.io` → main site
- `tryghostsystems.com` → cold email domain

## 2. DNS Records (add at your registrar/Cloudflare)

### SPF
```
Type: TXT
Name: @
Value: v=spf1 include:sendgrid.net include:_spf.google.com ~all
```

### DKIM (SendGrid)
1. Go to SendGrid → Settings → Sender Authentication → Domain Authentication
2. Enter `tryghostsystems.com`
3. Add CNAME records they provide
4. Validate

### DMARC
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@tryghostsystems.com; pct=100
```

### Custom Tracking (optional)
```
Type: CNAME
Name: s1._domainkey
Value: s1.domainkey.u12345.wl123.sendgrid.net
```

## 3. Warm-up Schedule

| Day | Volume |
|-----|--------|
| 1-3 | 5 emails/day |
| 4-7 | 10 emails/day |
| 8-14 | 20 emails/day |
| 15-21 | 35 emails/day |
| 22-30 | 50 emails/day |

Never send more than 50/day from a new domain.

## 4. Content Rules
- No images in first email (triggers spam filters)
- No more than 1 link
- Avoid: "free", "guarantee", "$$$", ALL CAPS
- Plain text > HTML for cold outreach
- Keep subject under 50 characters

## 5. Inbox Placement Test
Before bulk send, test with:
- mail-tester.com
- glockapps.com
- send a test to your own Gmail + Outlook

## 6. Reputation Monitoring
- Google Postmaster Tools (postmaster.google.com)
- Microsoft SNDS (sendersupport.olc.protection.outlook.com)

## 7. Tools
- **SendGrid:** $19.95/mo for 50K emails (plenty)
- **Instantly.ai:** $37/mo for unlimited warm-up + scheduling
- **Smartlead:** $34/mo for multi-inbox rotation

---

Ready to send? Run:
```bash
export SMTP_HOST=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USER=apikey
export SMTP_PASS=SG.xxx
export FROM_EMAIL=hello@tryghostsystems.com
python send_live.py --live
```
