#!/usr/bin/env python3
"""
Fetch fundamental data for a stock.
Includes income statement, balance sheet, cash flow, and key ratios.

Usage:
    python scripts/fetch_fundamentals.py AAPL
    python scripts/fetch_fundamentals.py AAPL --json
"""

import sys
import json
from datetime import datetime
from typing import Optional

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install yfinance pandas")
    sys.exit(1)


def safe_get(df: pd.DataFrame, key: str, period: int = 0) -> Optional[float]:
    """Safely get a value from a DataFrame."""
    try:
        if key in df.index:
            val = df.iloc[:, period][key]
            if pd.notna(val):
                return float(val)
    except (KeyError, IndexError):
        pass
    return None


def calculate_growth(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    """Calculate YoY growth rate."""
    if current is None or previous is None or previous == 0:
        return None
    return ((current - previous) / abs(previous)) * 100


def fetch_fundamentals(ticker: str) -> dict:
    """Fetch comprehensive fundamental data for a ticker."""
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

        # Get financial statements
        income_stmt = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow

        # Income Statement metrics
        revenue = safe_get(income_stmt, "Total Revenue")
        revenue_prev = safe_get(income_stmt, "Total Revenue", 1)
        gross_profit = safe_get(income_stmt, "Gross Profit")
        operating_income = safe_get(income_stmt, "Operating Income")
        net_income = safe_get(income_stmt, "Net Income")
        net_income_prev = safe_get(income_stmt, "Net Income", 1)
        ebitda = safe_get(income_stmt, "EBITDA")

        # Balance Sheet metrics
        total_assets = safe_get(balance_sheet, "Total Assets")
        total_liabilities = safe_get(balance_sheet, "Total Liabilities Net Minority Interest")
        total_equity = safe_get(balance_sheet, "Stockholders Equity") or safe_get(balance_sheet, "Total Equity Gross Minority Interest")
        total_debt = safe_get(balance_sheet, "Total Debt")
        cash = safe_get(balance_sheet, "Cash And Cash Equivalents")
        current_assets = safe_get(balance_sheet, "Current Assets")
        current_liabilities = safe_get(balance_sheet, "Current Liabilities")

        # Cash Flow metrics
        operating_cf = safe_get(cash_flow, "Operating Cash Flow")
        capex = safe_get(cash_flow, "Capital Expenditure")
        free_cash_flow = safe_get(cash_flow, "Free Cash Flow")
        if free_cash_flow is None and operating_cf and capex:
            free_cash_flow = operating_cf + capex  # capex is usually negative

        dividends_paid = safe_get(cash_flow, "Common Stock Dividend Paid")
        share_repurchases = safe_get(cash_flow, "Repurchase Of Capital Stock")

        # Calculate ratios
        gross_margin = (gross_profit / revenue * 100) if gross_profit and revenue else None
        operating_margin = (operating_income / revenue * 100) if operating_income and revenue else None
        net_margin = (net_income / revenue * 100) if net_income and revenue else None

        roe = (net_income / total_equity * 100) if net_income and total_equity else None
        roa = (net_income / total_assets * 100) if net_income and total_assets else None
        roic = None
        if operating_income and total_debt is not None and total_equity:
            invested_capital = total_debt + total_equity
            if invested_capital > 0:
                roic = (operating_income / invested_capital * 100)

        debt_to_equity = (total_debt / total_equity) if total_debt and total_equity else None
        current_ratio = (current_assets / current_liabilities) if current_assets and current_liabilities else None

        # Growth rates
        revenue_growth = calculate_growth(revenue, revenue_prev)
        earnings_growth = calculate_growth(net_income, net_income_prev)

        # Per share metrics from info
        shares_outstanding = info.get("sharesOutstanding")
        eps = info.get("trailingEps")
        book_value_per_share = info.get("bookValue")

        return {
            "ticker": ticker.upper(),
            "name": info.get("shortName") or info.get("longName"),
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "currency": info.get("currency", "USD"),
            "fiscal_year_end": info.get("lastFiscalYearEnd"),

            # Income Statement
            "income_statement": {
                "revenue": revenue,
                "revenue_growth_yoy": round(revenue_growth, 2) if revenue_growth else None,
                "gross_profit": gross_profit,
                "operating_income": operating_income,
                "ebitda": ebitda,
                "net_income": net_income,
                "earnings_growth_yoy": round(earnings_growth, 2) if earnings_growth else None,
                "eps": eps,
            },

            # Margins
            "margins": {
                "gross_margin": round(gross_margin, 2) if gross_margin else None,
                "operating_margin": round(operating_margin, 2) if operating_margin else None,
                "net_margin": round(net_margin, 2) if net_margin else None,
                "ebitda_margin": round(ebitda / revenue * 100, 2) if ebitda and revenue else None,
            },

            # Balance Sheet
            "balance_sheet": {
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
                "total_equity": total_equity,
                "total_debt": total_debt,
                "cash": cash,
                "net_debt": (total_debt - cash) if total_debt and cash else None,
                "current_assets": current_assets,
                "current_liabilities": current_liabilities,
            },

            # Cash Flow
            "cash_flow": {
                "operating_cash_flow": operating_cf,
                "capital_expenditure": capex,
                "free_cash_flow": free_cash_flow,
                "dividends_paid": dividends_paid,
                "share_repurchases": share_repurchases,
            },

            # Profitability Ratios
            "profitability": {
                "roe": round(roe, 2) if roe else None,
                "roa": round(roa, 2) if roa else None,
                "roic": round(roic, 2) if roic else None,
            },

            # Financial Health
            "financial_health": {
                "debt_to_equity": round(debt_to_equity, 2) if debt_to_equity else None,
                "current_ratio": round(current_ratio, 2) if current_ratio else None,
                "interest_coverage": info.get("interestCoverage"),
                "quick_ratio": info.get("quickRatio"),
            },

            # Valuation
            "valuation": {
                "market_cap": info.get("marketCap"),
                "enterprise_value": info.get("enterpriseValue"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "peg_ratio": info.get("pegRatio"),
                "price_to_book": info.get("priceToBook"),
                "price_to_sales": info.get("priceToSalesTrailing12Months"),
                "ev_to_ebitda": info.get("enterpriseToEbitda"),
                "ev_to_revenue": info.get("enterpriseToRevenue"),
            },

            # Shares & Dividends
            "shares": {
                "shares_outstanding": shares_outstanding,
                "float_shares": info.get("floatShares"),
                "insider_ownership": info.get("heldPercentInsiders"),
                "institutional_ownership": info.get("heldPercentInstitutions"),
            },

            "dividends": {
                "dividend_rate": info.get("dividendRate"),
                "dividend_yield": info.get("dividendYield"),
                "payout_ratio": info.get("payoutRatio"),
                "ex_dividend_date": info.get("exDividendDate"),
            },

            # Company Info
            "company": {
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "employees": info.get("fullTimeEmployees"),
                "description": info.get("longBusinessSummary"),
            }
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e),
            "success": False
        }


def format_currency(val: Optional[float], currency: str = "USD") -> str:
    """Format currency values."""
    if val is None:
        return "N/A"
    symbols = {"USD": "$", "AUD": "A$", "GBP": "£", "EUR": "€"}
    symbol = symbols.get(currency, "$")

    if abs(val) >= 1e12:
        return f"{symbol}{val/1e12:.2f}T"
    if abs(val) >= 1e9:
        return f"{symbol}{val/1e9:.2f}B"
    if abs(val) >= 1e6:
        return f"{symbol}{val/1e6:.2f}M"
    return f"{symbol}{val:,.0f}"


def print_summary(data: dict) -> None:
    """Print a human-readable summary."""
    if not data.get("success"):
        print(f"Error: {data.get('error')}")
        return

    curr = data.get("currency", "USD")
    inc = data["income_statement"]
    mar = data["margins"]
    bal = data["balance_sheet"]
    cf = data["cash_flow"]
    prof = data["profitability"]
    health = data["financial_health"]
    val = data["valuation"]
    div = data["dividends"]

    print(f"""
{'='*70}
FUNDAMENTAL ANALYSIS: {data['ticker']} - {data.get('name', 'Unknown')}
{'='*70}

INCOME STATEMENT (TTM)
  Revenue:           {format_currency(inc.get('revenue'), curr)}  ({inc.get('revenue_growth_yoy', 'N/A'):+.1f}% YoY)
  Gross Profit:      {format_currency(inc.get('gross_profit'), curr)}
  Operating Income:  {format_currency(inc.get('operating_income'), curr)}
  Net Income:        {format_currency(inc.get('net_income'), curr)}  ({inc.get('earnings_growth_yoy', 'N/A'):+.1f}% YoY)
  EPS:               ${inc.get('eps', 'N/A')}

MARGINS
  Gross Margin:      {mar.get('gross_margin', 'N/A')}%
  Operating Margin:  {mar.get('operating_margin', 'N/A')}%
  Net Margin:        {mar.get('net_margin', 'N/A')}%
  EBITDA Margin:     {mar.get('ebitda_margin', 'N/A')}%

BALANCE SHEET
  Total Assets:      {format_currency(bal.get('total_assets'), curr)}
  Total Equity:      {format_currency(bal.get('total_equity'), curr)}
  Total Debt:        {format_currency(bal.get('total_debt'), curr)}
  Cash:              {format_currency(bal.get('cash'), curr)}
  Net Debt:          {format_currency(bal.get('net_debt'), curr)}

CASH FLOW
  Operating CF:      {format_currency(cf.get('operating_cash_flow'), curr)}
  CapEx:             {format_currency(cf.get('capital_expenditure'), curr)}
  Free Cash Flow:    {format_currency(cf.get('free_cash_flow'), curr)}

PROFITABILITY
  ROE:               {prof.get('roe', 'N/A')}%
  ROA:               {prof.get('roa', 'N/A')}%
  ROIC:              {prof.get('roic', 'N/A')}%

FINANCIAL HEALTH
  Debt/Equity:       {health.get('debt_to_equity', 'N/A')}x
  Current Ratio:     {health.get('current_ratio', 'N/A')}x
  Interest Coverage: {health.get('interest_coverage', 'N/A')}x

VALUATION
  Market Cap:        {format_currency(val.get('market_cap'), curr)}
  Enterprise Value:  {format_currency(val.get('enterprise_value'), curr)}
  P/E Ratio:         {val.get('pe_ratio', 'N/A')}x
  Forward P/E:       {val.get('forward_pe', 'N/A')}x
  PEG Ratio:         {val.get('peg_ratio', 'N/A')}x
  P/B Ratio:         {val.get('price_to_book', 'N/A')}x
  EV/EBITDA:         {val.get('ev_to_ebitda', 'N/A')}x

DIVIDENDS
  Dividend Yield:    {div.get('dividend_yield', 0)*100:.2f}% if div.get('dividend_yield') else 'N/A'
  Payout Ratio:      {div.get('payout_ratio', 0)*100:.1f}% if div.get('payout_ratio') else 'N/A'

{'='*70}
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_fundamentals.py TICKER [--json]")
        print("Example: python fetch_fundamentals.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1]
    json_output = "--json" in sys.argv

    data = fetch_fundamentals(ticker)

    if json_output:
        print(json.dumps(data, indent=2, default=str))
    else:
        print_summary(data)
