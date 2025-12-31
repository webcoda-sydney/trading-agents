# Trading Agents - Claude Instructions

Comprehensive AI trading agents for investment analysis, portfolio management, and trading decisions.

## ⚠️ CRITICAL: Date Awareness

**ALWAYS use the date from the `<env>` block in your system context.** The `<env>` block contains `Today's date: YYYY-MM-DD` - this is the ACTUAL current date.

**DO NOT rely on your internal sense of time.** Your training data has a knowledge cutoff that may cause you to believe it's an earlier date (e.g., 2024 when it's actually 2025). This leads to incorrect analysis.

When performing any analysis:
- Check the `<env>` block for `Today's date`
- Use this date for all date references, market context, and analysis
- When fetching data, news, or prices - use the current year from `<env>`
- State the current date explicitly in market briefings and analysis

## Agent Teams Summary

### Analysis Team (5 agents)
- **fundamental-analyst**: Financial statements, valuations, moat analysis, DCF - Score 0-100
- **technical-analyst**: RSI, MACD, Bollinger, patterns, support/resistance - Score 0-100
- **sentiment-analyst**: Social sentiment, options flow, positioning - Score -100 to +100
- **news-analyst**: News monitoring, event classification, impact - Score -100 to +100
- **macro-strategist**: Central banks, economic data, sector rotation - Score 0-100

### Research Team (3 agents)
- **bullish-researcher**: Bull case construction, upside catalysts, growth drivers
- **bearish-researcher**: Risk identification, red flags, bear case, downside scenarios
- **equity-researcher**: Synthesises all analysis into comprehensive research reports

### Execution Team (3 agents)
- **risk-manager**: Position sizing, policy gates, stops - MUST APPROVE all trades
- **portfolio-manager**: CIO - synthesises inputs, makes final recommendations
- **trade-executor**: Order execution, execution quality, trade implementation

### Strategy Specialists (5 agents)
- **value-investor**: Deep value, margin of safety, Graham/Buffett approach
- **growth-investor**: High growth, TAM analysis, GARP, Rule of 40
- **momentum-trader**: Price momentum, relative strength, trend following
- **dividend-hunter**: Income investing, dividend safety, yield analysis
- **options-strategist**: Options strategies, Greeks, volatility trading

### Market Specialists (2 agents)
- **crypto-analyst**: Cryptocurrency analysis, on-chain metrics, tokenomics
- **forex-analyst**: Currency pairs, rate differentials, central bank policy

### Regional Specialists (2 agents)
- **asx-specialist**: ASX expertise, franking, commodities, China exposure
- **us-market-specialist**: US markets, Fed policy, earnings, options

### Coaching & Review (2 agents)
- **trading-coach**: Psychology, behavioural biases, discipline, journaling
- **trade-reviewer**: Post-trade analysis, attribution, skill vs luck

### Discovery & Briefing (2 agents)
- **market-analyst**: Daily briefings, overnight markets, sector views
- **stock-picker**: Stock screening, opportunity discovery, idea generation

## Trading Rules (Enforced by risk-manager)

| Rule | Limit |
|------|-------|
| Max Position | 10% of portfolio |
| Max Sector | 30% of portfolio |
| Min Cash | 10% of portfolio |
| Stop-Loss | Required on all positions |

## Workflow

### For Stock Analysis (`/opinion {TICKER}`)
1. `fundamental-analyst` → Fundamentals score
2. `technical-analyst` → Technical score
3. `sentiment-analyst` → Sentiment score
4. `news-analyst` → News impact score
5. `macro-strategist` → Macro context score
6. `bullish-researcher` + `bearish-researcher` → Bull/bear cases
7. `equity-researcher` → Synthesised recommendation
8. `risk-manager` → Risk assessment
9. `portfolio-manager` → Final decision

### For Trade Execution (`/trade`)
1. Run full analysis workflow
2. `risk-manager` MUST approve
3. Check policy gates (position, sector, cash)
4. `trade-executor` implements if approved
5. `trading-coach` + `trade-reviewer` post-trade review

### For Discovery (`/discover`)
1. `market-analyst` → Market context
2. `stock-picker` → Run screens
3. Apply strategy filters (value, growth, momentum, dividend)
4. Prioritise by conviction score

## Real-Time Data Fetching

Use Python scripts to fetch live market data. **No API keys required** for basic functionality (uses yfinance).

### Quick Commands

```bash
# Install dependencies (first time only)
pip install -r scripts/requirements.txt

# Fetch current price and metrics
python scripts/fetch_price.py AAPL

# Fetch fundamental analysis
python scripts/fetch_fundamentals.py AAPL

# Fetch technical indicators (RSI, MACD, Bollinger, etc.)
python scripts/fetch_technicals.py AAPL

# Fetch news with sentiment
python scripts/fetch_news.py AAPL

# Fetch portfolio valuation
python scripts/fetch_portfolio.py
```

### For JSON Output (Programmatic Use)

Add `--json` flag to any script:
```bash
python scripts/fetch_price.py AAPL --json
```

### Enhanced Data (Optional API Keys)

For real-time data and sentiment analysis, configure API keys:
1. Copy `config/api-keys.example.json` to `config/api-keys.json`
2. Add your API keys (free tiers available)
3. Set as environment variables

| Provider | Free Tier | Best For |
|----------|-----------|----------|
| Alpha Vantage | 500/day | Technical indicators |
| Finnhub | 60/min | Real-time + sentiment |
| Twelve Data | 800/day | Global coverage |

## Key Data Files

```
config/trading-rules.json      # Position limits, stop-loss rules
config/screening-presets.json  # Stock screening criteria
config/api-keys.json           # API keys (gitignored)
data/portfolio.json            # Current portfolio state
data/positions.json            # Current holdings
data/watchlist.json            # Stocks being monitored
data/trades.json               # Trade history
scripts/                       # Data fetching scripts
.claude/skills/                # Data fetching skills
```

## Standards

- **Language**: Australian English (colour, realise, centre)
- **Currency**: Local currency for market ($, £, €, ¥)
- **Date Format**: DD/MM/YYYY or local format
- **Timezone**: Local market timezone

## Disclaimer

Paper trading for educational purposes only. Not financial advice.
