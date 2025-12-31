# Trading Agents

A comprehensive collection of AI trading agents for investment analysis, portfolio management, and trading decisions. Built for Claude Code.

## Overview

This is a generic trading agents toolkit that can be used for any market (stocks, crypto, forex). It includes 24 specialised AI agents organised into functional teams that work together to analyse markets, manage risk, and make investment decisions.

Designed for paper trading and educational purposes.

## Agent Teams

### Analysis Team (5 agents)
| Agent | Purpose |
|-------|---------|
| **fundamental-analyst** | Company financials, valuations, moat analysis, DCF models |
| **technical-analyst** | Chart patterns, indicators (RSI, MACD, Bollinger), support/resistance |
| **sentiment-analyst** | Social media, options flow, positioning data, contrarian signals |
| **news-analyst** | News monitoring, event classification, market impact assessment |
| **macro-strategist** | Central bank policy, economic indicators, sector rotation |

### Research Team (3 agents)
| Agent | Purpose |
|-------|---------|
| **bullish-researcher** | Builds bull cases, identifies upside catalysts, growth drivers |
| **bearish-researcher** | Identifies risks, red flags, bear cases, downside scenarios |
| **equity-researcher** | Synthesises all analysis into comprehensive research reports |

### Execution Team (3 agents)
| Agent | Purpose |
|-------|---------|
| **risk-manager** | Position sizing, policy enforcement, stop-loss management (MUST APPROVE all trades) |
| **portfolio-manager** | CIO role - synthesises inputs, makes final decisions, portfolio construction |
| **trade-executor** | Order execution, execution quality, trade implementation |

### Strategy Specialists (5 agents)
| Agent | Purpose |
|-------|---------|
| **value-investor** | Deep value, margin of safety, intrinsic value, Buffett/Graham style |
| **growth-investor** | High growth stocks, TAM analysis, GARP, Rule of 40 |
| **momentum-trader** | Price momentum, relative strength, trend following |
| **dividend-hunter** | Income investing, dividend safety, yield analysis, franking |
| **options-strategist** | Options strategies, volatility trading, hedging, Greeks |

### Market Specialists (2 agents)
| Agent | Purpose |
|-------|---------|
| **crypto-analyst** | Cryptocurrency analysis, on-chain metrics, tokenomics, DeFi |
| **forex-analyst** | Currency pairs, interest rate differentials, central bank analysis |

### Regional Specialists (2 agents)
| Agent | Purpose |
|-------|---------|
| **asx-specialist** | Australian Stock Exchange expertise, franking, commodities, China exposure |
| **us-market-specialist** | US markets, Fed policy, earnings, options liquidity |

### Coaching & Review (2 agents)
| Agent | Purpose |
|-------|---------|
| **trading-coach** | Trading psychology, behavioural biases, discipline, journaling |
| **trade-reviewer** | Post-trade analysis, performance attribution, skill vs luck |

### Discovery & Briefing (2 agents)
| Agent | Purpose |
|-------|---------|
| **market-analyst** | Daily briefings, overnight markets, sector views, macro context |
| **stock-picker** | Stock screening, opportunity discovery, idea generation |

## Agent Workflow

```
         ┌─────────────────────────────────────────────────────────────┐
         │                    DISCOVERY & BRIEFING                     │
         │         market-analyst  ←→  stock-picker                    │
         └─────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
         ┌─────────────────────────────────────────────────────────────┐
         │                      ANALYSIS TEAM                          │
         │  fundamental  │  technical  │  sentiment  │  news  │ macro │
         └─────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
         ┌─────────────────────────────────────────────────────────────┐
         │                      RESEARCH TEAM                          │
         │    bullish-researcher  ←→  bearish-researcher               │
         │                          ↓                                  │
         │                   equity-researcher                         │
         └─────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
         ┌─────────────────────────────────────────────────────────────┐
         │                     STRATEGY LAYER                          │
         │ value │ growth │ momentum │ dividend │ options │ specialist │
         └─────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
         ┌─────────────────────────────────────────────────────────────┐
         │                     EXECUTION TEAM                          │
         │       portfolio-manager → risk-manager → trade-executor     │
         └─────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
         ┌─────────────────────────────────────────────────────────────┐
         │                    COACHING & REVIEW                        │
         │           trading-coach  ←→  trade-reviewer                 │
         └─────────────────────────────────────────────────────────────┘
```

## Commands (Optional)

If using the ASX-specific paper trading system, these commands are available:

