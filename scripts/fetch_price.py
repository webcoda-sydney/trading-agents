#!/usr/bin/env python3
"""
Fetch current price and basic stock data.
Uses yfinance (free, no API key required).

Usage:
    python scripts/fetch_price.py AAPL
    python scripts/fetch_price.py AAPL MSFT GOOGL
    python scripts/fetch_price.py BTC-USD ETH-USD
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Optional

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)


def fetch_price(ticker: str) -> dict:
    """Fetch current price and key metrics for a ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Handle case where ticker doesn't exist
        if not info or info.get("regularMarketPrice") is None:
            return {
                "ticker": ticker,
                "error": f"No data found for {ticker}",
                "success": False
            }

        # Get historical data for performance calculations
        hist = stock.history(period="1y")

        # Calculate performance metrics
        perf_1w = perf_1m = perf_3m = perf_ytd = perf_1y = None

        if len(hist) > 0:
            current = hist['Close'].iloc[-1]

            if len(hist) >= 5:
                perf_1w = ((current / hist['Close'].iloc[-5]) - 1) * 100
            if len(hist) >= 21:
                perf_1m = ((current / hist['Close'].iloc[-21]) - 1) * 100
            if len(hist) >= 63:
                perf_3m = ((current / hist['Close'].iloc[-63]) - 1) * 100
            if len(hist) >= 252:
                perf_1y = ((current / hist['Close'].iloc[0]) - 1) * 100

            # YTD calculation
            year_start = datetime(datetime.now().year, 1, 1)
            ytd_data = hist[hist.index >= year_start.strftime('%Y-%m-%d')]
            if len(ytd_data) > 0:
                perf_ytd = ((current / ytd_data['Close'].iloc[0]) - 1) * 100

        # Get current price (try multiple fields)
        current_price = (
            info.get("currentPrice") or
            info.get("regularMarketPrice") or
            info.get("previousClose")
        )

        # Calculate 52-week percentile
        high_52w = info.get("fiftyTwoWeekHigh")
        low_52w = info.get("fiftyTwoWeekLow")
        percentile_52w = None
        if high_52w and low_52w and current_price:
            if high_52w != low_52w:
                percentile_52w = ((current_price - low_52w) / (high_52w - low_52w)) * 100

        return {
            "ticker": ticker.upper(),
            "name": info.get("shortName") or info.get("longName"),
            "success": True,
            "timestamp": datetime.now().isoformat(),

            # Price data
            "price": {
                "current": current_price,
                "previous_close": info.get("previousClose"),
                "open": info.get("regularMarketOpen") or info.get("open"),
                "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
                "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
                "change": info.get("regularMarketChange"),
                "change_pct": info.get("regularMarketChangePercent"),
            },

            # 52-week range
            "range_52w": {
                "high": high_52w,
                "low": low_52w,
                "percentile": round(percentile_52w, 1) if percentile_52w else None,
            },

            # Key metrics
            "metrics": {
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "peg_ratio": info.get("pegRatio"),
                "price_to_book": info.get("priceToBook"),
                "dividend_yield": info.get("dividendYield"),
                "dividend_rate": info.get("dividendRate"),
                "beta": info.get("beta"),
                "eps": info.get("trailingEps"),
            },

            # Performance
            "performance": {
                "1_week": round(perf_1w, 2) if perf_1w else None,
                "1_month": round(perf_1m, 2) if perf_1m else None,
                "3_month": round(perf_3m, 2) if perf_3m else None,
                "ytd": round(perf_ytd, 2) if perf_ytd else None,
                "1_year": round(perf_1y, 2) if perf_1y else None,
            },

            # Volume
            "volume": {
                "current": info.get("volume") or info.get("regularMarketVolume"),
                "average": info.get("averageVolume"),
                "average_10d": info.get("averageDailyVolume10Day"),
            },

            # Company info
            "company": {
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "exchange": info.get("exchange"),
                "currency": info.get("currency"),
            }
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e),
            "success": False
        }


def format_large_number(num: Optional[float]) -> str:
    """Format large numbers for display (e.g., 1.5T, 250B, 50M)."""
    if num is None:
        return "N/A"
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    if num >= 1e6:
        return f"${num/1e6:.2f}M"
    return f"${num:,.0f}"


def print_summary(data: dict) -> None:
    """Print a human-readable summary."""
    if not data.get("success"):
        print(f"Error: {data.get('error')}")
        return

    p = data["price"]
    m = data["metrics"]
    r = data["range_52w"]
    perf = data["performance"]
    c = data["company"]

    change_str = ""
    if p.get("change") and p.get("change_pct"):
        sign = "+" if p["change"] >= 0 else ""
        change_str = f" ({sign}{p['change']:.2f}, {sign}{p['change_pct']:.2f}%)"

    print(f"""
{'='*60}
{data['ticker']} - {data.get('name', 'Unknown')}
{'='*60}

PRICE
  Current:       ${p['current']:.2f}{change_str}
  Day Range:     ${p.get('day_low', 0):.2f} - ${p.get('day_high', 0):.2f}
  52-Week Range: ${r.get('low', 0):.2f} - ${r.get('high', 0):.2f} ({r.get('percentile', 'N/A')}th percentile)

METRICS
  Market Cap:    {format_large_number(m.get('market_cap'))}
  P/E Ratio:     {m.get('pe_ratio', 'N/A'):.2f if m.get('pe_ratio') else 'N/A'}
  Forward P/E:   {m.get('forward_pe', 'N/A'):.2f if m.get('forward_pe') else 'N/A'}
  EPS:           ${m.get('eps', 0):.2f if m.get('eps') else 'N/A'}
  Dividend:      {m.get('dividend_yield', 0)*100:.2f}% if m.get('dividend_yield') else 'N/A'
  Beta:          {m.get('beta', 'N/A'):.2f if m.get('beta') else 'N/A'}

PERFORMANCE
  1 Week:        {perf.get('1_week', 'N/A'):+.2f}% if perf.get('1_week') else 'N/A'
  1 Month:       {perf.get('1_month', 'N/A'):+.2f}% if perf.get('1_month') else 'N/A'
  3 Month:       {perf.get('3_month', 'N/A'):+.2f}% if perf.get('3_month') else 'N/A'
  YTD:           {perf.get('ytd', 'N/A'):+.2f}% if perf.get('ytd') else 'N/A'
  1 Year:        {perf.get('1_year', 'N/A'):+.2f}% if perf.get('1_year') else 'N/A'

INFO
  Sector:        {c.get('sector', 'N/A')}
  Industry:      {c.get('industry', 'N/A')}
  Exchange:      {c.get('exchange', 'N/A')}
{'='*60}
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_price.py TICKER [TICKER2 ...]")
        print("Example: python fetch_price.py AAPL MSFT GOOGL")
        sys.exit(1)

    tickers = sys.argv[1:]

    # Check for --json flag
    json_output = "--json" in tickers
    if json_output:
        tickers.remove("--json")

    results = []
    for ticker in tickers:
        data = fetch_price(ticker)
        results.append(data)

        if not json_output:
            print_summary(data)

    if json_output:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
