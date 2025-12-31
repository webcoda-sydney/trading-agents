#!/usr/bin/env python3
"""
Fetch recent news for a stock.
Uses yfinance news feed (free, no API key required).

For enhanced news with sentiment, configure Finnhub or Alpha Vantage API keys.

Usage:
    python scripts/fetch_news.py AAPL
    python scripts/fetch_news.py AAPL --json
    python scripts/fetch_news.py AAPL --limit 5
"""

import sys
import json
from datetime import datetime, timezone
from typing import Optional, List
import os

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)

# Try to import requests for API providers
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def fetch_yfinance_news(ticker: str, limit: int = 10) -> List[dict]:
    """Fetch news from Yahoo Finance (free, no API key)."""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news

        if not news:
            return []

        results = []
        for item in news[:limit]:
            # Parse timestamp
            pub_time = None
            if "providerPublishTime" in item:
                pub_time = datetime.fromtimestamp(
                    item["providerPublishTime"],
                    tz=timezone.utc
                ).isoformat()

            results.append({
                "title": item.get("title"),
                "publisher": item.get("publisher"),
                "link": item.get("link"),
                "published": pub_time,
                "type": item.get("type"),
                "thumbnail": item.get("thumbnail", {}).get("resolutions", [{}])[0].get("url") if item.get("thumbnail") else None,
                "source": "yfinance",
            })

        return results

    except Exception as e:
        print(f"Warning: yfinance news error: {e}", file=sys.stderr)
        return []


