# Portfolio Management Skill

This skill teaches Claude how to manage the paper trading portfolio using data files and scripts.

## Portfolio Data Structure

### Portfolio State (`data/portfolio.json`)

```json
{
  "name": "My Trading Portfolio",
  "currency": "USD",
  "created": "2025-01-01T00:00:00Z",
  "cash": 100000.00,
  "initial_capital": 100000.00
}
```

### Positions (`data/positions.json`)

```json
{
  "positions": [
    {
      "ticker": "AAPL",
      "quantity": 50,
      "avg_cost": 175.50,
      "sector": "Technology",
      "entry_date": "2025-01-15",
      "stop_loss": 161.46,
      "notes": "Strong fundamentals, AI growth catalyst"
    }
  ]
}
```

### Trade History (`data/trades.json`)

```json
{
  "trades": [
    {
      "id": "TRD-001",
      "date": "2025-01-15T10:30:00Z",
      "ticker": "AAPL",
      "action": "BUY",
      "quantity": 50,
      "price": 175.50,
      "total": 8775.00,
      "fees": 0,
      "reason": "Technical breakout + strong earnings"
    }
  ]
}
```

### Watchlist (`data/watchlist.json`)

```json
{
  "watchlist": [
    {
      "ticker": "NVDA",
      "added": "2025-01-10",
      "target_price": 450.00,
      "notes": "Wait for pullback",
      "alerts": ["price_below_500"]
    }
  ]
}
```

## Trading Rules

Loaded from `config/trading-rules.json`:

| Rule | Default | Description |
|------|---------|-------------|
| Max Position | 10% | Maximum single position size |
| Max Sector | 30% | Maximum sector exposure |
| Min Cash | 10% | Minimum cash reserve |
| Default Stop-Loss | 8% | Stop-loss below entry |
| Max Positions | 20 | Maximum number of holdings |

## Portfolio Operations

### Check Portfolio Value

```bash
python scripts/fetch_portfolio.py
```

### Calculate Position Size

Before any trade, calculate appropriate size:

```python
# Example calculation
portfolio_value = 100000
max_position_pct = 0.10  # 10%
stock_price = 175.50

max_position_value = portfolio_value * max_position_pct  # $10,000
max_shares = int(max_position_value / stock_price)  # 56 shares
```

### Execute Paper Trade

1. **Validate** against trading rules
2. **Update** `data/positions.json`
3. **Update** `data/portfolio.json` (cash)
4. **Log** to `data/trades.json`
5. **Set** stop-loss

### Risk Checks Before Trade

Always verify:

1. **Position size** <= 10% of portfolio
2. **Sector exposure** after trade <= 30%
3. **Cash remaining** after trade >= 10%
4. **Stop-loss** is defined

## Portfolio Metrics

### Key Performance Indicators

- **Total Return**: (Current Value - Initial Capital) / Initial Capital
- **Unrealised P&L**: Sum of position gains/losses
- **Realised P&L**: Profit/loss from closed trades
- **Win Rate**: Winning trades / Total trades
- **Average Win/Loss**: Average profit vs average loss
- **Sharpe Ratio**: Risk-adjusted return

### Sector Allocation

Track exposure by sector:
- Technology: Max 30%
- Financials: Max 30%
- Healthcare: Max 30%
- etc.

## Journal Integration

After each trade, prompt for journal entry:

1. **Rationale**: Why this trade?
2. **Thesis**: What needs to happen for success?
3. **Risk**: What could go wrong?
4. **Exit criteria**: When to sell?

Stored in `data/journal/entries/[DATE]-[TICKER].json`

## File Operations

### Creating New Files

When creating portfolio data files, use this structure:

```bash
data/
├── portfolio.json      # Portfolio state
├── positions.json      # Current holdings
├── trades.json         # Trade history
├── watchlist.json      # Stocks being monitored
├── opinions/           # Saved AI opinions
│   └── AAPL-2025-01-15.json
├── research/           # Research reports
│   └── AAPL.json
└── journal/
    └── entries/        # Trade journals
        └── 2025-01-15-AAPL-BUY.json
```

### Updating Portfolio After Trade

1. Read current `portfolio.json` and `positions.json`
2. Calculate new values
3. Write updated files
4. Append to `trades.json`

## Commands Integration

These slash commands interact with portfolio data:

- `/portfolio` - View current portfolio
- `/trade` - Execute paper trade
- `/watchlist` - Manage watchlist
- `/journal` - Add trade journal entry
- `/performance` - View performance metrics
- `/allocate` - Calculate position sizing
