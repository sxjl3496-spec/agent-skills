# 合作者在研项目排查方法

> 来源：2026年8月2日会话
> 场景：需确认欧祖军院长是否还有省自科在研项目，能否参与新申报

## 一、问题

限项规定要求"作为申请人申请和作为负责人正在主持的项目总数合计限为1项"。如果合作者（作为参与者）有在研项目，虽不直接触发限项（限项主要约束申请人），但合作者自己如果有在研省自科项目，可能影响其参与意愿，也可能被评审专家认为"团队重叠"。

更关键的是：如果合作者自己还想申请项目，就需要确认他是否有申请名额。

## 二、排查方法：论文基金标注提取（⭐ 核心技巧）

### 原理

中国学者发表论文时，通常在致谢中标注基金项目编号。通过搜索Google Scholar中该学者论文的摘要（gs_rs字段），可以提取到funding信息。

### 具体操作

```bash
# Google Scholar搜索该学者的论文
curl -s -x http://127.0.0.1:7897 \
  "https://scholar.google.com/scholar?q=author:%22Zujun+Ou%22+funding+OR+supported+OR+NSFC&hl=zh-CN" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

```python
# 提取论文摘要中的基金标注
import re
gs_rs = re.findall(r'<div class="gs_rs">(.*?)</div>', html, re.DOTALL)
for snippet in gs_rs:
    clean = re.sub(r'<[^>]+>', '', snippet).strip()
    if 'supported' in clean.lower() or 'funded' in clean.lower() or 'foundation' in clean.lower():
        print(f"  基金标注: {clean[:300]}")
```

### 方法一：Crossref API 提取基金标注（⭐ 2026.8.2 实测，最可靠）

**原理**：Crossref API 返回结构化的 `funder` 字段（含基金名称+编号），不依赖JS渲染，不受反爬限制，比Google Scholar的snippet提取可靠得多。

```bash
# 搜索该学者的论文，返回funding信息
curl -s "https://api.crossref.org/works?query.author=Wu+Zhaoxia&filter=from-pub-date:2023&rows=10&select=DOI,title,author,published,funder,container-title" \
  -H "User-Agent: Mozilla/5.0"
```

```python
import json
data = json.load(sys.stdin)
for item in data.get('message', {}).get('items', []):
    authors = item.get('author', [])
    author_names = [f"{a.get('given','')} {a.get('family','')}" for a in authors[:5]]
    funding = item.get('funder', [])
    if any('Zhaoxia' in name and 'Wu' in name for name in author_names):
        for f in funding:
            print(f"基金: {f.get('name','')} | 编号: {f.get('award', [])}")
```

#### 湖南省03自科基金编号格式解码

从Crossref返回的基金编号中可解码项目类型和立项年份：

| 编号格式 | 含义 | 执行期 | 示例 |
|:---|:---|:---|:---|
| YYJJ3xxxx | 面上项目（5万） | 3年 | 23JJ30604 = 2023年面上 |
| YYJJ4xxxx | 重点项目（50万） | 4年 | - |
| YYJJ5xxxx | 一般/青年项目（5万） | 3年 | 2022JJ50208 = 2022年一般 |
| YYJJ6xxxx | 青年项目 | 3年 | - |

**判断逻辑**：立项年份 + 执行期 = 结题年份。如果结题年份 < 申报年份（2027），则项目已结题，不影响参与。

**实际案例（吴朝霞）**：
- 23JJ30604（2023年面上，3年）-> 2025年底结题 -> 2027年已结题 ✅ 可参与
- 2022JJ50208（2022年一般，3年）-> 2024年底结题 -> 2027年已结题 ✅ 可参与

#### Crossref 方法优势

| 方法 | 可靠性 | 数据结构化 | 反爬风险 | 中文论文覆盖 |
|:---|:---:|:---:|:---:|:---:|
| Crossref API | ⭐⭐⭐⭐⭐ | ✅ JSON funder字段 | 无 | 低（仅有DOI的） |
| Google Scholar snippet | ⭐⭐⭐ | 需正则提取 | 高（频繁反爬） | 高 |
| Semantic Scholar API | ⭐⭐⭐⭐ | ✅ JSON | 低 | 中 |
| 直接问合作者 | ⭐⭐⭐⭐⭐ | N/A | 无 | 100% |

**推荐顺序**：Crossref API -> Semantic Scholar API -> Google Scholar -> 直接问

### 方法二：Google Scholar snippet 提取（备选）

通过搜索Google Scholar中该学者论文的摘要（gs_rs字段），提取funding信息。

```bash
curl -s -x http://127.0.0.1:7897 \
  "https://scholar.google.com/scholar?q=author:%22Zujun+Ou%22+funding+OR+supported+OR+NSFC&hl=zh-CN" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