def fetch_finnhub_news(ticker: str, limit: int = 10) -> List[dict]:
    """Fetch news from Finnhub (requires API key)."""
    api_key = os.environ.get("FINNHUB_API_KEY")
    if not api_key or not HAS_REQUESTS:
        return []

    try:
        # Get news from last 7 days
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        url = f"https://finnhub.io/api/v1/company-news"
        params = {
            "symbol": ticker,
            "from": from_date,
            "to": to_date,
            "token": api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        news = response.json()

        results = []
        for item in news[:limit]:
            pub_time = None
            if "datetime" in item:
                pub_time = datetime.fromtimestamp(
                    item["datetime"],
                    tz=timezone.utc
                ).isoformat()

            results.append({
                "title": item.get("headline"),
                "summary": item.get("summary"),
                "publisher": item.get("source"),
                "link": item.get("url"),
                "published": pub_time,
                "category": item.get("category"),
                "sentiment": item.get("sentiment"),  # Finnhub provides sentiment
                "source": "finnhub",
            })

        return results

    except Exception as e:
        print(f"Warning: Finnhub news error: {e}", file=sys.stderr)
        return []


def fetch_alphavantage_news(ticker: str, limit: int = 10) -> List[dict]:
    """Fetch news from Alpha Vantage (requires API key)."""
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key or not HAS_REQUESTS:
        return []

    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "limit": limit,
            "apikey": api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "feed" not in data:
            return []

        results = []
        for item in data["feed"][:limit]:
            # Find sentiment for this specific ticker
            ticker_sentiment = None
            for ts in item.get("ticker_sentiment", []):
                if ts.get("ticker") == ticker:
                    ticker_sentiment = {
                        "score": float(ts.get("ticker_sentiment_score", 0)),
                        "label": ts.get("ticker_sentiment_label"),
                        "relevance": float(ts.get("relevance_score", 0)),
                    }
                    break

            results.append({
                "title": item.get("title"),
                "summary": item.get("summary"),
                "publisher": item.get("source"),
                "link": item.get("url"),
                "published": item.get("time_published"),
                "overall_sentiment_score": float(item.get("overall_sentiment_score", 0)),
                "overall_sentiment_label": item.get("overall_sentiment_label"),
                "ticker_sentiment": ticker_sentiment,
                "topics": [t.get("topic") for t in item.get("topics", [])],
                "source": "alphavantage",
            })

        return results

    except Exception as e:
        print(f"Warning: Alpha Vantage news error: {e}", file=sys.stderr)
        return []


def classify_news_impact(title: str, summary: str = "") -> dict:
    """Simple rule-based news classification."""
    text = (title + " " + (summary or "")).lower()

    # Impact keywords
    positive_keywords = [
        "upgrade", "beat", "surge", "soar", "rally", "breakthrough",
        "record", "growth", "profit", "dividend", "buyback", "acquisition",
        "partnership", "approval", "wins", "launches", "expands"
    ]
    negative_keywords = [
        "downgrade", "miss", "plunge", "crash", "decline", "loss",
        "lawsuit", "investigation", "recall", "layoff", "cuts", "warning",
        "bankruptcy", "fraud", "scandal", "fine", "penalty"
    ]
    major_keywords = [
        "ceo", "merger", "acquisition", "ipo", "earnings", "fda",
        "sec", "antitrust", "bankruptcy", "takeover"
    ]

    # Count matches
    positive_count = sum(1 for kw in positive_keywords if kw in text)
    negative_count = sum(1 for kw in negative_keywords if kw in text)
    is_major = any(kw in text for kw in major_keywords)

    # Determine impact
    if positive_count > negative_count:
        sentiment = "POSITIVE"
    elif negative_count > positive_count:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    impact = "HIGH" if is_major else ("MEDIUM" if positive_count + negative_count > 0 else "LOW")

    return {
        "sentiment": sentiment,
        "impact": impact,
        "positive_signals": positive_count,
        "negative_signals": negative_count,
    }


def fetch_news(ticker: str, limit: int = 10) -> dict:
    """Fetch news from all available sources."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Check if valid ticker
        if not info or not info.get("shortName"):
            return {
                "ticker": ticker,
                "error": f"No data found for {ticker}",
                "success": False
            }

        # Fetch from all sources
        all_news = []

        # Primary: yfinance (always available)
        yf_news = fetch_yfinance_news(ticker, limit)
        all_news.extend(yf_news)

        # Optional: Finnhub (if API key configured)
        fh_news = fetch_finnhub_news(ticker, limit)
        all_news.extend(fh_news)

        # Optional: Alpha Vantage (if API key configured)
        av_news = fetch_alphavantage_news(ticker, limit)
        all_news.extend(av_news)

        # Deduplicate by title (prefer sources with sentiment)
        seen_titles = set()
        unique_news = []
        for item in all_news:
            title = item.get("title", "").lower()[:50]  # First 50 chars
            if title and title not in seen_titles:
                seen_titles.add(title)

                # Add classification if not present
                if "sentiment" not in item:
                    classification = classify_news_impact(
                        item.get("title", ""),
                        item.get("summary", "")
                    )
                    item["classification"] = classification

                unique_news.append(item)

        # Sort by date (newest first)
        unique_news.sort(
            key=lambda x: x.get("published") or "",
            reverse=True
        )

        # Aggregate sentiment
        sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
        for item in unique_news:
            if "classification" in item:
                sentiment_counts[item["classification"]["sentiment"]] += 1
            elif item.get("overall_sentiment_label"):
                label = item["overall_sentiment_label"]
                if "Bullish" in label:
                    sentiment_counts["POSITIVE"] += 1
                elif "Bearish" in label:
                    sentiment_counts["NEGATIVE"] += 1
                else:
                    sentiment_counts["NEUTRAL"] += 1

        # Overall sentiment
        total = sum(sentiment_counts.values())
        if total > 0:
            if sentiment_counts["POSITIVE"] > sentiment_counts["NEGATIVE"] * 1.5:
                overall_sentiment = "BULLISH"
            elif sentiment_counts["NEGATIVE"] > sentiment_counts["POSITIVE"] * 1.5:
                overall_sentiment = "BEARISH"
            else:
                overall_sentiment = "MIXED"
        else:
            overall_sentiment = "NO_NEWS"

        return {
            "ticker": ticker.upper(),
            "name": info.get("shortName") or info.get("longName"),
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "news_count": len(unique_news),
            "sources_used": list(set(n.get("source") for n in unique_news)),
            "sentiment_summary": {
                "overall": overall_sentiment,
                "positive_count": sentiment_counts["POSITIVE"],
                "negative_count": sentiment_counts["NEGATIVE"],
                "neutral_count": sentiment_counts["NEUTRAL"],
            },
            "news": unique_news[:limit],
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e),
            "success": False
        }


def print_summary(data: dict) -> None:
    """Print a human-readable summary."""
    if not data.get("success"):
        print(f"Error: {data.get('error')}")
        return

    sent = data["sentiment_summary"]

    print(f"""
{'='*70}
NEWS ANALYSIS: {data['ticker']} - {data.get('name', 'Unknown')}
{'='*70}

SENTIMENT SUMMARY: {sent['overall']}
  Positive: {sent['positive_count']} | Negative: {sent['negative_count']} | Neutral: {sent['neutral_count']}
  Sources: {', '.join(data.get('sources_used', ['yfinance']))}

RECENT NEWS ({data['news_count']} articles)
{'-'*70}
""")

    for i, item in enumerate(data.get("news", []), 1):
        # Sentiment indicator
        if "classification" in item:
            sentiment = item["classification"]["sentiment"]
            impact = item["classification"]["impact"]
            indicator = {"POSITIVE": "+", "NEGATIVE": "-", "NEUTRAL": "o"}[sentiment]
            impact_str = f"[{impact}]"
        elif item.get("overall_sentiment_label"):
            indicator = "+" if "Bullish" in item["overall_sentiment_label"] else ("-" if "Bearish" in item["overall_sentiment_label"] else "o")
            impact_str = ""
        else:
            indicator = "o"
            impact_str = ""

        # Format date
        pub_date = item.get("published", "")[:10] if item.get("published") else "Unknown"

        print(f"""
[{indicator}] {impact_str} {item.get('title', 'No title')}
    Source: {item.get('publisher', 'Unknown')} | Date: {pub_date}
    Link: {item.get('link', 'N/A')}""")

        if item.get("summary"):
            summary = item["summary"][:200] + "..." if len(item.get("summary", "")) > 200 else item["summary"]
            print(f"    Summary: {summary}")

    print(f"\n{'='*70}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_news.py TICKER [--json] [--limit N]")
        print("Example: python fetch_news.py AAPL --limit 5")
        print("\nOptional API keys (environment variables):")
        print("  FINNHUB_API_KEY - For enhanced news with sentiment")
        print("  ALPHA_VANTAGE_API_KEY - For news with detailed sentiment analysis")
        sys.exit(1)

    ticker = sys.argv[1]
    json_output = "--json" in sys.argv

    # Parse limit
    limit = 10
    if "--limit" in sys.argv:
        try:
            limit_idx = sys.argv.index("--limit")
            limit = int(sys.argv[limit_idx + 1])
        except (IndexError, ValueError):
            pass

    # Import timedelta for Finnhub date range
    from datetime import timedelta

    data = fetch_news(ticker, limit)

    if json_output:
        print(json.dumps(data, indent=2, default=str))
    else:
        print_summary(data)
