# Watchlist Management

Add, remove, or view stocks on your watchlist.

## Arguments
- `$ARGUMENTS` - Action and ticker: `add CBA`, `remove BHP`, `view`

## Examples
```
/watchlist add BHP 43.00      # Add BHP with target entry at $43
/watchlist add CBA            # Add CBA without target
/watchlist remove WES         # Remove WES from watchlist
/watchlist view               # Show full watchlist
/watchlist                    # Same as view
```

## Instructions

Parse action from `$ARGUMENTS`:

**For `add [ticker] [target_price?]`:**
1. Fetch current price using yfinance
2. Get company name and sector
3. Add to `data/watchlist.json`:
   ```json
   {
     "ticker": "BHP.AX",
     "company_name": "BHP Group Limited",
     "sector": "Materials",
     "added_date": "2025-12-26T00:00:00Z",
     "current_price": 45.50,
     "target_entry_price": 43.00,
     "priority": "MEDIUM",
     "research_status": "NOT_STARTED",
     "notes": ""
   }
   ```
4. Show confirmation with current vs target price

**For `remove [ticker]`:**
1. Remove from `data/watchlist.json`
2. Show confirmation

**For `view` or no arguments:**
1. Load `data/watchlist.json`
2. Fetch current prices for all items
3. Display table:

```
WATCHLIST
=========================================
TICKER  CURRENT   TARGET    STATUS
BHP     $45.50    $43.00    5.8% above target
CBA     $108.75   -         No target set
WES     $65.00    $62.00    At target!

Research Status:
- BHP: NOT_STARTED
- CBA: COMPLETED
- WES: IN_PROGRESS
```

4. Highlight any stocks at or below target entry price