```python
gs_rs = re.findall(r'<div class="gs_rs">(.*?)</div>', html, re.DOTALL)
for snippet in gs_rs:
    clean = re.sub(r'<[^>]+>', '', snippet).strip()
    if 'supported' in clean.lower() or 'funded' in clean.lower():
        print(f"  基金标注: {clean[:300]}")
```

### 实际发现（欧祖军案例，Google Scholar方法）

从论文摘要中提取到的基金标注：

| 论文年份 | 基金标注 | 判断 |
|:---:|:---|:---|
| 2019 | "National Natural Science Foundation of China (Grant Nos. 11561025 and 11701213), Hunan Provincial Natural Science Foundation of China" | 国自然2项+省自科 |
| 2020 | 同上 | 同上 |
| 2017 | "Grant Nos. 11271147, 11201177, 11561025" | 早期国自然 |

**推断**：
- 国自然11561025（地区基金）2011年获批，执行期4年 -> 2015年结题
- 国自然11701213（青年基金）2017年获批，执行期3年 -> 2020年结题

**结论**：到2027年，这些项目都已结题，不影响参与新项目。

### 局限性

1. **只能找到标注了基金号的论文**：有些论文不标注funding
2. **无法确认2024-2025年新申请的项目**：如果合作者最近申请了新项目，论文还没发出来，就查不到
3. **Crossref同名作者干扰**：Crossref中"Wu Zhaoxia"可能混杂食品科学等同名作者，需通过论文标题方向筛选
4. **Crossref只收录有DOI的论文**：纯中文期刊（无DOI）的论文不会出现，需Google Scholar补充

### 终极方案：直接问

网络搜索无法100%确认合作者的在研项目状态。最可靠的方法是直接问：

> "X院长，我正在准备省自科的申报，想请您作为项目组成员参与。想确认一下您目前名下还有在研的省自科项目吗？"

## 三、双保险策略（⭐ 2026.8.2 新增）

### 策略

| 项目 | 负责人 | 方向 | 你角色 |
|:---|:---|:---|:---|
| 碳排放权交易ABM仿真 | **冯泽宇** | G03经济科学 | 负责人 |
| 均匀设计ABM实验优化 | **欧祖军** | A04应用数学 | 参与者 |

### 限项检查

- 自己申请1项 + 参与合作者1项 = 合计2项 ✅（不超过2项限制）
- 只作为申请人申请1项 ✅
- 两个项目学科代码不同（G03 vs A04），不冲突

### 前提条件

1. 合作者（欧院长）愿意自己申请项目
2. 合作者没有在研项目占限项
3. 合作者的项目方向能让他的研究方向有用武之地

### 欧祖军方向的选题设计

如果让欧院长申请A04应用数学方向，选题必须让他的均匀设计/偏差下界理论有用武之地：

> **基于均匀设计的多智能体仿真实验最优设计与参数校准方法研究**

| 欧院长的角色 | 冯泽宇的角色 |
|:---|:---|
| 均匀设计理论：低偏差序列构造、偏差下界证明 | ABM仿真平台：将均匀设计嵌入参数校准流程 |
| 折叠设计：多水平参数的最优实验设计 | 反事实实验：多场景对比的因子设计验证 |

### 关键话术

> "院长，今年省自科申报，您那边还有申请名额吗？如果有的话，我想结合您的均匀设计方向和我的ABM仿真方法，一起写一个A04应用数学方向的申报书。另外我自己也想申请一个G03经济科学方向的碳交易课题，想请您也参与一下。"

## 四、教训

1. **不要假设合作者有空**：院长可能已有在研项目，必须先确认
2. **论文基金标注是排查在研项目的有效手段**：虽然不100%可靠，但能提供重要线索
3. **双保险策略需要合作者愿意申请**：不能强推，要看合作者的意愿
4. **两个项目方向要互补不冲突**：A04（数学方法）和G03（经济应用）天然互补，不冲突
