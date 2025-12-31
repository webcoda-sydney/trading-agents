# Portfolio Performance Report

Generate a performance report for the specified period.

## Arguments
- `$ARGUMENTS` - Period: today, week, month, quarter, ytd, all

## Examples
```
/performance today    # Today's performance
/performance week     # Last 7 days
/performance month    # Last 30 days
/performance ytd      # Year to date
/performance all      # Since inception
```

## Instructions

For the period in `$ARGUMENTS`:

1. **Load data:**
   - `data/portfolio.json` - Current state
   - `data/positions.json` - Current holdings
   - `data/trades.json` - Trade history
   - `data/performance/returns-history.json` - Historical metrics
   - `data/price-snapshots/` - Historical prices

2. **Calculate metrics:**
   - **Total return**: (Current Value - Initial Capital) / Initial Capital
   - **Period return**: Based on starting value for the period
   - **Realised P&L**: Sum of closed trade profits/losses
   - **Unrealised P&L**: Current positions mark-to-market
   - **Win rate**: Winning trades / Total trades
   - **Best/Worst performers**: By return percentage

3. **Benchmark comparison** (if data available):
   - Compare to ASX200 (^AXJO) for same period

4. **Display report:**

```
PERFORMANCE REPORT - [PERIOD]
========================================
Portfolio Value:    $103,250.00
Initial Capital:    $100,000.00
Total Return:       +$3,250.00 (+3.25%)

Period Return:      +$450.00 (+0.44%)
vs ASX200:          +0.55% (underperformed by 0.11%)

Realised P&L:       $0.00
Unrealised P&L:     +$3,250.00

POSITIONS
---------
CBA     100 shares   +$305.00 (+2.89%)
BHP     50 shares    +$125.00 (+1.50%)
...

TRADE STATISTICS
----------------
Total Trades:       5
Winning Trades:     4 (80%)
Average Win:        +$150.00
Average Loss:       -$75.00
```

5. **Save snapshot** to `data/performance/returns-history.json`
