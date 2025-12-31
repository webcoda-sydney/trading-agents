#!/usr/bin/env python3
"""
Fetch technical analysis indicators for a stock.
Includes RSI, MACD, Bollinger Bands, Moving Averages, and more.

Usage:
    python scripts/fetch_technicals.py AAPL
    python scripts/fetch_technicals.py AAPL --json
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Optional, Tuple

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install yfinance pandas numpy")
    sys.exit(1)

# Try to import pandas-ta for advanced indicators
try:
    import pandas_ta as ta
    HAS_PANDAS_TA = True
except ImportError:
    HAS_PANDAS_TA = False


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate RSI manually if pandas-ta not available."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate MACD manually if pandas-ta not available."""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger(prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate Bollinger Bands."""
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    return upper, sma, lower


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Average True Range."""
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def identify_trend(prices: pd.Series, sma_50: pd.Series, sma_200: pd.Series) -> dict:
    """Identify trend based on moving averages."""
    current = prices.iloc[-1]
    sma50_val = sma_50.iloc[-1]
    sma200_val = sma_200.iloc[-1]

    # Primary trend
    if current > sma200_val and sma50_val > sma200_val:
        primary_trend = "BULLISH"
    elif current < sma200_val and sma50_val < sma200_val:
        primary_trend = "BEARISH"
    else:
        primary_trend = "NEUTRAL"

    # Golden/Death cross detection
    cross = None
    if len(sma_50) > 5 and len(sma_200) > 5:
        # Check last 5 days for crosses
        for i in range(-5, 0):
            prev_50 = sma_50.iloc[i-1]
            curr_50 = sma_50.iloc[i]
            prev_200 = sma_200.iloc[i-1]
            curr_200 = sma_200.iloc[i]

            if prev_50 <= prev_200 and curr_50 > curr_200:
                cross = "GOLDEN_CROSS"
                break
            elif prev_50 >= prev_200 and curr_50 < curr_200:
                cross = "DEATH_CROSS"
                break

    return {
        "primary": primary_trend,
        "price_vs_sma50": "ABOVE" if current > sma50_val else "BELOW",
        "price_vs_sma200": "ABOVE" if current > sma200_val else "BELOW",
        "sma50_vs_sma200": "ABOVE" if sma50_val > sma200_val else "BELOW",
        "recent_cross": cross,
    }


def identify_support_resistance(high: pd.Series, low: pd.Series, close: pd.Series) -> dict:
    """Identify key support and resistance levels."""
    # Use pivot points and recent highs/lows
    recent_high = high.tail(20).max()
    recent_low = low.tail(20).min()
    current = close.iloc[-1]

    # Simple pivot calculation
    pivot = (recent_high + recent_low + current) / 3
    r1 = 2 * pivot - recent_low
    r2 = pivot + (recent_high - recent_low)
    s1 = 2 * pivot - recent_high
    s2 = pivot - (recent_high - recent_low)

    return {
        "resistance_1": round(r1, 2),
        "resistance_2": round(r2, 2),
        "pivot": round(pivot, 2),
        "support_1": round(s1, 2),
        "support_2": round(s2, 2),
        "recent_high": round(recent_high, 2),
        "recent_low": round(recent_low, 2),
    }


def generate_signal(rsi: float, macd_hist: float, bb_position: float, trend: str) -> dict:
    """Generate overall technical signal."""
    signals = []
    score = 50  # Neutral starting point

    # RSI signals
    if rsi < 30:
        signals.append("RSI oversold (bullish)")
        score += 15
    elif rsi > 70:
        signals.append("RSI overbought (bearish)")
        score -= 15
    elif rsi < 40:
        signals.append("RSI approaching oversold")
        score += 5

    # MACD signals
    if macd_hist > 0:
        signals.append("MACD bullish")
        score += 10
    else:
        signals.append("MACD bearish")
        score -= 10

    # Bollinger Band position
    if bb_position < 0:
        signals.append("Below lower Bollinger (oversold)")
        score += 10
    elif bb_position > 100:
        signals.append("Above upper Bollinger (overbought)")
        score -= 10

    # Trend
    if trend == "BULLISH":
        signals.append("Uptrend confirmed")
        score += 15
    elif trend == "BEARISH":
        signals.append("Downtrend confirmed")
        score -= 15

    # Normalize score to 0-100
    score = max(0, min(100, score))

    # Generate rating
    if score >= 70:
        rating = "STRONG_BUY"
    elif score >= 55:
        rating = "BUY"
    elif score >= 45:
        rating = "HOLD"
    elif score >= 30:
        rating = "SELL"
    else:
        rating = "STRONG_SELL"

    return {
        "score": score,
        "rating": rating,
        "signals": signals,
    }


def fetch_technicals(ticker: str) -> dict:
    """Fetch technical analysis data for a ticker."""
    try:
        stock = yf.Ticker(ticker)

        # Get 1 year of daily data for technical analysis
        hist = stock.history(period="1y")

        if hist.empty:
            return {
                "ticker": ticker,
                "error": f"No historical data found for {ticker}",
                "success": False
            }

        close = hist['Close']
        high = hist['High']
        low = hist['Low']
        volume = hist['Volume']
        current_price = close.iloc[-1]

        # Moving Averages
        sma_20 = close.rolling(window=20).mean()
        sma_50 = close.rolling(window=50).mean()
        sma_200 = close.rolling(window=200).mean()
        ema_12 = close.ewm(span=12, adjust=False).mean()
        ema_26 = close.ewm(span=26, adjust=False).mean()

        # RSI
        if HAS_PANDAS_TA:
            rsi = ta.rsi(close, length=14)
        else:
            rsi = calculate_rsi(close, 14)

        # MACD
        macd_line, signal_line, macd_hist = calculate_macd(close)

        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = calculate_bollinger(close)

        # ATR (volatility)
        atr = calculate_atr(high, low, close)

        # Stochastic (if pandas-ta available)
        stoch_k = stoch_d = None
        if HAS_PANDAS_TA:
            stoch = ta.stoch(high, low, close)
            if stoch is not None and not stoch.empty:
                stoch_k = stoch.iloc[-1, 0]
                stoch_d = stoch.iloc[-1, 1]

        # Volume analysis
        avg_volume_20 = volume.rolling(window=20).mean().iloc[-1]
        volume_ratio = volume.iloc[-1] / avg_volume_20 if avg_volume_20 > 0 else 1

        # Trend identification
        trend = identify_trend(close, sma_50, sma_200)

        # Support/Resistance
        support_resistance = identify_support_resistance(high, low, close)

        # Calculate Bollinger Band position (0 = at lower, 100 = at upper)
        bb_range = bb_upper.iloc[-1] - bb_lower.iloc[-1]
        bb_position = ((current_price - bb_lower.iloc[-1]) / bb_range * 100) if bb_range > 0 else 50

        # Generate signal
        signal = generate_signal(
            rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50,
            macd_hist.iloc[-1] if not pd.isna(macd_hist.iloc[-1]) else 0,
            bb_position,
            trend["primary"]
        )

        return {
            "ticker": ticker.upper(),
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "current_price": round(current_price, 2),

            # Moving Averages
            "moving_averages": {
                "sma_20": round(sma_20.iloc[-1], 2) if not pd.isna(sma_20.iloc[-1]) else None,
                "sma_50": round(sma_50.iloc[-1], 2) if not pd.isna(sma_50.iloc[-1]) else None,
                "sma_200": round(sma_200.iloc[-1], 2) if not pd.isna(sma_200.iloc[-1]) else None,
                "ema_12": round(ema_12.iloc[-1], 2) if not pd.isna(ema_12.iloc[-1]) else None,
                "ema_26": round(ema_26.iloc[-1], 2) if not pd.isna(ema_26.iloc[-1]) else None,
            },

            # Oscillators
            "oscillators": {
                "rsi_14": round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else None,
                "rsi_signal": "OVERSOLD" if rsi.iloc[-1] < 30 else ("OVERBOUGHT" if rsi.iloc[-1] > 70 else "NEUTRAL"),
                "stochastic_k": round(stoch_k, 2) if stoch_k else None,
                "stochastic_d": round(stoch_d, 2) if stoch_d else None,
            },

            # MACD
            "macd": {
                "macd_line": round(macd_line.iloc[-1], 4) if not pd.isna(macd_line.iloc[-1]) else None,
                "signal_line": round(signal_line.iloc[-1], 4) if not pd.isna(signal_line.iloc[-1]) else None,
                "histogram": round(macd_hist.iloc[-1], 4) if not pd.isna(macd_hist.iloc[-1]) else None,
                "signal": "BULLISH" if macd_hist.iloc[-1] > 0 else "BEARISH",
            },

            # Bollinger Bands
            "bollinger_bands": {
                "upper": round(bb_upper.iloc[-1], 2) if not pd.isna(bb_upper.iloc[-1]) else None,
                "middle": round(bb_middle.iloc[-1], 2) if not pd.isna(bb_middle.iloc[-1]) else None,
                "lower": round(bb_lower.iloc[-1], 2) if not pd.isna(bb_lower.iloc[-1]) else None,
                "position_pct": round(bb_position, 1),
                "width": round((bb_upper.iloc[-1] - bb_lower.iloc[-1]) / bb_middle.iloc[-1] * 100, 2) if bb_middle.iloc[-1] else None,
            },

            # Volatility
            "volatility": {
                "atr_14": round(atr.iloc[-1], 2) if not pd.isna(atr.iloc[-1]) else None,
                "atr_pct": round(atr.iloc[-1] / current_price * 100, 2) if not pd.isna(atr.iloc[-1]) else None,
            },

            # Volume
            "volume": {
                "current": int(volume.iloc[-1]),
                "average_20d": int(avg_volume_20),
                "ratio": round(volume_ratio, 2),
                "signal": "HIGH" if volume_ratio > 1.5 else ("LOW" if volume_ratio < 0.5 else "NORMAL"),
            },

            # Trend
            "trend": trend,

            # Support/Resistance
            "support_resistance": support_resistance,

            # Overall Signal
            "signal": signal,
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

    ma = data["moving_averages"]
    osc = data["oscillators"]
    macd = data["macd"]
    bb = data["bollinger_bands"]
    vol = data["volatility"]
    volume = data["volume"]
    trend = data["trend"]
    sr = data["support_resistance"]
    sig = data["signal"]

    print(f"""
{'='*70}
TECHNICAL ANALYSIS: {data['ticker']} @ ${data['current_price']}
{'='*70}

OVERALL SIGNAL: {sig['rating']} (Score: {sig['score']}/100)
{'-'*70}
{chr(10).join(f"  - {s}" for s in sig['signals'])}

TREND ANALYSIS
  Primary Trend:    {trend['primary']}
  Price vs SMA50:   {trend['price_vs_sma50']}
  Price vs SMA200:  {trend['price_vs_sma200']}
  SMA50 vs SMA200:  {trend['sma50_vs_sma200']}
  Recent Cross:     {trend['recent_cross'] or 'None'}

MOVING AVERAGES
  SMA 20:           ${ma.get('sma_20', 'N/A')}
  SMA 50:           ${ma.get('sma_50', 'N/A')}
  SMA 200:          ${ma.get('sma_200', 'N/A')}
  EMA 12:           ${ma.get('ema_12', 'N/A')}
  EMA 26:           ${ma.get('ema_26', 'N/A')}

OSCILLATORS
  RSI (14):         {osc.get('rsi_14', 'N/A')} ({osc.get('rsi_signal', 'N/A')})
  Stochastic %K:    {osc.get('stochastic_k', 'N/A')}
  Stochastic %D:    {osc.get('stochastic_d', 'N/A')}

MACD
  MACD Line:        {macd.get('macd_line', 'N/A')}
  Signal Line:      {macd.get('signal_line', 'N/A')}
  Histogram:        {macd.get('histogram', 'N/A')} ({macd.get('signal', 'N/A')})

BOLLINGER BANDS
  Upper:            ${bb.get('upper', 'N/A')}
  Middle:           ${bb.get('middle', 'N/A')}
  Lower:            ${bb.get('lower', 'N/A')}
  Position:         {bb.get('position_pct', 'N/A')}% (0=lower, 100=upper)
  Width:            {bb.get('width', 'N/A')}%

VOLATILITY
  ATR (14):         ${vol.get('atr_14', 'N/A')} ({vol.get('atr_pct', 'N/A')}%)

VOLUME
  Current:          {volume.get('current', 'N/A'):,}
  20-Day Avg:       {volume.get('average_20d', 'N/A'):,}
  Ratio:            {volume.get('ratio', 'N/A')}x ({volume.get('signal', 'N/A')})

SUPPORT & RESISTANCE
  Resistance 2:     ${sr.get('resistance_2', 'N/A')}
  Resistance 1:     ${sr.get('resistance_1', 'N/A')}
  Pivot:            ${sr.get('pivot', 'N/A')}
  Support 1:        ${sr.get('support_1', 'N/A')}
  Support 2:        ${sr.get('support_2', 'N/A')}

{'='*70}
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_technicals.py TICKER [--json]")
        print("Example: python fetch_technicals.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1]
    json_output = "--json" in sys.argv

    data = fetch_technicals(ticker)

    if json_output:
        print(json.dumps(data, indent=2, default=str))
    else:
        print_summary(data)
