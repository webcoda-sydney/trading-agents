# Trading Agents - Claude Instructions

Comprehensive AI trading agents for investment analysis, portfolio management, and trading decisions.

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

## Key Data Files

```
config/trading-rules.json    # Position limits, stop-loss rules
config/screening-presets.json # Stock screening criteria
data/portfolio.json          # Current portfolio state
data/positions.json          # Current holdings
data/watchlist.json          # Stocks being monitored
data/trades.json             # Trade history
```

## Standards

- **Language**: Australian English (colour, realise, centre)
- **Currency**: Local currency for market ($, £, €, ¥)
- **Date Format**: DD/MM/YYYY or local format
- **Timezone**: Local market timezone

## Disclaimer

Paper trading for educational purposes only. Not financial advice.
