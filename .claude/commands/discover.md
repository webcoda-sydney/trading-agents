# Stock Discovery

AI-powered stock discovery that analyses the market and recommends stocks to investigate.

## Arguments
- `$ARGUMENTS` - Investment goal or style (optional)

## Examples
```
/discover                    # General market analysis
/discover income             # Find income-generating stocks
/discover growth tech        # Growth stocks in tech sector
/discover defensive          # Low-volatility defensive plays
/discover beaten down        # Oversold recovery candidates
```

## Instructions

This command provides intelligent stock discovery by:

1. **Analyse Current Portfolio** (if positions exist)
   - Read `data/positions.json` for current holdings
   - Identify sector gaps and diversification opportunities
   - Note any overweight positions

2. **Run Multiple Screens**
   - Load `config/screening-presets.json`
   - Run 2-3 relevant screens based on user's goal
   - Cross-reference results to find stocks appearing in multiple screens

3. **Market Context** (use web-researcher if needed)
   - What sectors are performing well/poorly?
   - Any recent market themes or trends?
   - Economic conditions affecting certain sectors

4. **Generate Recommendations**
   Based on the analysis, provide:

```
STOCK DISCOVERY REPORT
======================
Goal: $ARGUMENTS (or "General Opportunity Scan")
Date: [today's date]

MARKET CONTEXT
--------------
[Brief 2-3 sentence market overview]

TOP RECOMMENDATIONS
-------------------

1. [TICKER] - [Company Name]
   Why: [2-3 bullet points on why this stock fits the criteria]
   Screen matches: value, quality
   Current price: $XX.XX
   Key metrics: P/E XX, Div Yield X.X%

2. [TICKER] - [Company Name]
   ...

3. [TICKER] - [Company Name]
   ...

SECTOR OPPORTUNITIES
--------------------
- [Sector]: [Brief thesis]
- [Sector]: [Brief thesis]

PORTFOLIO FIT
-------------
[Based on current holdings, explain how recommendations complement/diversify]

WATCHLIST CANDIDATES
--------------------
[List 5-7 additional stocks worth monitoring]

NEXT STEPS
----------
1. /research [TOP_PICK] - Deep dive on top recommendation
2. /watchlist add [TICKER] - Add candidates to watchlist
3. /allocate [TICKER] 5% - Calculate position size
```

5. **Save Discovery Report**
   - Save to `data/scan-results/discovery-[date].json`
   - Include all analysis and recommendations

**Key Principles:**
- Prioritise stocks NOT already in portfolio
- Consider correlation with existing holdings
- Balance risk across recommendations
- Provide actionable next steps
