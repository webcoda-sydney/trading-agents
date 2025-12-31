# Execute Paper Trade

Execute a paper trade (buy or sell shares).

## Arguments
- `$ARGUMENTS` - Trade details in format: `[action] [ticker] [quantity] [price] [notes]`

## Examples
```
/trade buy CBA 100 105.50 "Initial banking position"
/trade sell BHP 50 45.75 "Taking profits"
```

## Instructions

Parse the trade command from: $ARGUMENTS

**For BUY orders:**
1. Read `data/portfolio.json` to check cash balance
2. Calculate total cost: (quantity × price) + $19.95 brokerage
3. Validate: sufficient cash, position limits (max 10% of portfolio)
4. If valid:
   - Create trade record in `data/trades.json`
   - Update or create position in `data/positions.json`
   - Deduct cost from cash balance in `data/portfolio.json`
   - Show trade confirmation

**For SELL orders:**
1. Read `data/positions.json` to verify position exists
2. Validate: sufficient shares owned
3. Calculate net proceeds: (quantity × price) - $19.95 brokerage
4. Calculate realised P&L using weighted average cost
5. If valid:
   - Create trade record in `data/trades.json`
   - Update position in `data/positions.json` (reduce or remove)
   - Add proceeds to cash balance in `data/portfolio.json`
   - Update realised P&L
   - Show trade confirmation with P&L

**Trade ID format:** `T[YYYYMMDD]-[sequence]`

**Always show:**
- Trade confirmation with all details
- Updated cash balance
- Updated portfolio value
