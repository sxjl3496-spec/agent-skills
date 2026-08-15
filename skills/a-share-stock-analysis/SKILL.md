---
name: a-share-stock-analysis
description: Analyzing A-share stocks using 东方财富/Wind data — reading intraday/K-line charts, analyzing capital flow (资金流向), correlating corporate announcements with price action, and inferring institutional (主力) behavior patterns.
triggers:
  - user shows stock charts (东方财富, 同花顺, Wind) and asks for analysis
  - user asks about 主力资金, capital flow, or institutional behavior
  - user asks to analyze corporate announcements and their market impact
  - user mentions 涨停, 跌停, 澄清公告, 割肉, or similar A-share terminology
  - user asks "为什么股价跌了/涨了" or "主力在干什么"
---

# A-Share Stock Analysis Guide

## 1. Reading Intraday Charts (分时图)

### Volume Bar Colors (成交量柱子)
| Color | Meaning |
|-------|---------|
| **Red (红柱)** | Price **UP** from previous tick — buying pressure dominant |
| **Green (绿柱)** | Price **DOWN** from previous tick — selling pressure dominant |
| **Bar height** | Volume at that time segment |

This is universal across 东方财富, 同花顺, Wind, etc.

### Key Metrics on Intraday Screen
- **现量**: Current tick volume
- **分时量**: Volume in current time segment
- **总手**: Total daily volume (in lots/手)
- **换手**: Turnover rate (volume / circulating shares)
- **金额**: Trading value (in RMB)

## 2. Reading K-Line Charts (日K/周K/月K)

### Moving Averages (均线)
- **MA5**: 5-day moving average (short-term trend)
- **MA10**: 10-day moving average
- **MA20**: 20-day moving average (medium-term trend)
- When price > MA = bullish; price < MA = bearish
- MA crossover (金叉/死叉) signals trend changes

### Chip Distribution (筹码分布)
- **获利比例**: % of shares currently profitable
- **平均成本**: Average holding cost of all shareholders
- **90%筹码**: Price range containing 90% of shares
- **集中度**: Chip concentration (lower = more concentrated)
- Low 获利比例 + high average cost → most holders are trapped (套牢)

## 3. Capital Flow Analysis (资金流向)

### Four Categories of Capital
| Category | Chinese | Typical Behavior |
|----------|---------|------------------|
| **Super-large** | 超大单 | Institutions, funds (smart money) |
| **Large** | 大单 | Big retail, small institutions |
| **Medium** | 中单 | Medium retail |
| **Small** | 小单 | Small retail (dumb money) |

### Interpreting Flow Patterns
- **超大+大单净流出, 中+小单净流入** → Institutions selling to retail (bearish)
- **超大+大单净流入, 中+小单净流出** → Institutions accumulating (bullish)
- **All categories net outflow** → Panic selling, no buyers
- **All categories net inflow** → Broad buying interest

### Red Flag: "Smart Money" Outflow After News
If 超大+大单 net outflow > 20% of daily volume → significant institutional exit

## 4. Corporate Announcement Analysis (公告分析)

### Common Announcement Types
| Type | Chinese | Market Impact |
|------|---------|---------------|
| **Clarification** | 澄清公告 | Usually bearish (kills speculation) |
| **Profit warning** | 业绩预告 | Depends on direction |
| **Major contract** | 重大合同 | Usually bullish |
| **Insider trading** | 高管变动 | Uncertain |
| **Dividend** | 分红送转 | Usually neutral to slightly bullish |

### Suspicious Announcement Patterns
1. **"跌不问、涨就管"**: Company silent during price decline, but immediately issues clarification when price rises → possible collusion or regulatory pressure
2. **Weekend clarifications after Friday limit-up**: Timing designed to maximize negative impact on Monday open → watch for this pattern
3. **Vague denials**: Company denies involvement without addressing core claims → may be technically true but misleading

## 5. Common Institutional Behavior Patterns

### Pattern 1: "炒作→澄清→出逃"
```
Day 1 (Fri): Rumor spreads → stock hits 涨停, institutions buy heavily
Day 2 (Sat): Company issues 澄清公告 denying rumor
Day 3 (Mon): Institutions dump shares, stock falls 5%+, volume spikes
```
**Key indicators**:
- Friday 涨停 with 超大量
- Saturday 澄清公告
- Monday 大跌 with 超大+大单净流出

### Pattern 2: "洗盘→拉升"
```
Phase 1: Price drops on low volume (shaking out weak hands)
Phase 2: Institutions accumulate quietly
Phase 3: Price rises on increasing volume
```

### Pattern 3: "出货→阴跌"
```
Phase 1: Price at peak, high volume, institutions selling
Phase 2: Price slowly declines on decreasing volume
Phase 3: Retail left holding bags
```

## 6. Reconstructing Institutional Moves

### Step-by-Step Analysis
1. **Check 5-day chart**: Identify volume spikes and price movements
2. **Check capital flow**: See if 超大+大单 moved with price
3. **Check announcements**: Look for news that explains the move
4. **Check timing**: Did announcements come before/after the move?
5. **Calculate P&L**: If institutions bought at X and sold at X±Y%, what was their gain/loss?

### Example: Analyzing "主力割肉"
```
Evidence needed:
- Day N: 超大量 + price spike → institutions buying
- Day N+1 or N+2: 澄清公告 or bad news
- Day N+2 or N+3: 大跌 + 超大+大单净流出 → institutions cutting losses

Calculate:
- Buy price (average of Day N high/low)
- Sell price (average of exit day high/low)
- Loss % = (sell - buy) / buy × 100%
```

## 7. Data Sources for A-Share Analysis

| Data | 东方财富 | Wind | Notes |
|------|---------|------|-------|
| Intraday charts | ✅ Free | ✅ | Real-time |
| Capital flow | ✅ Free | ✅ | Daily summary |
| Announcements | ✅ Free | ✅ | 巨潮资讯网 is authoritative |
| K-line charts | ✅ Free | ✅ | Historical |
| Chip distribution | ✅ Free | ✅ | Estimated |
| Institutional holdings | ⚠️ Limited | ✅ | 季报 data |

## Pitfalls

1. **Correlation ≠ causation**: High volume doesn't always mean institutions are buying; could be institutions selling to retail
2. **Capital flow data is estimated**: Different platforms may show different numbers for the same stock
3. **Announcements may be incomplete**: Company may deny specific claims while the underlying story has truth
4. **Timing matters**: A 澄清公告 on Saturday affects Monday's opening differently than one during trading hours
5. **Don't assume all institutions are smart**: Some funds buy high and sell low too

## References

See `references/case-study-zhonghangxifei.md` for a detailed case study of the "炒作→澄清→出逃" pattern with 中航西飞 (000768).
