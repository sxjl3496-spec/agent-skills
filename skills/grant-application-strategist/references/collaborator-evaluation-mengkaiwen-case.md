# 合作者评估案例：孟开文教授（西南财经大学数学学院，博士导师）

> 来源：2026年8月1日会话
> 场景：申报湖南省自科基金青年A类，考虑邀请博士导师作为项目组成员

---

## 一、背景

申报人（冯泽宇）的博士导师，西南财经大学数学学院教授。申报人课题涉及绿波信号优化的MILP求解和出行权交易市场均衡分析，需要运筹学/最优化方向的合作者补短板。

## 二、评估方法

### Google Scholar 搜索（通过 Clash 代理端口7897）

Google Scholar 对频繁请求会返回CSS重定向页面而非搜索结果。当 Scholar 直接搜索作者名失效时，用以下降级策略：

### arXiv API（⭐ 可靠替代方案）

当 Google Scholar 搜索返回空结果或CSS时，arXiv API 是查找研究者预印本的可靠途径：

```python
import requests

resp = requests.get(
    'http://export.arxiv.org/api/query?search_query=au:"Kaiwen Meng"&max_results=15',
    proxies={'http': 'http://127.0.0.1:7897', 'https': 'http://127.0.0.1:7897'},
    timeout=20
)
# 解析 Atom feed
import re
entries = re.findall(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
for entry in entries:
    title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL).group(1).strip()
    authors = re.findall(r'<name>(.*?)</name>', entry)
    date = re.search(r'<published>(.*?)</published>', entry).group(1)[:10]
    summary = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL).group(1).strip()[:200]
```

**优势**：arXiv API 返回结构化 XML（Atom feed），不依赖JS渲染，不受反爬限制。
**局限**：只能找到发在arXiv上的预印本，期刊论文需通过Scholar补充。

### 搜索策略：多关键词交叉

1. 搜索 `"K Meng" "X Yang"` （合作者+常见共同作者）→ 获取期刊论文
2. 搜索 `au:"Kaiwen Meng"` on arXiv API → 获取预印本
3. 两者合并去重，构建完整论文清单

## 三、评估结果

### 基本信息

| 项目 | 内容 |
|:---|:---|
| 姓名 | 孟开文（Kaiwen Meng / KW Meng） |
| 职务 | 西南财经大学数学学院，教授 |
| 英文论文 | 17篇+（另4篇arXiv预印本） |
| 最高单篇引用 | **186次**（Group sparse optimization, JMLR 2017） |
| 核心方向 | **变分分析、最优化理论、误差界、稀疏优化、非光滑优化** |
| 期刊分布 | **SIAM J. Optimization、Mathematical Programming、Operations Research**（运筹学三大顶刊）+ Optimization×3, Set-Valued and Variational Analysis×3 等 |
| 与申报人关系 | 博士导师，已合作2篇工作论文（在审SSCI：JASSS + Social Choice and Welfare） |

### 与课题的关联度

| 维度 | 关联度 | 说明 |
|:---|:---:|:---|
| 运筹学 | ✅✅✅ 极高 | 纯运筹学/最优化理论方向教授 |
| 交通信号优化MILP | ✅✅ 高 | 线性规划/整数规划/约束优化是专业范围 |
| ABM参数校准 | ✅ 中等 | 稀疏优化和L1正则化可用于参数选择 |
| 出行权交易机制 | ✅ 中等 | 多目标优化、变分不等式可用于市场均衡分析 |

### 与欧祖军院长对比

| 维度 | 欧祖军 | 孟开文 |
|:---|:---|:---|
| 研究方向 | 试验设计/统计学 | **运筹学/最优化** |
| 最高引用 | 26次 | **186次** |
| 顶刊论文 | 0篇 | **3篇**（SIAM/Math Programming/Operations Research） |
| 与课题关联度 | 低（统计方向） | **高**（信号优化MILP直接对口） |
| 与申报人关系 | 院长（行政关系） | **博士导师**（学术血缘） |
| 申报书角色 | 统计设计/学院支持 | **运筹学理论支撑/最优化方法指导** |

## 四、多合作者互补策略（⭐ 本案例核心洞察）

### 策略：两个合作者互补，化解"学科跨越"风险

| 合作者 | 角色 | 补的短板 |
|:---|:---|:---|
| 欧祖军（院长，本校） | 统计设计+参数校准+学院支持 | 统计学短板 + 行政支持信号 |
| 孟开文（博导，外校） | 运筹学理论+最优化建模 | 运筹学短板 + 学术血缘背书 |

**效果**：两个一挂，评审专家看到的是"数学+统计+运筹学"完整团队配置，学科跨越风险的问题基本化解。

### 多合作者的可行性

- 省自科青年A类没有要求项目组成员全部来自依托单位
- 博士导师作为项目组成员是常见做法，评审专家天然认可
- 两个合作者各有明确分工（统计设计 vs 优化建模），不是"挂名不干活"

### 话术模板

> "孟老师，我在申报2027年湖南省自科青年基金，课题是用ABM仿真做城市交通拥堵治理，里面涉及绿波信号优化的混合整数规划求解和出行权交易的市场均衡分析，正好是您运筹学和变分分析的方向。想请您作为项目组成员支持一下，主要帮忙把关优化模型的理论部分。我们之前合作的论文方法论可以迁移过来。"

**关键要素**：
1. 提到具体技术问题（MILP + 市场均衡）——让导师觉得你认真准备了
2. 对应导师的实际专长（运筹学 + 变分分析）——角色定位准确
3. 提到已有合作基础（2篇在审SSCI）——不是临时拉来挂名
4. "把关理论部分"——暗示不需要他做大量工作

## 五、启示

1. **博士导师是最佳合作者**：学术血缘关系天然合理，不需要额外解释合作动机
2. **顶刊背书分量极重**：SIAM/Mathematical Programming/Operations Research三篇顶刊在省自科评审中分量极重，远超院长的中等引用
3. **多合作者互补 > 单合作者**：一个人补不了所有短板，两个互补的合作者能覆盖"统计+运筹学"两个方向
4. **外校合作者完全可行**：省自科不要求成员全部来自依托单位
5. **arXiv API 是 Scholar 的可靠降级方案**：当 Google Scholar 被反爬限制时，arXiv API 不受影响
