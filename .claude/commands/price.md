# Update Stock Prices

Fetch and update current prices for positions and/or watchlist.

## Arguments
- `$ARGUMENTS` - Either `--all`, a specific ticker, or blank for positions only

## Examples
```
/price              # Update all positions
/price --all        # Update positions AND watchlist
/price CBA          # Get price for specific ticker
```

## Instructions

Based on `$ARGUMENTS`:

**If blank or no arguments:**
1. Run `python scripts/update_prices.py`
2. Show updated positions with current prices and P&L
3. Show portfolio summary

**If `--all`:**
1. Run `python scripts/update_prices.py --all`
2. Show updated positions with current prices and P&L
3. Show updated watchlist with current prices
4. Show portfolio summary

**If specific ticker (e.g., CBA):**
1. Use yfinance to fetch current price for the ticker
2. Show: current price, day change, 52-week range
3. If ticker is in positions, show current P&L

**Display format:**
```
TICKER  PRICE     CHANGE    P&L
CBA     $108.75   +1.25%    +$305.00 (+2.89%)
BHP     $45.50    -0.50%    +$125.00 (+1.50%)
```

**Always show timestamp** of when prices were fetched.
