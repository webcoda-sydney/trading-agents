#!/usr/bin/env python3
"""
Fetch current prices and calculate portfolio value.
Reads portfolio from data/portfolio.json and updates with live prices.

Usage:
    python scripts/fetch_portfolio.py
    python scripts/fetch_portfolio.py --json
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)


def get_project_root() -> Path:
    """Get the project root directory."""
    # Look for CLAUDE.md or .claude folder to identify root
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CLAUDE.md").exists() or (current / ".claude").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def load_portfolio(data_dir: Path) -> dict:
    """Load portfolio data from JSON files."""
    portfolio_file = data_dir / "portfolio.json"
    positions_file = data_dir / "positions.json"

    portfolio = {
        "cash": 100000,
        "currency": "USD",
        "positions": []
    }

    if portfolio_file.exists():
        with open(portfolio_file, "r") as f:
            portfolio.update(json.load(f))

    if positions_file.exists():
        with open(positions_file, "r") as f:
            positions_data = json.load(f)
            if "positions" in positions_data:
                portfolio["positions"] = positions_data["positions"]
            elif isinstance(positions_data, list):
                portfolio["positions"] = positions_data

    return portfolio


def fetch_current_prices(tickers: list) -> dict:
    """Fetch current prices for multiple tickers."""
    prices = {}
    if not tickers:
        return prices

    try:
        # Batch fetch for efficiency
        data = yf.download(tickers, period="1d", progress=False)

        if len(tickers) == 1:
            # Single ticker - different DataFrame structure
            ticker = tickers[0]
            if not data.empty and "Close" in data.columns:
                prices[ticker] = float(data["Close"].iloc[-1])
        else:
            # Multiple tickers
            if not data.empty and "Close" in data.columns:
                for ticker in tickers:
                    if ticker in data["Close"].columns:
                        price = data["Close"][ticker].iloc[-1]
                        if not pd.isna(price):
                            prices[ticker] = float(price)

    except Exception as e:
        print(f"Warning: Batch fetch failed: {e}", file=sys.stderr)
        # Fallback to individual fetches
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                price = info.get("currentPrice") or info.get("regularMarketPrice")
                if price:
                    prices[ticker] = float(price)
            except Exception:
                pass

    return prices


def calculate_portfolio_value(portfolio: dict, prices: dict) -> dict:
    """Calculate total portfolio value and position metrics."""
    cash = portfolio.get("cash", 0)
    positions = portfolio.get("positions", [])
    currency = portfolio.get("currency", "USD")

    position_details = []
    total_cost_basis = 0
    total_market_value = 0
    total_unrealised_pnl = 0

    # Calculate for each position
    for pos in positions:
        ticker = pos.get("ticker", pos.get("symbol"))
        quantity = pos.get("quantity", pos.get("shares", 0))
        avg_cost = pos.get("avg_cost", pos.get("average_cost", pos.get("cost_basis", 0)))

        current_price = prices.get(ticker)

        if current_price is None:
            # Try to fetch individually
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info.get("currentPrice") or info.get("regularMarketPrice")
            except Exception:
                current_price = avg_cost  # Use cost basis as fallback

        cost_basis = quantity * avg_cost
        market_value = quantity * current_price if current_price else cost_basis
        unrealised_pnl = market_value - cost_basis
        unrealised_pnl_pct = (unrealised_pnl / cost_basis * 100) if cost_basis > 0 else 0

        total_cost_basis += cost_basis
        total_market_value += market_value
        total_unrealised_pnl += unrealised_pnl

        position_details.append({
            "ticker": ticker,
            "quantity": quantity,
            "avg_cost": round(avg_cost, 2),
            "current_price": round(current_price, 2) if current_price else None,
            "cost_basis": round(cost_basis, 2),
            "market_value": round(market_value, 2),
            "unrealised_pnl": round(unrealised_pnl, 2),
            "unrealised_pnl_pct": round(unrealised_pnl_pct, 2),
            "weight": 0,  # Will be calculated after total is known
        })

    # Calculate total portfolio value
    total_value = cash + total_market_value

    # Calculate weights
    for pos in position_details:
        pos["weight"] = round(pos["market_value"] / total_value * 100, 2) if total_value > 0 else 0

    # Calculate sector exposure (if available)
    sectors = {}
    for pos in positions:
        sector = pos.get("sector", "Unknown")
        ticker = pos.get("ticker", pos.get("symbol"))
        market_value = next((p["market_value"] for p in position_details if p["ticker"] == ticker), 0)
        sectors[sector] = sectors.get(sector, 0) + market_value

    sector_weights = {
        sector: round(value / total_value * 100, 2)
        for sector, value in sectors.items()
    } if total_value > 0 else {}

    return {
        "timestamp": datetime.now().isoformat(),
        "currency": currency,
        "summary": {
            "total_value": round(total_value, 2),
            "cash": round(cash, 2),
            "cash_pct": round(cash / total_value * 100, 2) if total_value > 0 else 100,
            "invested": round(total_market_value, 2),
            "invested_pct": round(total_market_value / total_value * 100, 2) if total_value > 0 else 0,
            "cost_basis": round(total_cost_basis, 2),
            "unrealised_pnl": round(total_unrealised_pnl, 2),
            "unrealised_pnl_pct": round(total_unrealised_pnl / total_cost_basis * 100, 2) if total_cost_basis > 0 else 0,
            "num_positions": len(position_details),
        },
        "positions": position_details,
        "sector_weights": sector_weights,
    }


def print_summary(data: dict) -> None:
    """Print a human-readable portfolio summary."""
    summary = data["summary"]
    positions = data["positions"]
    currency = data.get("currency", "USD")
    symbols = {"USD": "$", "AUD": "A$", "GBP": "£", "EUR": "€"}
    sym = symbols.get(currency, "$")

    pnl_sign = "+" if summary["unrealised_pnl"] >= 0 else ""

    print(f"""
{'='*70}
PORTFOLIO SUMMARY
{'='*70}

