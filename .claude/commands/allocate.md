# Position Size Calculator

Calculate optimal position size for a new trade.

## Arguments
- `$ARGUMENTS` - Ticker and target allocation: `CBA 5%` or `CBA 5000`

## Examples
```
/allocate CBA 5%        # Allocate 5% of portfolio to CBA
/allocate BHP 5000      # Allocate $5,000 to BHP
/allocate CBA           # Use default 5% allocation
```

## Instructions

Parse `$ARGUMENTS` for ticker and allocation:

1. **Load data:**
   - `data/portfolio.json` - Current portfolio value and cash
   - `data/positions.json` - Existing positions
   - `config/trading-rules.json` - Position limits

2. **Fetch current price** for the ticker using yfinance

3. **Calculate position size:**

   **If percentage allocation (e.g., 5%):**
   ```
   Target Value = Portfolio Value × Allocation %
   ```

   **If dollar amount (e.g., 5000):**
   ```
   Target Value = $5,000
   ```

   **If no allocation specified:**
   ```
   Target Value = Portfolio Value × 5% (default)
   ```

4. **Apply limits:**
   - Max 10% of portfolio (from trading-rules.json)
   - Max available cash
   - Min $500 trade size

5. **Calculate shares:**
   ```
   Shares = floor(Target Value / Current Price)
   Total Cost = (Shares × Price) + $19.95 brokerage
   Actual Allocation = Total Cost / Portfolio Value
   ```

6. **Display calculation:**

```
POSITION SIZE CALCULATOR - CBA
========================================
Current Price:      $108.75
Portfolio Value:    $103,250.00
Cash Available:     $50,000.00

Target Allocation:  5.00%
Target Value:       $5,162.50
Max Allowed:        $10,325.00 (10% limit)

RECOMMENDATION
--------------
Shares to Buy:      47
Share Cost:         $5,111.25
Brokerage:          $19.95
Total Cost:         $5,131.20
Actual Allocation:  4.97%

Remaining Cash:     $44,868.80

Execute with: /trade buy CBA 47 108.75 "your notes here"
```

7. **Warnings:**
   - If existing position, show combined allocation
   - If exceeds sector limit, warn user
   - If insufficient cash, show max affordable
