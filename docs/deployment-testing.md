# Deployment Testing Report

Live deployment health verification for VN Portfolio Optimizer.

**App URL:** [mctgiangproject1.streamlit.app](https://mctgiangproject1.streamlit.app)  
**Status Page:** [stats.uptimerobot.com/spxJeakm9r](https://stats.uptimerobot.com/spxJeakm9r)  
**Testing Date:** 2026-08-21  
**Testing Environment:** Windows 11, Chrome DevTools

---

## Monitoring Setup

**Tool:** UptimeRobot (Free tier)

**Configuration:**
- Monitor type: HTTP(S) HEAD request
- Check interval: 5 minutes
- Alert: Email notifications to maintainer
- Expected status: 2xx-3xx (includes redirects)
- Follow redirections: Enabled

**Public status page** shared for transparency.

---

## Browser Compatibility

Tested on Windows 11:

| Browser | Version | Result | Notes |
|---------|---------|--------|-------|
| Chrome | Latest | ✅ Pass | All features work as expected |
| Edge | Latest | ✅ Pass | All features work as expected |

**Not tested:** Firefox, Safari (limited by test environment - macOS/iOS unavailable)

---

## Mobile Responsiveness

Tested via Chrome DevTools device emulation:

| Device | Viewport | Result | Notes |
|--------|----------|--------|-------|
| iPhone 12 Pro | 390 × 844 | ✅ Pass | Responsive layout, all controls accessible |
| Samsung Galaxy S20 Ultra | 412 × 915 | ✅ Pass | Charts scale correctly |
| iPad Air | 820 × 1180 | ✅ Pass | Full desktop-like experience |

**Streamlit's built-in responsive design handles mobile well.**

---

## Network Resilience

Tested via Chrome DevTools network throttling:

| Network | DOMContentLoaded | Full Load | Finish | Verdict |
|---------|------------------|-----------|--------|---------|
| 3G | 19.8s | 1.4 min | 3.4 min | ✅ Eventually loads |

**Data transfer:** 822 KB compressed / 6.9 MB total (compression working)

**Analysis:** 3G users experience slow initial load but app remains functional. 
Not the primary use case (Vietnamese urban users mostly on 4G/WiFi).

---

## Cold Start Behavior

Streamlit Cloud puts apps to sleep after inactivity period.

**Not tested in this session** (app was already warm during testing window).

**Expected behavior:** 30-90 seconds cold start on first access after sleep. 
Users clicking demo link may experience this delay.

**Mitigation options (deferred):**
- Streamlit Cloud paid tier: no sleep
- Uptime pinger keeping app warm (requires 5-min pings)
- Alternative: accept cold start as free tier trade-off

---

## Known Limitations

- **Free tier constraints:** 5-minute monitor interval, no SMS alerts
- **Cold starts:** Unavoidable on Streamlit Cloud free tier
- **Browser coverage:** Firefox and Safari not tested (test environment limitation)
- **Load testing:** Not performed (research project scope, low concurrent users)

---

## Ongoing Monitoring

**Alert triggers:**
- App returns non-2xx/3xx HTTP status
- App does not respond within timeout period
- Consecutive check failures

**Notification channels:**
- Email: maintainer receives immediate alert
- Status page: public visibility of incidents

**Incident response:**
- Check Streamlit Cloud dashboard for deployment errors
- Verify GitHub Actions CI status (recent broken commits?)
- Review Streamlit logs for runtime errors

---

## Verification Checklist

- [x] UptimeRobot monitor active
- [x] Email alert tested (Test notification received)
- [x] Public status page created and linked
- [x] README badges include status page link
- [x] Documentation section references status page
- [x] Cross-browser testing completed (Chrome, Edge)
- [x] Mobile responsiveness verified (3 device sizes)
- [x] Slow network resilience confirmed (3G)

**Last verified:** 2026-08-26