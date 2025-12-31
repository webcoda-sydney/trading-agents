# Portfolio Overview

Display current portfolio holdings and summary.

## Arguments
- `$ARGUMENTS` - Optional: `detailed` for expanded view

## Examples
```
/portfolio           # Standard portfolio view
/portfolio detailed  # Detailed view with all metrics
```

## Instructions

1. **Load data:**
   - `data/portfolio.json` - Portfolio state
   - `data/positions.json` - Current holdings
   - `data/trades.json` - Trade count

2. **Display summary:**

```
PORTFOLIO SUMMARY
========================================
Total Value:        $103,250.00
Cash Balance:       $50,000.00 (48.4%)
Invested:           $53,250.00 (51.6%)

Performance
-----------
Initial Capital:    $100,000.00
Total P&L:          +$3,250.00 (+3.25%)
Unrealised:         +$3,250.00
Realised:           $0.00

POSITIONS
=========================================
TICKER  QTY    AVG COST   CURRENT    P&L
CBA     100    $105.50    $108.75    +$325.00 (+3.08%)
BHP     50     $44.00     $45.50     +$75.00 (+1.70%)
NAB     75     $32.00     $33.25     +$93.75 (+3.91%)
...

Total Positions: 5
```

3. **If `detailed` argument:**
   - Show sector allocation breakdown
   - Show position weights
   - Show days held for each position
   - Show dividend income (if any)
   - Show distance to stop-loss/target

4. **Highlight alerts:**
   - Positions near stop-loss (within 2%)
   - Positions at target price
   - Overweight positions (>10%)
   - Overweight sectors (>30%)
