# Sector Analysis

Analyse ASX sectors to identify opportunities and trends.

## Arguments
- `$ARGUMENTS` - Sector name or `all` for overview

## Sectors Available
- `materials` - Mining, metals, chemicals (BHP, RIO, FMG)
- `financials` - Banks, insurance (CBA, NAB, WBC, ANZ)
- `healthcare` - Biotech, medical (CSL, COH, RMD)
- `consumer` - Retail, discretionary (WES, JBH)
- `staples` - Consumer staples (WOW, COL)
- `energy` - Oil, gas, renewables (WDS, STO, ORG)
- `tech` - Technology (XRO, WTC, ALU)
- `realestate` - REITs, property (GMG, SGP, DXS)
- `industrials` - Infrastructure (TCL, BXB)
- `utilities` - Utilities (APA)

## Examples
```
/sector all           # Overview of all sectors
/sector financials    # Deep dive into financials
/sector materials     # Mining and resources analysis
```

## Instructions

**If `all` or no arguments:**
1. Load `data/fundamentals-cache.json`
2. Group stocks by sector
3. Calculate sector averages:
   - Average P/E ratio
   - Average dividend yield
   - Total market cap
   - Average YTD performance

4. Display sector comparison:
```
ASX SECTOR OVERVIEW
===================

SECTOR          STOCKS   AVG P/E   AVG DIV   MKT CAP    STATUS
---------------------------------------------------------------------
Financials      8        12.5      5.2%      $450B      Undervalued
Materials       10       15.2      3.8%      $320B      Fair value
Healthcare      4        35.0      1.2%      $180B      Premium
...

SECTOR RANKINGS
---------------
Best value:     Financials (P/E: 12.5)
Best dividend:  Financials (Yield: 5.2%)
Best growth:    Healthcare (momentum)
Most defensive: Utilities, Staples

PORTFOLIO EXPOSURE
------------------
[If positions exist, show current sector allocation vs benchmark]
```

**If specific sector:**
1. Filter stocks in that sector
2. Rank by various criteria
3. Show detailed breakdown:

```
SECTOR ANALYSIS: Financials
===========================

STOCKS IN SECTOR
----------------
TICKER   NAME                   PRICE     P/E      DIV %    MKT CAP
CBA      Commonwealth Bank      $108.75   15.2     4.2%     $175B
NAB      National Australia     $33.25    11.2     5.8%     $95B
WBC      Westpac Banking        $25.50    10.8     6.2%     $88B
ANZ      ANZ Group              $28.00    11.5     5.5%     $80B
...

SECTOR METRICS
--------------
Average P/E:        12.5
Average Div Yield:  5.2%
Total Market Cap:   $450B

TOP PICKS IN SECTOR
-------------------
Best value:    WBC (lowest P/E at 10.8)
Best dividend: WBC (highest yield at 6.2%)
Best quality:  CBA (highest ROE)

SECTOR OUTLOOK
--------------
[Brief 2-3 sentence outlook for the sector]

NEXT STEPS
----------
/research WBC  - Research top sector pick
/scan value    - Find value stocks across all sectors
```
