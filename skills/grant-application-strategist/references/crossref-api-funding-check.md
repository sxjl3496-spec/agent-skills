# Crossref API 排查合作者在研基金

## 场景

需要确认合作者名下是否有在研省级自然科学基金项目（判断限项影响），但Google Scholar反爬严重，Semantic Scholar不返回funding信息。

## 方法：Crossref API 查询论文基金标注

Crossref API 返回论文的结构化 `funder` 字段，包含基金名称和编号，不受反爬限制。

### 搜索命令

```bash
curl -s "https://api.crossref.org/works?query.author=Zhaoxia+Wu&filter=from-pub-date:2023&rows=10&select=DOI,title,author,published,funder,container-title"
```

### Python 解析示例

```python
import requests, json

resp = requests.get(
    "https://api.crossref.org/works",
    params={
        "query.author": "Wu Zhaoxia",
        "filter": "from-pub-date:2023",
        "rows": "10",
        "select": "DOI,title,author,published,funder,container-title"
    },
    timeout=15
)
data = resp.json()
for item in data.get("message", {}).get("items", []):
    title = item.get("title", [""])[0]
    funding = item.get("funder", [])
    if funding:
        for f in funding:
            print(f"基金: {f.get('name', '')} | 编号: {f.get('award', [])}")
```

### 湖南省自科基金编号解码

格式：`YYJJ X XXXX`

| 编号段 | 含义 |
|:---|:---|
| YY | 立项年份（如23=2023年） |
| JJ | 基金（湖南省自科） |
| X（第3位） | 类型：3=面上/4=重点/5=一般/6=青年 |
| XXXX | 序号 |

**示例**：`23JJ30604`
- 23 = 2023年立项
- JJ = 湖南省自科基金
- 3 = 面上项目
- 0604 = 序号
- 面上项目执行期3年（2023.1-2025.12），到2027年已结题

### 注意事项

1. **同名作者问题**：Crossref搜索"Wu Zhaoxia"可能返回食品科学、化学等同名作者的论文。需通过论文标题和期刊名称交叉确认是否是目标合作者。
2. **funder字段不一定有**：部分论文的Crossref元数据中没有funder信息，不代表该论文没有基金资助。
3. **编号格式各省不同**：此解码规则仅适用于湖南省自科基金，国自然编号格式不同（如11871015）。
4. **API无需认证**：Crossref API是公开的，不需要API key，但有速率限制（每秒约50次）。

## 本案例实测结果（2026.8.2）

吴朝霞老师通过Crossref API确认的基金：

| 基金 | 编号 | 类型 | 立项年份 | 执行期 | 2027年状态 |
|:---|:---|:---:|:---:|:---|:---:|
| 湖南省自科基金 | 23JJ30604 | 面上 | 2023 | 2023-2025 | 已结题 |
| 湖南省自科基金 | 2022JJ50208 | 一般 | 2022 | 2022-2024 | 已结题 |
| 湖南省教育厅 | 20B527 | - | 2020 | 3年 | 已结题 |

**结论**：吴朝霞老师2027年可以参与新项目，名下项目均已结题。
