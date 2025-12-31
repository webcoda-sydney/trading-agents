# Stock Data Skill

This skill teaches Claude how to fetch real-time stock data using the Python scripts in `/scripts`.

## When to Use This Skill

Use these data fetching scripts when you need:
- Current stock prices and performance metrics
- Fundamental analysis data (financial statements, ratios)
- Technical analysis indicators (RSI, MACD, Bollinger Bands)
- News and sentiment analysis
- Portfolio valuation

## Available Scripts

### 1. Price Data (`fetch_price.py`)

Fetches current price, key metrics, and performance data.

```bash
python scripts/fetch_price.py AAPL
python scripts/fetch_price.py AAPL MSFT GOOGL  # Multiple tickers
python scripts/fetch_price.py AAPL --json      # JSON output
```

**Returns:**
- Current price, day change, 52-week range
- P/E ratio, market cap, dividend yield
- 1-week, 1-month, 3-month, YTD, 1-year performance
- Sector, industry, exchange info

### 2. Fundamentals (`fetch_fundamentals.py`)

Fetches comprehensive fundamental analysis data.

```bash
python scripts/fetch_fundamentals.py AAPL
python scripts/fetch_fundamentals.py AAPL --json
```

**Returns:**
- Income statement: Revenue, gross profit, net income, EPS
- Margins: Gross, operating, net, EBITDA
- Balance sheet: Assets, liabilities, equity, debt, cash
- Cash flow: Operating CF, CapEx, free cash flow
- Ratios: ROE, ROA, ROIC, debt/equity, current ratio
- Valuation: P/E, P/B, EV/EBITDA, PEG

### 3. Technicals (`fetch_technicals.py`)

Fetches technical analysis indicators and signals.

```bash
python scripts/fetch_technicals.py AAPL
python scripts/fetch_technicals.py AAPL --json
```

**Returns:**
- Moving averages: SMA 20/50/200, EMA 12/26
- Oscillators: RSI (14), Stochastic
- MACD: Line, signal, histogram
- Bollinger Bands: Upper, middle, lower, position
- Volatility: ATR (14)
- Volume analysis: Current vs average
- Trend identification: Bullish/bearish/neutral
- Support/resistance levels
- Overall signal: Strong Buy to Strong Sell (0-100 score)

### 4. News (`fetch_news.py`)

Fetches recent news with sentiment analysis.

```bash
python scripts/fetch_news.py AAPL
python scripts/fetch_news.py AAPL --limit 5
python scripts/fetch_news.py AAPL --json
```

**Returns:**
- News articles with titles, summaries, links
- Sentiment classification (positive/negative/neutral)
- Impact rating (high/medium/low)
- Overall sentiment summary

**Optional API keys for enhanced news:**
- `FINNHUB_API_KEY` - Real-time news with sentiment
- `ALPHA_VANTAGE_API_KEY` - Detailed sentiment scores

### 5. Portfolio (`fetch_portfolio.py`)

Fetches live portfolio valuation.

```bash
python scripts/fetch_portfolio.py
python scripts/fetch_portfolio.py --json
```

**Requires:** `data/portfolio.json` and/or `data/positions.json`

**Returns:**
- Total portfolio value
- Cash and invested amounts
- Per-position metrics: price, P&L, weight
- Sector allocation

## Data Sources

| Priority | Source | API Key Required | Coverage |
|----------|--------|------------------|----------|
| 1 | yfinance | No | Global stocks, crypto, forex |
| 2 | Alpha Vantage | Yes (free tier available) | US stocks, 60+ indicators |
| 3 | Finnhub | Yes (free tier available) | Global, real-time, sentiment |
| 4 | Twelve Data | Yes (free tier available) | Global, 100+ indicators |

## Installation

Before first use, install dependencies:

```bash
pip install -r scripts/requirements.txt
```

## Usage Guidelines

1. **Always use `--json` flag** when parsing data programmatically
2. **Cache results** when making multiple calls for the same ticker
3. **Batch requests** when fetching multiple tickers (use space-separated list)
4. **Check for errors** - scripts return `"success": false` on failure

## Example Workflow

For a complete stock analysis:

```bash
# 1. Get current price and performance
python scripts/fetch_price.py AAPL --json > price.json

# 2. Get fundamental analysis
python scripts/fetch_fundamentals.py AAPL --json > fundamentals.json

# 3. Get technical indicators
python scripts/fetch_technicals.py AAPL --json > technicals.json

# 4. Get recent news
python scripts/fetch_news.py AAPL --limit 5 --json > news.json
```

## Crypto and Forex

These scripts also support:

- **Crypto**: Use Yahoo Finance format (e.g., `BTC-USD`, `ETH-USD`)
- **Forex**: Use currency pair format (e.g., `EURUSD=X`, `GBPUSD=X`)
- **ASX stocks**: Use `.AX` suffix (e.g., `CBA.AX`, `BHP.AX`)
- **LSE stocks**: Use `.L` suffix (e.g., `HSBA.L`, `BP.L`)

## Error Handling

If a script fails:
1. Check ticker symbol is valid
2. Verify internet connection
3. Check if yfinance is installed (`pip install yfinance`)
4. For enhanced features, verify API keys are set

Scripts always return a `success` field indicating whether data was retrieved.
