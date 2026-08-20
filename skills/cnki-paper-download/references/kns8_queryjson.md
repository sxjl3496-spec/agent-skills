# 知网KNS8 QueryJson结构参考

> 来源：从文献云镜像站浏览器真实请求破解（2026.8.6）
> 接口：`POST https://pdf.ccki.top/kns8s/brief/grid`

## QueryJson 完整结构

```json
{
  "Platform": "",
  "Resource": "CROSSDB",
  "Classid": "WD0FTY92",
  "Products": "",
  "QNode": {
    "QGroup": [{
      "Key": "Subject",
      "Title": "",
      "Logic": 0,
      "Items": [{
        "Field": "SU",
        "Value": "碳排放权交易",
        "Operator": "TOPRANK",
        "Logic": 0,
        "Title": "主题"
      }],
      "ChildItems": []
    }]
  },
  "ExScope": 1,
  "SearchType": 2,
  "Rlang": "BOTH",
  "KuaKuCode": "YSTT4HG0,LSTPFY1C,JUP3MUPD,MPMFIG1A,EMRPGLPA,WQ0UVIAA,BLZOG7CK,PWFIRAGL,NN3FJMUV,NLBO1Z6R",
  "Expands": {},
  "SearchFrom": 1
}
```

## 关键字段说明

### Resource
- 值：`"CROSSDB"`
- 说明：跨库检索模式

### Classid
- 值：`"WD0FTY92"`
- 说明：页面的classid，从页面HTML的 `<input id="classid">` 提取
- 注意：不是dbcode

### QGroup.Key
- 值：`"Subject"`（不是 `"MutiGroup"`！）
- 说明：检索分组类型

### QGroup.Logic / Item.Logic
- 值：`0`（AND）/ `1`（OR）/ `2`（NOT）
- ⚠️ **必须用数字，不是字符串！**

### Item.Operator
- 值：`"TOPRANK"`（排序相关）/ `"DEFAULT"`（默认）/ `"FUZZY"`（模糊）
- 注意：字符串，不是数字

### ExScope
- 值：`1`
- ⚠️ **必须是数字1，不是字符串"0"！**

### SearchType
- 值：`2`（简单检索）/ `1`（高级检索）/ `3`（作者检索）/ `4`（专家检索）/ `5`（句子检索）

### Rlang
- 值：`"BOTH"`（中英文）/ `"CHINESE"`（中文）/ `"FOREIGN"`（英文）

### KuaKuCode ⭐⭐⭐ 关键字段！
- 值：一串数据库编码，逗号分隔
- **缺失会导致**：`"没有指定检索分类"` 错误
- 完整值（从浏览器真实请求提取）：
  ```
  YSTT4HG0,LSTPFY1C,JUP3MUPD,MPMFIG1A,EMRPGLPA,WQ0UVIAA,BLZOG7CK,PWFIRAGL,NN3FJMUV,NLBO1Z6R
  ```

## 请求参数（完整）

### URL
```
POST https://pdf.ccki.top/kns8s/brief/grid
```

### Headers
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36
Referer: https://pdf.ccki.top/kns8s/defaultresult/index
X-Requested-With: XMLHttpRequest
Content-Type: application/x-www-form-urlencoded
```

### POST Body
```
boolSearch=true
QueryJson=<URL编码的JSON>
pageNum=1
pageSize=20
sortField=FFD
sortType=desc
dstyle=listmode
productStr=YSTT4HG0,LSTPFY1C,RMJLXHZ3,JQIRZIYA,JUP3MUPD,1UR4K4HZ,BPBAFJ5S
aside=
searchFrom=home
manageId=
subject=
language=
uniplatform=NZKPT
```

### 字段说明

| 字段 | 值 | 说明 |
|------|-----|------|
| `boolSearch` | `"true"` | 检索模式（简单/高级） |
| `QueryJson` | URL编码的JSON | 查询结构体 |
| `pageNum` | `"1"` | 页码 |
| `pageSize` | `"20"` | 每页数量（20/40/50） |
| `sortField` | `"FFD"` | 排序字段（FFD=相关度，PT=时间，CAF=被引） |
| `sortType` | `"desc"` | 排序方向（asc/desc） |
| `dstyle` | `"listmode"` | 显示模式 |
| `productStr` | 一串代码 | 产品库编码（与KuaKuCode部分重叠） |
| `searchFrom` | `"home"` | 来源 |
| `uniplatform` | `"NZKPT"` | 平台（从页面HTML提取） |

## Logic 值对照表

| 名称 | 值 | 用途 |
|------|-----|------|
| AND | 0 | 交集 |
| OR | 1 | 并集 |
| NOT | 2 | 排除 |

## OperatorType 值对照表

| 名称 | 值 | 用途 |
|------|-----|------|
| DEFAULT | 0 | 默认 |
| TOPRANK | 1 | 排序相关 |
| FUZZY | 2 | 模糊匹配 |
| GT | 3 | 大于 |
| GE | 4 | 大于等于 |
| LT | 5 | 小于 |
| LE | 6 | 小于等于 |
| BETWEEN | 7 | 区间 |
| FREQUENCY | 8 | 频次 |
| PREFIX | 9 | 前缀 |
| SUFFIX | 10 | 后缀 |
| CONTAINS | 11 | 包含 |
| NEAR | 12 | 邻近 |
| SENTENCE | 13 | 句子 |
| IS | 14 | 等于 |
| FUZZYFREQUENCY | 15 | 模糊频次 |

## API签名机制（getVV）

知网KNS8有请求签名，使用 AES-ECB 加密：

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json, time

# 从页面HTML提取
REST_TOKEN = "36c8848550a147f18be0746277febbbf"  # <input id="restApiToken">
CLIENT_ID = "36583a2e-653b-45d0-a66a-fb7762c5810e"  # <input id="restApiClientId">

def get_vv():
    """生成请求签名"""
    key = REST_TOKEN.encode("utf-8")
    data = json.dumps({"timestamp": int(time.time()*1000), "vk": CLIENT_ID})
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data.encode("utf-8"), 16))
    return encrypted.hex()
```

签名用于 `/preferences/getsearchsetting` 接口，brief/grid 接口不一定需要。

## 常见错误

### 1. "没有指定检索分类"
- 原因：缺少 `KuaKuCode` 字段
- 修复：添加完整的 `KuaKuCode` 值

### 2. "检索模型参数错误"
- 原因：`Logic`/`Operator` 用了字符串而非数字
- 修复：`"Logic": 0`（不是 `"AND"`）

### 3. "未登录"
- 原因：没有从入口页跳转
- 修复：必须经过 `入口页 → cnkipdf.php → 知网镜像` 完整链路

### 4. 返回空结果
- 原因：`Classid` 值错误或页面状态损坏
- 修复：重新刷新页面，从HTML提取正确的 `Classid`

## 参考脚本

- `scripts/cnki_search.py` - requests方案检索
- `scripts/pw_search2.py` - Playwright方案检索
- `scripts/pw_cssci_test.py` - CSSCI过滤测试
- `scripts/pw_download.py` - 批量下载（含CSSCI过滤+限速）
