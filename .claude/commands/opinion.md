# AI Second Opinion on Trades

Get AI analysis and validation before executing a trade. Helps avoid emotional decisions and identifies blind spots.

## Arguments
- `$ARGUMENTS` - Trade you're considering: `buy CBA` or `sell BHP`

## Examples
```
/opinion buy CBA at 108
/opinion sell BHP
/opinion add to NAB
/opinion should I buy CSL?
/opinion is WES a good buy right now?
```

## Instructions

Before the user commits to a trade, provide comprehensive AI analysis.

### 1. Gather Context

**For the stock:**
- Current price (via yfinance)
- Key fundamentals (P/E, dividend yield, market cap)
- Recent performance (1 week, 1 month, YTD)
- Distance from 52-week high/low
- Recent news (web search)

**For the portfolio:**
- Load `data/portfolio.json` - current state
- Load `data/positions.json` - existing positions
- Load `data/trades.json` - trading history
- Load `data/journal/entries/*.json` - past trades in this stock
- Load `config/trading-rules.json` - position limits

**For research:**
- Load `data/research/[TICKER].json` if exists
- Check `data/watchlist.json` for notes

### 2. Generate Analysis

```
═══════════════════════════════════════════════════════════
AI SECOND OPINION: [BUY/SELL] [TICKER]
═══════════════════════════════════════════════════════════

📊 STOCK SNAPSHOT
─────────────────
[TICKER] - [Company Name]
Current Price:    $108.75
Day Change:       +1.2%
52-Week Range:    $95.20 - $115.50 (currently 85th percentile)
P/E Ratio:        15.2 (sector avg: 14.5)
Dividend Yield:   4.2%
Market Cap:       $175B

📈 RECENT PERFORMANCE
─────────────────────
1 Week:   +2.5%
1 Month:  +5.8%
YTD:      +12.3%
vs ASX200: Outperforming by 3.1%

🎯 BULL CASE (Reasons to proceed)
─────────────────────────────────
1. [Strong fundamental reason]
2. [Technical/momentum reason]
3. [Sector/macro reason]
4. [Valuation reason]

⚠️ BEAR CASE (Reasons for caution)
──────────────────────────────────
1. [Key risk or concern]
2. [Valuation concern if applicable]
3. [Sector/macro headwind]
4. [Technical warning if applicable]

📰 RECENT NEWS
──────────────
• [Headline 1] - [Brief impact assessment]
• [Headline 2] - [Brief impact assessment]
• [Headline 3] - [Brief impact assessment]

💼 PORTFOLIO FIT
────────────────
Current Exposure:     [0% / already hold X shares]
After Trade:          [X% of portfolio]
Sector Allocation:    Financials will be [X%] (limit: 30%)
Position Size Check:  [✅ Within limits / ⚠️ Exceeds X% limit]
Correlation:          [Low/Medium/High] with existing holdings

📜 YOUR HISTORY WITH THIS STOCK
───────────────────────────────
Previous Trades:
• [Date]: Bought at $X, Sold at $Y (+/-Z%)
• [Date]: ...

Journal Notes:
• "[Previous reasoning and lessons]"

🎲 AI PROBABILITY ASSESSMENT
────────────────────────────
Probability of Profit (6 months): [65%]
Expected Return Range: [-8% to +15%]
Risk/Reward Ratio: [1:1.8]

Confidence Level: [HIGH/MEDIUM/LOW]
Reasoning: [Why this confidence level]

✅ AI RECOMMENDATION
────────────────────
[PROCEED / PROCEED WITH CAUTION / RECONSIDER / AVOID]

[2-3 sentence summary of recommendation with specific reasoning]

💡 SUGGESTIONS
──────────────
• [Specific suggestion, e.g., "Consider waiting for pullback to $105"]
• [Position sizing suggestion, e.g., "Start with half position"]
• [Risk management, e.g., "Set stop-loss at $100 (8% below)"]

═══════════════════════════════════════════════════════════
```

### 3. Special Considerations

**For BUY opinions:**
- Check if better entry points exist
- Suggest scaling in vs all-at-once
- Recommend stop-loss level
- Check for upcoming events (earnings, ex-div)

**For SELL opinions:**
- Check if thesis is still valid
- Consider tax implications (holding period)
- Evaluate partial vs full sale
- Check for upcoming dividends

**For ADD TO POSITION:**
- Calculate new average cost
- Evaluate "throwing good money after bad" risk
- Check concentration limits

### 4. Save Opinion

Save to `data/opinions/[TICKER]-[DATE].json` for tracking whether AI opinions were followed and their accuracy over time.

### 5. Follow-Up

After providing opinion, offer:
```
What would you like to do?
• /trade buy [TICKER] [quantity] [price] - Proceed with trade
• /allocate [TICKER] [%] - Calculate position size
• /research [TICKER] - Deep dive research
• /watchlist add [TICKER] - Add to watchlist and wait
```