| Command | Description |
|---------|-------------|
| `/briefing` | Daily market briefing |
| `/discover` | Find new opportunities |
| `/opinion` | Get analysis on a stock |
| `/trade` | Execute a paper trade |
| `/portfolio` | View portfolio status |
| `/watchlist` | Manage watchlist |
| `/news` | Get news for holdings |
| `/sector` | Sector analysis |
| `/journal` | Trade journaling |
| `/performance` | Portfolio performance |
| `/research` | Deep research |
| `/scan` | Run screening presets |
| `/allocate` | Position sizing |
| `/price` | Get current price |
| `/ask` | Ask trading coach |

## Quick Start

### Option 1: Clone and Use Directly

```bash
git clone https://github.com/webcoda-sydney/trading-agents.git
cd trading-agents

# Install data fetching dependencies (optional but recommended)
pip install -r scripts/requirements.txt

# Start Claude Code
claude
```

Then try:
```
/briefing
/discover
/opinion AAPL
```

### Option 2: Add to Existing Project

```bash
# Add as submodule
git submodule add https://github.com/webcoda-sydney/trading-agents.git .trading-agents

# Copy agents
cp -r .trading-agents/.claude/agents/* .claude/agents/
```

### Option 3: Copy Specific Agents

Only need certain agents? Copy just what you need:

```bash
# Example: Copy only the analysis team
cp .trading-agents/.claude/agents/fundamental-analyst.md .claude/agents/
cp .trading-agents/.claude/agents/technical-analyst.md .claude/agents/
cp .trading-agents/.claude/agents/sentiment-analyst.md .claude/agents/
```

## Default Trading Rules

| Rule | Value |
|------|-------|
| Max Position Size | 10% of portfolio |
| Max Sector Exposure | 30% of portfolio |
| Min Cash Reserve | 10% of portfolio |
| Default Stop-Loss | 8% below entry |

Configure in `config/trading-rules.json`.

## Real-Time Data

The toolkit includes Python scripts for fetching live market data. **No API keys required** for basic use.

```bash
# Fetch current price
python scripts/fetch_price.py AAPL

# Fetch fundamentals (income statement, ratios, etc.)
python scripts/fetch_fundamentals.py AAPL

# Fetch technical indicators (RSI, MACD, Bollinger, support/resistance)
python scripts/fetch_technicals.py AAPL

# Fetch news with sentiment analysis
python scripts/fetch_news.py AAPL

# Fetch portfolio valuation
python scripts/fetch_portfolio.py
```

### Optional: Enhanced Data Providers

For real-time streaming and advanced sentiment, configure API keys:

| Provider | Free Tier | Signup |
|----------|-----------|--------|
| Alpha Vantage | 500 calls/day | [alphavantage.co](https://www.alphavantage.co/support/#api-key) |
| Finnhub | 60 calls/min | [finnhub.io](https://finnhub.io/register) |
| Twelve Data | 800 calls/day | [twelvedata.com](https://twelvedata.com/register) |

Copy `config/api-keys.example.json` to `config/api-keys.json` and add your keys.

## Structure

```
trading-agents/
├── .claude/
│   ├── agents/          # 24 trading agents
│   ├── commands/        # 15 slash commands
│   └── skills/          # Data fetching skills
├── scripts/             # Python data fetching scripts
│   ├── fetch_price.py
│   ├── fetch_fundamentals.py
│   ├── fetch_technicals.py
│   ├── fetch_news.py
│   ├── fetch_portfolio.py
│   └── requirements.txt
├── config/
│   ├── trading-rules.json      # Position limits, stop-loss rules
│   ├── screening-presets.json  # Stock screening criteria
│   ├── api-keys.example.json   # API key template
│   ├── alerts.json             # Alert configuration
│   └── ai-settings.json        # Agent settings
├── data/                # Portfolio data
│   ├── portfolio.json   # Portfolio state
│   ├── positions.json   # Current holdings
│   ├── trades.json      # Trade history
│   └── watchlist.json   # Monitored stocks
├── .mcp.json            # MCP server configuration
├── CLAUDE.md
└── README.md
```

## Customisation

### Adding Regional Specialists
Copy `asx-specialist.md` or `us-market-specialist.md` and customise for your market:
- Update sector weights
- Add local market drivers
- Include relevant indices
- Adjust for local conventions (currency, date format)

### Adjusting Risk Rules
Edit `config/trading-rules.json` to match your risk tolerance:
- Position size limits
- Sector concentration
- Stop-loss levels
- Cash reserve requirements

## Disclaimer

This is for **paper trading and educational purposes only**. Not financial advice. Past performance does not guarantee future results. Always do your own research before making investment decisions.

## Licence

MIT
