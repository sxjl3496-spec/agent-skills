---
name: wind-terminal-data-extraction
description: Navigating Wind Financial Terminal (万得金融终端) to extract financial data — options, equities, bonds, macro, etc. Covers keyboard shortcuts, module navigation, Excel plugin batch extraction, and Wind API usage.
triggers:
  - user mentions Wind, 万得, Wind金融终端, or WSD/WSD functions
  - user needs to extract financial data from a Chinese financial data terminal
  - user asks about options data, Greek letters, or derivatives data sourcing
  - user references WebVPN access to Wind (common in Chinese universities)
---

# Wind Financial Terminal — Data Extraction Guide

> **Related skill**: For analyzing the data you extract (reading charts, capital flow patterns, institutional behavior), see `a-share-stock-analysis`.

## Quick Navigation (Keyboard Shortcuts)

Wind uses a **keyboard wizard** (键盘精灵) — type any shortcut command in the search bar to jump directly to a module.

### Options (期权) Module
| Function | Command | Description |
|---|---|---|
| Options Overview Screen | `10` | T-quote display, IV smile, 3-chart layout |
| Strategy Analysis | `OSA` | Custom strategy backtesting, 8 classic strategies |
| Volatility Surface | `OVS` | 3D IV surface, term structure, skew |
| Options Special Stats | `OSR` | Contract info, daily quotes, volume/OI rankings |
| Options Deep Info | `F9` | Per-contract overview, vol analysis, news |
| Options Pricing Calc | `OVC` | Theoretical price + Greeks (Delta/Gamma/Vega/Theta/Rho) |
| Options Combo Calc | `OPC` | Multi-leg portfolio pricing |

### Stock Module
| Function | Command | Description |
|---|---|---|
| Data Browser | `EDE` | Time-series data for individual stocks |
| Financial Comparison | `FA` | Financial statements across periods |
| Deep Info | `F9` | Company overview, shareholders, financials |
| Conditional Stock Picker | `EQS` | Screen stocks by 10,000+ indicators |

### Macro/Bond
| Function | Command | Description |
|---|---|---|
| Economic Database | `EDB` | China macro (EDBC), industry (EDBI), global (EDBG) |
| Bond Calculator | `BC1` | Bond pricing, yield calculation |
| Yield Curve | `YC` | Term structure analysis |

### Index/Futures
| Function | Command | Description |
|---|---|---|
| Stock Index Futures Screen | `6` | Real-time stock index futures |
| Index Data Browser | `IDE` | Index time-series extraction |
| Index Financial Comparison | `IFA` | Index constituent financials |

## Workflow: Extracting Options Data (SSE 50ETF Example)

### What data is available where:

| Data Field | Source Module | Notes |
|---|---|---|
| Date, Close, Volume, OI | `OSR` → Daily Quotes | Bulk export available |
| Strike, Option Name, Expiry | `OSR` → Contract Info | Contract master list |
| Delta, Gamma, Vega, Theta, Rho | `OVC` (single) or Excel plugin (batch) | OVC is per-contract; use WSD for batch |
| Risk-free Rate | `EDB` → China Government Bond Yield | Use 1-year CGB yield as proxy |
| Asset Price (underlying) | Direct quote or `WSD` | e.g., 510050.SH for 50ETF |
| Time-to-Expiry | Calculate manually | (Expiry Date - Date) / 365 |

### Step-by-step:
1. **Get contract list**: `OSR` → 沪深交易所期权 → 上证50ETF期权 → Contract Info → Export
2. **Get daily quotes**: `OSR` → Daily Quotes for each contract → Export
3. **Get Greeks**: `OVC` for single contracts, or Excel plugin for batch
4. **Get risk-free rate**: `EDB` → EDBC → 金融 → 利率 → 中国国债收益率 → 1年期
5. **Get underlying price**: `WSD("510050.SH", "close", start, end)`

## Excel Plugin (Batch Extraction)

Wind Excel plugin uses unified function syntax. Key functions:

### WSD — Historical Data (Time Series)
```
=WSD("instrument", "indicator1;indicator2", "startDate", "endDate", "params")
```
Examples:
```
=WSD("510050.SH", "close;volume;oi", "2024-01-01", "2025-06-12")
=WSD("10005369.SH", "close;delta;gamma;vega;theta;rho", "2024-01-01", "2025-06-12")
```

### WSS — Cross-Sectional Data (Snapshot)
```
=WSS("instruments", "indicators", "params")
```

### WSQ — Real-time Quotes
```
=WSQ("instrument", "indicator1;indicator2")
```

### EDB — Economic Database
```
=EDB("indicatorCode", "startDate", "endDate")
```

### Batch pattern for options:
1. Export all contract codes from `OSR`
2. For each contract, call `WSD` with desired indicators
3. Combine results in a single sheet

## Wind API (Python)

Wind API supports Python, Matlab, R, VBA, C#, C++.

### Setup:
```python
from WindPy import w
w.start()
```

### Get options data:
```python
# Daily close + volume for a specific contract
data = w.wsd("10005369.SH", "close;volume;oi;delta;gamma;vega;theta;rho",
             "2024-01-01", "2025-06-12")

# Get all 50ETF option contracts
contracts = w.wset("optioncontractset", "exchange=SSE;underlying=510050.SH")
```

### Code Generator:
Wind provides a **Code Generator** (快捷键 `CG`) — visually select parameters and auto-generate API code.

## Alternative Data Sources

If Wind terminal access is unavailable, see `references/science-databank-alternative.md` for Science Data Bank and other alternative sources for SSE 50ETF options data.

## Common Pitfalls

1. **Contract codes change**: Options have limited lifetimes. You need ALL contract codes across the period, not just current ones. Use `OSR` contract master list to get historical contract codes.

2. **Greeks are model-dependent**: Wind's Greeks use Black-Scholes for European-style options. The `OVC` calculator lets you adjust parameters (vol model, rate, etc.).

3. **Risk-free rate proxy**: Wind doesn't always bundle the risk-free rate with options data. You typically need to separately extract 1-year or 3-month CGB yield from `EDB` and merge.

4. **Time-to-Expiry calculation**: Wind provides `expiry_date` in contract info but `time_to_expiry` as a continuous variable may need manual calculation: `(expiry - date) / 365` or `/ 252` depending on convention.

5. **WebVPN access**: Many Chinese universities provide Wind access via WebVPN (e.g., `webvpn.swufe.edu.cn`). The Wind terminal runs as a thin client through the browser — all keyboard shortcuts work the same way.

6. **Excel plugin installation**: The Wind Excel plugin is installed with the Wind client. If missing, check Wind installation directory for the add-in file and register it in Excel.

7. **WebVPN web portal (WDS) vs desktop terminal**: When accessing Wind through a university WebVPN (e.g., `webvpn.swufe.edu.cn`), the interface is the **WDS web portal**, NOT the desktop terminal. The web version has a different layout — there may be no obvious search bar or keyboard wizard. Look for:
   - A **top navigation bar** with tabs like 行情 | 数据 | 研究 | 工具
   - **Left sidebar menu** with expandable category tree
   - **Homepage icon cards** (股票 | 债券 | 期货 | 期权 | etc.)
   - Try appending URL hash fragments like `#/option/OSR` to navigate directly
   - If completely stuck, ask the user to screenshot the page — the web UI varies by deployment
