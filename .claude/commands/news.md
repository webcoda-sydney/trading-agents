# News & Sentiment Monitor

Monitor news and announcements for your holdings and watchlist. Get AI-powered sentiment analysis and alerts.

## Arguments
- `$ARGUMENTS` - Action or ticker: `scan`, `alerts`, `[ticker]`, `sentiment`

## Examples
```
/news                  # Scan news for all holdings
/news CBA              # News specifically for CBA
/news scan             # Full portfolio news scan
/news alerts           # Show triggered alerts
/news sentiment        # Sentiment overview for portfolio
/news watchlist        # News for watchlist stocks
```

## Instructions

### For no arguments or `scan`:

Comprehensive news scan for all holdings and watchlist.

1. **Gather Holdings**
   - Load `data/positions.json` for current holdings
   - Load `data/watchlist.json` for watched stocks

2. **Search News** (use web search)
   For each stock, search for:
   - "[Company name] ASX news"
   - "[Ticker] announcement"
   - Recent price-sensitive announcements

3. **Analyse Sentiment**
   For each news item:
   - Positive / Negative / Neutral
   - Materiality: High / Medium / Low
   - Likely price impact

4. **Generate Report**

```
═══════════════════════════════════════════════════════════
NEWS & SENTIMENT MONITOR
[Date and Time]
═══════════════════════════════════════════════════════════

🚨 ALERTS (Action Required)
───────────────────────────
⚠️ CBA - MATERIAL ANNOUNCEMENT
   "CBA announces $2.5B share buyback"
   Sentiment: POSITIVE | Impact: HIGH
   AI Take: Bullish signal, shows confidence. Your position
   should benefit.
   → Consider: Hold, potentially add on dips

⚠️ BHP - PRICE SENSITIVE
   "Iron ore production guidance lowered for Q2"
   Sentiment: NEGATIVE | Impact: MEDIUM
   AI Take: Short-term pressure likely, but long-term
   thesis intact.
   → Consider: Hold, monitor iron ore prices

📰 PORTFOLIO NEWS
─────────────────

CBA (You own 100 shares)
├─ "Big four banks to benefit from rate cuts" [POSITIVE]
├─ "CBA digital transformation on track" [POSITIVE]
└─ "Housing market shows signs of cooling" [NEUTRAL]
   Overall Sentiment: 🟢 POSITIVE

BHP (You own 50 shares)
├─ "China stimulus boosts commodity demand" [POSITIVE]
├─ "Iron ore prices stabilise above $100" [POSITIVE]
└─ "Production guidance lowered" [NEGATIVE]
   Overall Sentiment: 🟡 MIXED

NAB (You own 75 shares)
├─ "NAB business confidence survey released" [NEUTRAL]
└─ No material announcements
   Overall Sentiment: 🔵 NEUTRAL

👀 WATCHLIST NEWS
─────────────────

WES (On watchlist, target $62)
├─ "Bunnings sales growth slows" [NEGATIVE]
├─ "Kmart turnaround continues" [POSITIVE]
└─ Current price: $65.50 (5.6% above target)
   AI Take: Wait for your entry price

CSL (On watchlist)
├─ "CSL plasma collection reaches record levels" [POSITIVE]
└─ "FDA approves new product" [POSITIVE]
   AI Take: Strong momentum, but premium valuation

📊 PORTFOLIO SENTIMENT SUMMARY
──────────────────────────────
🟢 Positive:  3 stocks (CBA, FMG, RIO)
🟡 Mixed:     1 stock (BHP)
🔵 Neutral:   2 stocks (NAB, WES)
🔴 Negative:  0 stocks

Overall Portfolio Sentiment: POSITIVE
News-Based Outlook: BULLISH

💡 AI RECOMMENDATIONS
─────────────────────
1. CBA buyback is material - consider holding through it
2. Monitor BHP closely for production updates
3. WES approaching your target entry - prepare research

═══════════════════════════════════════════════════════════
```

### For specific ticker (`/news CBA`):

Deep dive on single stock:
- All recent news (past 7 days)
- ASX announcements
- Analyst commentary
- Social sentiment if available
- Detailed AI analysis

### For `alerts`:

Show alert configuration and triggered alerts:

```
NEWS ALERTS
═══════════

ALERT CONFIGURATION
───────────────────
[✓] Material announcements for holdings
[✓] Earnings releases
[✓] Dividend announcements
[✓] Director trades
[✓] Target price hits on watchlist
[ ] Broker upgrades/downgrades

RECENTLY TRIGGERED
──────────────────
🔔 CBA - Share buyback announced (2 hours ago)
🔔 BHP - Production guidance update (5 hours ago)
🔔 WES - Approaching target price (yesterday)
```

### For `sentiment`:

Portfolio-wide sentiment analysis:

```
PORTFOLIO SENTIMENT ANALYSIS
════════════════════════════

SENTIMENT SCORES (AI-Generated)
───────────────────────────────
Ticker  Score   Trend      Key Driver
CBA     +72     ↑ Rising   Buyback, rate cut hopes
BHP     +45     ↓ Falling  Production concerns
NAB     +55     → Stable   No major news
WES     +60     ↑ Rising   Kmart turnaround

SECTOR SENTIMENT
────────────────
Financials:  +65 (Positive)
Materials:   +48 (Neutral-Positive)
Consumer:    +58 (Positive)

NEWS VELOCITY
─────────────
High activity:  CBA (8 articles today)
Normal:         BHP, NAB (2-3 articles)
Quiet:          Others

AI MARKET READ
──────────────
Overall tone is cautiously optimistic. Banks leading
on rate cut expectations. Resources mixed on China
signals. Consumer holding up despite cost pressures.
```

### 5. Save News Log

Maintain rolling log in `data/news/[YYYY-MM-DD].json` for:
- Historical sentiment tracking
- Pattern recognition
- Alert history
