# Natural Language Portfolio Queries

Ask questions about your portfolio in plain English. AI interprets and answers.

## Arguments
- `$ARGUMENTS` - Your question in natural language

## Examples
```
/ask What's my best performer this month?
/ask How much am I up on banks?
/ask Which stocks are near their stop-loss?
/ask When do my holdings pay dividends?
/ask What's my total dividend income this year?
/ask Show me stocks down more than 5%
/ask How diversified am I by sector?
/ask What would happen if the market dropped 10%?
/ask Which stocks should I be worried about?
/ask Am I overweight in any sector?
```

## Instructions

Parse the natural language query and provide intelligent answers by loading relevant data files.

### Data Sources to Query

1. **Portfolio State**: `data/portfolio.json`
2. **Positions**: `data/positions.json`
3. **Trades**: `data/trades.json`
4. **Watchlist**: `data/watchlist.json`
5. **Research**: `data/research/*.json`
6. **Performance**: `data/performance/returns-history.json`
7. **Price Snapshots**: `data/price-snapshots/*.json`
8. **Journal**: `data/journal/entries/*.json`
9. **Fundamentals**: `data/fundamentals-cache.json`
10. **Trading Rules**: `config/trading-rules.json`

### Query Categories

**Performance Queries:**
- "best/worst performer" → Sort positions by P&L %
- "how much am I up/down" → Calculate total or filtered P&L
- "returns this week/month/year" → Time-based performance

**Position Queries:**
- "show me [sector] stocks" → Filter by sector
- "stocks near stop-loss" → Compare price to stop levels
- "stocks at target" → Compare to target prices
- "largest/smallest positions" → Sort by value or weight

**Dividend Queries:**
- "dividend income" → Sum dividend field from positions
- "next dividends" → Use web search for upcoming ex-dates
- "dividend yield" → Calculate portfolio yield

**Risk Queries:**
- "sector breakdown" → Group positions by sector
- "overweight/underweight" → Compare to rules
- "what if market drops X%" → Stress test calculation
- "correlation" → Analyse sector/stock correlation

**Trade Queries:**
- "recent trades" → Last N trades
- "winning/losing trades" → Filter by outcome
- "average hold time" → Calculate from trades

**Watchlist Queries:**
- "watchlist status" → Show watchlist with current prices
- "stocks near entry" → Close to target entry price

### Response Format

```
📊 YOUR QUESTION
────────────────
"[Original question]"

💡 ANSWER
─────────
[Direct answer to the question]

📈 DETAILS
──────────
[Supporting data, tables, or breakdown as needed]

[Only if relevant:]
💭 AI INSIGHT
─────────────
[Additional context or suggestions based on the query]
```

### Example Responses

**Query: "What's my best performer this month?"**
```
📊 YOUR QUESTION
────────────────
"What's my best performer this month?"

💡 ANSWER
─────────
BHP is your best performer this month at +8.5%

📈 TOP 5 THIS MONTH
───────────────────
1. BHP   +8.5%  (+$425)
2. CBA   +3.2%  (+$305)
3. NAB   +2.1%  (+$95)
4. WES   -0.5%  (-$45)
5. CSL   -1.2%  (-$180)

💭 AI INSIGHT
─────────────
BHP is benefiting from the iron ore rally. Consider
whether to take partial profits given it's now 12%
of your portfolio.
```

**Query: "Am I overweight in any sector?"**
```
📊 YOUR QUESTION
────────────────
"Am I overweight in any sector?"

💡 ANSWER
─────────
Yes - Financials at 42% exceeds your 30% limit.

📈 SECTOR ALLOCATION
────────────────────
Financials:   42% ⚠️ OVERWEIGHT (limit: 30%)
Materials:    25% ✅
Healthcare:   15% ✅
Consumer:     10% ✅
Cash:          8% ✅

💭 AI INSIGHT
─────────────
Consider trimming CBA or NAB to reduce Financials
exposure. Both are up nicely - good time to rebalance.
```

### Handling Unknown Queries

If the query can't be answered from available data:
1. Explain what data would be needed
2. Suggest alternative questions
3. Offer to fetch external data if appropriate
