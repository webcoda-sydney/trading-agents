# Market Scanner

Screen ASX stocks using predefined investment strategies.

## Arguments
- `$ARGUMENTS` - Screening preset name or action

## Presets Available
- `value` - Low P/E, high dividend yield, undervalued stocks
- `growth` - High revenue growth, strong ROE
- `dividend` - High yield dividend payers (5%+)
- `momentum` - Stocks near 52-week highs
- `quality` - High ROE, low debt, strong fundamentals
- `bluechip` - Large cap stable companies
- `smallcap_value` - Undervalued small companies

## Examples
```
/scan value           # Screen for value stocks
/scan dividend        # High dividend yield stocks
/scan momentum        # Stocks with momentum
/scan --list          # Show all available presets
/scan --update        # Refresh fundamentals cache (takes 5+ mins)
```

## Instructions

Based on `$ARGUMENTS`:

**If preset name (value, growth, dividend, etc.):**
1. Check if fundamentals cache exists (`data/fundamentals-cache.json`)
2. If cache is missing or >24 hours old, suggest running `--update` first
3. Run: `python scripts/market_scanner.py [preset]`
4. Display results in formatted table
5. Save results to `data/scan-results/`
6. Suggest top picks for further research

**If `--list`:**
1. Run: `python scripts/market_scanner.py --list`
2. Display all available presets with their criteria

**If `--update`:**
1. Warn user this takes 5-10 minutes
2. Run: `python scripts/market_scanner.py --update`
3. Fetches fundamentals for all 50 ASX stocks in ticker list
4. Updates cache file

**Display format:**
```
SCREENING: Value Investing
Undervalued stocks with strong fundamentals
============================================

Found 8 stocks:

TICKER   NAME                      PRICE        P/E     DIV %    MKT CAP
---------------------------------------------------------------------------
NAB      National Australia Bank   $33.25      11.2     5.8%     $95.2B
WBC      Westpac Banking           $25.50      10.8     6.2%     $88.4B
...

Next steps:
  /research NAB  - Research top pick
  /watchlist add NAB  - Add to watchlist
```

**After displaying results:**
- Highlight the top 3 picks
- Explain why they scored well on the criteria
- Suggest adding top picks to watchlist for monitoring
