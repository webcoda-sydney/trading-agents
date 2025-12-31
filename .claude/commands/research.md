# Stock Research

Generate or view investment research for an ASX stock.

## Arguments
- `$ARGUMENTS` - Ticker symbol (e.g., CBA, BHP)

## Examples
```
/research CBA       # Generate research for Commonwealth Bank
/research BHP       # Generate research for BHP Group
```

## Instructions

For the ticker in `$ARGUMENTS`:

1. **Check if research exists**: Look for `data/research/[TICKER].json`

2. **If research exists and is recent (< 30 days):**
   - Display existing research summary
   - Ask if user wants to refresh

3. **If no research or refresh requested:**

   Use the web-researcher agent to gather:
   - Current stock price and key metrics
   - Company description and sector
   - Recent news and announcements
   - Analyst consensus (if available)

   Create research file with structure:
   ```json
   {
     "ticker": "CBA.AX",
     "company_name": "...",
     "analysis_date": "...",
     "recommendation": "BUY|HOLD|SELL",
     "target_price": 0.00,
     "investment_thesis": {
       "bull_case": [...],
       "bear_case": [...],
       "key_risks": [...]
     },
     "fundamentals": {
       "market_cap_aud": 0,
       "pe_ratio": 0,
       "dividend_yield": 0
     },
     "position_sizing": {
       "max_position_size_pct": 10.0,
       "suggested_entry": 0.00,
       "stop_loss": 0.00
     }
   }
   ```

4. **Display research summary:**
   - Recommendation with confidence level
   - Key bull/bear points
   - Suggested entry price and position size
   - Stop-loss level
