---
name: academic-figure
description: >
  学术论文配图制作。适用于SCI/Nature/IEEE等高质量期刊的论文图表制作。当用户需要：(1) 制作论文配图，(2) 科研数据可视化，(3) 多面板科学图表，(4) 期刊级PDF/SVG/TIFF输出。支持Python(matplotlib/seaborn)和R(ggplot2)。触发词："论文配图"、"科研绘图"、"画图"、"作图"、"出图"、"论文图表"、"可视化"、"figure"。
---

# 学术论文配图制作 (Academic Figure)

## 概述

本技能提供从图表设计到期刊级输出的完整科研绘图流程，确保图表符合高水平期刊的投稿要求。

**支持后端**: Python (matplotlib/seaborn) 或 R (ggplot2/patchwork)

---

## 何时使用

- 制作论文配图（单图或多面板）
- 科研数据可视化
- 需要期刊级输出（PDF/SVG/TIFF/EPS）
- 优化现有图表质量
- 制作方法流程图、实验结果图、对比图

**触发词**: "论文配图"、"科研绘图"、"画图"、"作图"、"出图"、"figure"、"plot"、"可视化"

---

## 工作流程

### 第1步：图表契约（设计前必做）

在写任何代码之前，必须明确：

1. **核心结论**: 这张图要传达什么科学结论？
2. **证据链**: 数据如何支撑这个结论？
3. **图表类型**: 属于哪种原型？
   - 比较型（bar/box/violin plot）
   - 关系型（scatter/heatmap）
   - 分布型（histogram/density）
   - 时序型（line/area）
   - 组合型（multi-panel figure）
4. **输出需求**: 期刊、格式（PDF/SVG/TIFF）、尺寸、分辨率
5. **审稿风险**: 可能被审稿人质疑什么？

### 第2步：后端选择

**如果用户未明确选择Python或R，必须询问："Python还是R？"**

选择后，整个绘图过程只用该后端。

### 第3步：图表制作

#### Python (matplotlib/seaborn) 快速设置

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 期刊级默认设置
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})
```

#### R (ggplot2) 快速设置

```r
library(ggplot2)
library(patchwork)

theme_journal <- theme_bw(base_size = 10) +
  theme(
    text = element_text(family = "serif"),
    panel.grid.minor = element_blank(),
    legend.position = "bottom"
  )
```

### 第4步：设计原则

#### 核心原则
1. **图表服务于科学逻辑**: 美观从属于结论清晰
2. **英雄面板**: 多面板图中，最重要的面板放在最显眼位置
3. **克制调色板**: 不超过5-7种颜色，优先使用色盲友好配色
4. **统计完整性**: 误差棒、p值、样本量直接标注在图上

#### 配色推荐

**Python 色盲友好配色**:
```python
# Nature 风格
nature_colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', 
                 '#F39B7F', '#8491B4', '#91D1C2', '#DC0000']

# 期刊通用
journal_colors = sns.color_palette("colorblind", 8)
```

#### 尺寸规范

| 图表类型 | 单栏 | 1.5栏 | 双栏 |
|---------|------|-------|------|
| 简单图 | 89mm | - | 183mm |
| 多面板 | - | 120mm | 183mm |
| 高度 | 60-80mm | 80-120mm | 100-150mm |

### 第5步：输出与质量检查

#### 导出设置

```python
# PDF (矢量图，推荐)
fig.savefig('figure1.pdf', format='pdf', bbox_inches='tight')

# TIFF (300dpi，某些期刊要求)
fig.savefig('figure1.tiff', format='tiff', dpi=300, bbox_inches='tight')

# SVG (可编辑矢量图)
fig.savefig('figure1.svg', format='svg', bbox_inches='tight')
```

#### 质量检查清单

- [ ] 核心结论在3秒内可识别
- [ ] 所有轴标签清晰可读
- [ ] 图例简洁明了
- [ ] 字体大小≥8pt（缩放后）
- [ ] 颜色在灰度打印下可区分
- [ ] 统计信息完整（n值、p值、误差棒说明）
- [ ] 分辨率≥300 DPI
- [ ] 格式符合目标期刊要求
- [ ] 多面板标签 (a), (b), (c) 正确标注

---

## 常见图表类型速查

### 比较型
- **柱状图**: `plt.bar()` / `geom_bar()`
- **箱线图**: `plt.boxplot()` / `geom_boxplot()`
- **小提琴图**: `sns.violinplot()` / `geom_violin()`

### 关系型
- **散点图**: `plt.scatter()` / `geom_point()`
- **热力图**: `sns.heatmap()` / `geom_tile()`
- **相关矩阵**: `sns.heatmap(df.corr())`

### 分布型
- **直方图**: `plt.hist()` / `geom_histogram()`
- **密度图**: `sns.kdeplot()` / `geom_density()`

### 时序型
- **折线图**: `plt.plot()` / `geom_line()`
- **面积图**: `plt.fill_between()` / `geom_ribbon()`

### 多面板组合
```python
fig, axes = plt.subplots(2, 2, figsize=(183/25.4, 150/25.4))
# 183mm = 双栏宽度
```

```r
p1 + p2 + p3 + p4 + 
  plot_layout(ncol = 2) +
  plot_annotation(tag_levels = 'a')
```

---

## 常见问题

### 中文字体显示问题
```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
```

### 图表太拥挤
- 减少非数据墨水（chartjunk）
- 使用 `plt.tight_layout()`
- 考虑拆分为多面板

### 颜色在打印后不可区分
- 使用色盲友好调色板
- 同时用颜色+形状/纹理区分数据系列

---

## 最佳实践

1. **先设计再编码**: 明确图表契约后再写代码
2. **少即是多**: 移除所有非必要元素
3. **一致性**: 同一篇论文的图表使用统一配色和风格
4. **可复现**: 保存完整的绘图代码
5. **预留修改空间**: 用矢量格式保存，方便后期调整