Total Value:      {sym}{summary['total_value']:,.2f}
  Cash:           {sym}{summary['cash']:,.2f} ({summary['cash_pct']:.1f}%)
  Invested:       {sym}{summary['invested']:,.2f} ({summary['invested_pct']:.1f}%)

Cost Basis:       {sym}{summary['cost_basis']:,.2f}
Unrealised P&L:   {pnl_sign}{sym}{summary['unrealised_pnl']:,.2f} ({pnl_sign}{summary['unrealised_pnl_pct']:.2f}%)

Positions: {summary['num_positions']}

HOLDINGS
{'-'*70}
{'Ticker':<8} {'Qty':>8} {'Avg Cost':>10} {'Price':>10} {'Value':>12} {'P&L':>10} {'Weight':>8}
{'-'*70}""")

    for pos in sorted(positions, key=lambda x: x["market_value"], reverse=True):
        pnl_str = f"{'+' if pos['unrealised_pnl'] >= 0 else ''}{pos['unrealised_pnl']:,.0f}"
        print(f"{pos['ticker']:<8} {pos['quantity']:>8} {sym}{pos['avg_cost']:>9.2f} {sym}{pos['current_price'] or 0:>9.2f} {sym}{pos['market_value']:>11,.2f} {pnl_str:>10} {pos['weight']:>7.1f}%")

    print(f"{'-'*70}")

    # Sector breakdown
    if data.get("sector_weights"):
        print(f"\nSECTOR ALLOCATION")
        print(f"{'-'*30}")
        for sector, weight in sorted(data["sector_weights"].items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(weight / 2)
            print(f"{sector:<15} {weight:>5.1f}% {bar}")

    print(f"\n{'='*70}")
    print(f"Updated: {data['timestamp'][:19]}")


if __name__ == "__main__":
    import pandas as pd  # Import here for batch fetch

    json_output = "--json" in sys.argv

    # Find project root and load portfolio
    root = get_project_root()
    data_dir = root / "data"

    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        print("Create data/portfolio.json with your portfolio data.")
        sys.exit(1)

    portfolio = load_portfolio(data_dir)

    # Get tickers from positions
    tickers = [
        pos.get("ticker", pos.get("symbol"))
        for pos in portfolio.get("positions", [])
    ]

    # Fetch prices
    prices = fetch_current_prices(tickers)

    # Calculate portfolio value
    result = calculate_portfolio_value(portfolio, prices)

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print_summary(result)
