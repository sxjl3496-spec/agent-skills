# 合作者评估案例：吴朝霞（硕士导师，湘潭大学）

## 背景

选题从交通方向（E12）转向碳排放权交易方向（G03经济科学）后，团队配置需要重新评估。原配置中孟开文（博导，运筹学/最优化）对碳交易方向价值有限，需要寻找方向更对口的合作者。

## 搜索方法

### 方法一：Crossref API（⭐ 2026.8.2 实测最可靠，发现基金标注）

**原理**：Crossref API 返回结构化 `funder` 字段（基金名称+编号），不受反爬限制。比Google Scholar可靠得多。

```bash
curl -s "https://api.crossref.org/works?query.author=Wu+Zhaoxia&filter=from-pub-date:2023&rows=10&select=DOI,title,author,published,funder,container-title" \
  -H "User-Agent: Mozilla/5.0"
```

**实际发现**：通过Crossref API成功提取到吴朝霞的湖南省自科基金编号：
- 23JJ30604（2023年面上项目，3年执行期，2025年底结题）
- 2022JJ50208（2022年一般项目，3年执行期，2024年底结题）

两个项目到2027年都已结题，吴朝霞可以参与新项目。

**湖南省自科基金编号解码**：`YYJJ X XXXX` -> YY=年份, JJ=基金, X=类型(3=面上/4=重点/5=一般/6=青年), 后4位=序号

### 方法二：Semantic Scholar API

```python
# 搜索作者档案
curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=Zhaoxia+Wu&fields=name,affiliations,paperCount,citationCount"
# 结果: Zhaoxia Wu, 论文数46, 总引用230
```

### 方法三：Google Scholar（走Clash代理，反爬严重）

```bash
curl -s -x http://127.0.0.1:7897 \
  "https://scholar.google.com/scholar?q=%22Z+Wu%22+%22S+Zeng%22+emission+OR+green+OR+carbon" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

**注意**：Google Scholar对中文作者搜索反爬严重，经常返回CSS重定向而非结果。Crossref API更可靠，但只覆盖有DOI的论文。三者需要互补使用。

**推荐搜索顺序**：Crossref API（基金标注）-> Semantic Scholar API（论文档案）-> Google Scholar（中文论文补充）

## 吴朝霞学术档案

| 维度 | 信息 |
|:---|:---|
| 姓名 | 吴朝霞 (Zhaoxia Wu) |
| 机构 | 湘潭大学 |
| Semantic Scholar论文数 | 46篇 |
| 总引用 | 230次 |
| 研究方向 | **绿色金融、碳排放权交易、ESG、环境经济** |
| 最新SSCI | 2026年Sustainability（ESG方向，引用17） |
| CSSCI | 经济地理2023（绿色金融，引用7） |
| 与少帅合作论文 | 排污权交易PSM-DID（产业经济评论CSSCI，2021） |

## 关键发现

### 1. 研究方向完全对口

| G03子方向 | 吴朝霞的论文 | 对口程度 |
|:---|:---|:---:|
| 资源与环境经济 | 排污权交易（产业经济评论CSSCI） | ⭐⭐⭐⭐⭐ |
| 资源与环境经济 | 绿色金融促进污染控制（经济地理CSSCI） | ⭐⭐⭐⭐⭐ |
| 金融经济 | ESG治理（Sustainability SSCI） | ⭐⭐⭐⭐ |
| 碳排放交易 | 中国碳排放交易思考（低碳经济2018） | ⭐⭐⭐⭐⭐ |

### 2. 与少帅已有合作论文

> 吴朝霞, **冯泽宇**（通讯作者）. 排污权交易政策对不同规模企业的影响研究--基于PSM-DID方法的研究. *产业经济评论*, 2021(01): 119-136. 【CSSCI】

这篇论文直接证明了两人在排污权交易方向有实质性合作产出，不是挂空名。

### 3. 硕士导师 vs 博士导师的选择

| 对比 | 吴朝霞（硕导，湘潭大学） | 孟开文（博导，西财） |
|:---|:---|:---|
| 对碳交易方向对口度 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 和少帅合作论文 | 有（排污权交易CSSCI） | 有（在审JASSS） |
| 学术级别 | 副教授/教授，46篇论文 | 教授/博导，SIAM顶刊 |
| 论文期刊分布 | 经济地理CSSCI+Sustainability SSCI | SIAM/Mathematical Programming |
| 对G03方向价值 | 完全对口（环境经济+绿色金融） | 沾边（运筹学是工具方法） |

## 最终团队配置

| 角色 | 人 | 单位 | 作用 |
|:---|:---|:---|:---|
| 负责人 | 冯泽宇 | 吉首大学 | ABM仿真+计量 |
| 合作导师 | **吴朝霞** | 湘潭大学 | **碳排放权交易方向背书+环境经济学指导** |
| 统计设计 | 欧祖军 | 吉首大学（院长） | ABM参数校准的实验设计+学院依托 |

## 教训

1. **选题方向变更后必须重新评估合作者**：交通方向选孟开文（MILP信号优化），碳交易方向选吴朝霞（环境经济），不能一个合作者打天下
2. **硕士导师可能比博士导师更对口**：博导级别高但方向不对口时，硕导级别够用+方向完全对口是更优选择
3. **已有合作论文是最强背书**：和吴朝霞的排污权交易CSSCI论文直接证明了合作产出能力
4. **合作者搜索要跨平台**：Semantic Scholar（英文论文）+ Google Scholar（中文论文）+ CNKI（中文论文补充），单一平台覆盖不全
