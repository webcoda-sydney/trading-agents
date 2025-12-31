# API Providers Skill

This skill documents available financial data API providers and how to configure them.

## Provider Comparison

### Free Tier Providers

| Provider | Free Limits | Best For | API Key Required |
|----------|-------------|----------|------------------|
| **yfinance** | Unlimited* | Basic data, no setup | No |
| **Alpha Vantage** | 500 calls/day | Technical indicators | Yes (free) |
| **Finnhub** | 60 calls/min | Real-time + sentiment | Yes (free) |
| **Twelve Data** | 800 calls/day | Global coverage | Yes (free) |
| **FMP** | 500MB/month | Fundamentals | Yes (free) |

*yfinance uses Yahoo Finance's public API - rate limits may apply.

### Paid Providers

| Provider | Starting Price | Best For |
|----------|----------------|----------|
| **Polygon.io** | $199/mo | Real-time streaming, US equities |
| **Twelve Data** | $29/mo | Global markets, WebSocket |
| **Intrinio** | $250/mo | Institutional-grade data |
| **Tradier** | Free with account | Live/paper trading execution |

## Configuration

### Environment Variables

Set API keys as environment variables:

```bash
# Windows (PowerShell)
$env:ALPHA_VANTAGE_API_KEY = "your_key_here"
$env:FINNHUB_API_KEY = "your_key_here"
$env:TWELVE_DATA_API_KEY = "your_key_here"

# Windows (CMD)
set ALPHA_VANTAGE_API_KEY=your_key_here

# Linux/macOS
export ALPHA_VANTAGE_API_KEY="your_key_here"
```

### Configuration File

Alternatively, create `config/api-keys.json` (gitignored):

```json
{
  "alpha_vantage": {
    "api_key": "YOUR_KEY",
    "tier": "free",
    "calls_per_day": 500
  },
  "finnhub": {
    "api_key": "YOUR_KEY",
    "tier": "free",
    "calls_per_minute": 60
  },
  "twelve_data": {
    "api_key": "YOUR_KEY",
    "tier": "free",
    "calls_per_day": 800
  }
}
```

## Getting API Keys

### Alpha Vantage (Free)
1. Visit https://www.alphavantage.co/support/#api-key
2. Enter email and get instant API key
3. Free tier: 500 API calls per day

### Finnhub (Free)
1. Visit https://finnhub.io/register
2. Create account and verify email
3. API key in dashboard
4. Free tier: 60 API calls per minute

### Twelve Data (Free)
1. Visit https://twelvedata.com/register
2. Create account
3. API key in dashboard
4. Free tier: 800 API credits per day

### Polygon.io
1. Visit https://polygon.io/
2. Sign up for account
3. Free tier: 5 calls/minute (very limited)
4. Paid plans from $199/month

### Tradier (Free with Brokerage Account)
1. Visit https://tradier.com
2. Open brokerage account
3. API access included free
4. Paper trading available

## Fallback Strategy

The scripts use this fallback order:

1. **yfinance** (always available, no key)
2. **Configured API** (if key set)
3. **Web search** (last resort, via Claude)

## Rate Limiting

To avoid hitting rate limits:

1. **Cache responses** - Don't fetch same ticker repeatedly
2. **Batch requests** - Use multi-ticker fetches when possible
3. **Time delays** - Add sleep between API calls if needed
4. **Check quotas** - Monitor usage against daily/minute limits

## Data Quality Notes

| Provider | Real-Time | Historical Depth | Fundamentals | Sentiment |
|----------|-----------|------------------|--------------|-----------|
| yfinance | ~15min delay | 30+ years | Good | None |
| Alpha Vantage | Near real-time | 20+ years | Limited | News only |
| Finnhub | Real-time | 10+ years | Good | Excellent |
| Twelve Data | Real-time | 30+ years | Good | Limited |

## MCP Server Integration

For deeper integration, configure MCP servers in `.mcp.json`:

```json
{
  "mcpServers": {
    "finnhub": {
      "command": "npx",
      "args": ["-y", "mcp-finnhub"],
      "env": {
        "FINNHUB_API_KEY": "${FINNHUB_API_KEY}"
      }
    }
  }
}
```

This enables Claude to access Finnhub data directly as an MCP tool.
