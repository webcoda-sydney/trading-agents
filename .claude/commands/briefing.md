# Daily AI Market Briefing

Generate a comprehensive morning briefing covering market conditions, portfolio impact, and what to watch today.

**⚠️ IMPORTANT**: Get the current date from the `<env>` block (`Today's date: YYYY-MM-DD`). Do NOT use your internal sense of time - it may be wrong due to training cutoff.

## Arguments
- `$ARGUMENTS` - Optional: `quick` for summary, `detailed` for full analysis

## Examples
```
/briefing              # Standard morning briefing
/briefing quick        # 2-minute summary
/briefing detailed     # Deep dive with extra context
```

## Instructions

Generate a comprehensive daily briefing by gathering and analysing:

### 1. Market Overview
Use web search to find:
- ASX futures / expected open
- Overnight US markets (S&P 500, NASDAQ, Dow)
- Asian markets (Hang Seng, Nikkei)
- Key commodities (Iron ore, Gold, Oil) - important for ASX
- AUD/USD movement
- Bond yields / interest rate news

### 2. Portfolio Impact Analysis
Load and analyse:
- `data/portfolio.json` - Current holdings
- `data/positions.json` - Position details
- `data/watchlist.json` - Stocks being monitored

For each holding:
- Check for overnight news or announcements
- Note any pre-market price movements
- Identify stocks likely to move today

### 3. Calendar Events
Check for today's:
- Earnings announcements from holdings or watchlist
- Ex-dividend dates
- AGMs or investor days
- Economic data releases (RBA, employment, GDP)
- Index rebalancing

### 4. News Scan
Search for recent news on:
- Each stock in portfolio
- Each stock in watchlist
- Sector-wide news affecting holdings
- Major ASX announcements

### 5. Generate Briefing

**Output Format:**

```
═══════════════════════════════════════════════════════════
DAILY MARKET BRIEFING - [Day, DD MMM YYYY]
═══════════════════════════════════════════════════════════

☀️ MARKET SNAPSHOT
──────────────────
ASX 200 Futures:    +0.3% (pointing to positive open)
US Markets:         S&P +0.5%, NASDAQ +0.8%, Dow +0.2%
Asian Markets:      Nikkei +0.4%, Hang Seng -0.2%

📦 COMMODITIES & CURRENCY
─────────────────────────
Iron Ore:    $108.50 (+1.2%) - Positive for BHP, RIO, FMG
Gold:        $2,650 (-0.3%)
Oil (Brent): $74.20 (+0.8%)
AUD/USD:     0.6520 (+0.2%)

📊 YOUR PORTFOLIO
─────────────────
Expected Impact: [POSITIVE/NEUTRAL/NEGATIVE]

Stocks to Watch Today:
• CBA - Trading ex-dividend today ($2.15 per share)
• BHP - Iron ore rally overnight, expect strength
• WES - No specific news

⚠️ ALERTS
─────────
• NAB approaching stop-loss ($31.50, current ~$31.80)
• BHP hit target price, consider taking profits

📅 TODAY'S CALENDAR
───────────────────
09:30 - RBA Interest Rate Decision
10:00 - CBA trading ex-dividend
14:00 - Employment data release

📰 KEY NEWS
───────────
• [Headline 1] - Impact: [Analysis]
• [Headline 2] - Impact: [Analysis]

🎯 ACTION ITEMS
───────────────
1. [Specific action based on analysis]
2. [Specific action based on analysis]
3. [Specific action based on analysis]

💡 AI INSIGHT
─────────────
[One paragraph of AI analysis synthesising all the above -
what does it all mean for your portfolio today?]

═══════════════════════════════════════════════════════════
```

### 6. Save Briefing
Save to `data/briefings/[YYYY-MM-DD].md` for historical reference.

### Quick Mode
If `quick` argument, provide condensed version:
- Market snapshot (3 lines)
- Portfolio impact (1 line)
- Top 3 things to watch
- 1 action item

### Detailed Mode
If `detailed` argument, add:
- Technical levels for each holding
- Deeper macro analysis
- Historical context
- Multiple scenario analysis
