# AI Trade Journal & Coach

Record trade decisions, track outcomes, and get AI coaching to improve your trading.

## Arguments
- `$ARGUMENTS` - Action: `add`, `review`, `analyse`, `lessons`

## Examples
```
/journal add CBA "Bought because banks look undervalued, expecting rate cuts to help"
/journal review              # Review recent trades and outcomes
/journal analyse             # AI analysis of your trading patterns
/journal lessons             # Key lessons learned from your trades
/journal                     # Show journal summary
```

## Instructions

### For `add [ticker] "[reasoning]"`:

1. Load latest trade for that ticker from `data/trades.json`
2. Create journal entry in `data/journal/entries/[trade_id].json`:

```json
{
  "trade_id": "T20250115-001",
  "ticker": "CBA.AX",
  "action": "BUY",
  "entry_date": "2025-01-15",
  "entry_price": 105.50,
  "quantity": 100,
  "reasoning": "User's reasoning here",
  "thesis": {
    "timeframe": "medium-term",
    "catalyst": "RBA rate cuts expected",
    "target_return": "10-15%",
    "risk_level": "medium"
  },
  "pre_trade_emotions": "",
  "market_conditions": "ASX up 0.5%, sector neutral",
  "ai_assessment": {
    "strengths": ["Clear thesis", "Defined catalyst"],
    "concerns": ["Sector concentration risk"],
    "probability_of_success": "65%",
    "suggestion": "Consider scaling in rather than full position"
  },
  "outcome": null,
  "lessons_learned": null,
  "closed_date": null
}
```

3. Provide AI assessment of the trade reasoning:
   - Is the thesis clear and testable?
   - What could go wrong?
   - Position sizing appropriate?
   - Emotional state check

### For `review`:

1. Load all journal entries from `data/journal/entries/`
2. Cross-reference with current positions and closed trades
3. Update outcomes for closed positions
4. Display:

```
TRADE JOURNAL REVIEW
════════════════════

OPEN POSITIONS
──────────────
CBA (Bought 15/01/2025 @ $105.50)
  Reasoning: "Banks undervalued, rate cuts coming"
  Current: $108.75 (+3.1%)
  Thesis Status: ✅ On track - RBA signalling cuts
  AI Notes: Thesis playing out, consider taking partial profits

BHP (Bought 20/01/2025 @ $44.00)
  Reasoning: "Iron ore demand recovery"
  Current: $43.50 (-1.1%)
  Thesis Status: ⚠️ Uncertain - China data mixed
  AI Notes: Give it more time, thesis not invalidated

RECENTLY CLOSED
───────────────
WES (Sold 10/01/2025)
  Result: +$450 (+8.5%)
  Held: 45 days
  Original Thesis: "Retail recovery play"
  Outcome: ✅ WIN - Thesis correct
  Lesson: Retail sector can move fast post-earnings

JOURNAL STATS
─────────────
Total Journaled Trades: 15
Win Rate: 67%
Average Winner: +12.3%
Average Loser: -6.2%
Best Trade: CSL +22% (held 90 days)
Worst Trade: ORG -11% (stopped out)
```

### For `analyse`:

Deep AI analysis of trading patterns:

```
TRADING PATTERN ANALYSIS
════════════════════════

🧠 BEHAVIOURAL PATTERNS DETECTED
────────────────────────────────
1. SELLING WINNERS TOO EARLY
   You've sold 4 positions within 2 weeks of buying that later
   went up another 10%+. Consider using trailing stops instead.

2. AVERAGING DOWN ON LOSERS
   You added to 2 losing positions. One worked out, one didn't.
   Your win rate on averaging down: 50%

3. SECTOR CONCENTRATION
   70% of your trades are in Financials. Consider diversifying.

📊 WHAT'S WORKING
─────────────────
• Value investing thesis: 75% win rate
• Trades held >30 days: 80% winners
• Morning entries: Better than afternoon

📉 WHAT'S NOT WORKING
─────────────────────
• Momentum trades: Only 40% win rate
• Trades held <7 days: 45% winners
• FOMO entries (after big moves): 30% win rate

💡 AI RECOMMENDATIONS
─────────────────────
1. Extend your holding period - your best trades took time
2. Avoid chasing momentum - not your strength
3. Stick to value/quality - that's where you shine
4. Add a cooling off period before FOMO trades
```

### For `lessons`:

Extract and display key lessons:

```
KEY LESSONS FROM YOUR TRADING
═════════════════════════════

✅ LESSONS THAT MADE YOU MONEY
──────────────────────────────
1. "Patience pays - my best trades were held 60+ days"
2. "Banks bounce hard after bad news is priced in"
3. "Earnings beats in quality stocks are worth holding through"

❌ EXPENSIVE LESSONS LEARNED
────────────────────────────
1. "Don't chase stocks up 10% in a day" (-$340 on ORG)
2. "Set stop losses and stick to them" (-$520 on WTC)
3. "Averaging down rarely works for me" (-$280 on STO)

📝 YOUR TRADING RULES (AI-GENERATED)
────────────────────────────────────
Based on your journal, these rules would improve results:
1. Only buy stocks you've researched for 24+ hours
2. Never chase >5% daily moves
3. Hold winners for minimum 30 days
4. Maximum 25% in any sector
5. Always set stop-loss at entry
```

### Data Storage

Create directory structure:
- `data/journal/entries/` - Individual trade journals
- `data/journal/analysis/` - AI analysis reports
- `data/journal/lessons.json` - Accumulated lessons
