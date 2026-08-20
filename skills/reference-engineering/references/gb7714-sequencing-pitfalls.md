# GB/T 7714 顺序编码重排 · Python 陷阱详解

> 来源：2026-08-14 省自科申报书文献战役实测（V2→V3→V7 多轮重排踩坑记录）

## 背景

申报书文献综述升级时，正文引用编号必须按"首次出现顺序"重新编号（GB/T 7714 顺序编码制）。人工重排不可行（50+条），必须脚本化。以下陷阱均在实际执行中踩到并修复。

## 陷阱1：int/str 键不匹配 → 表被整体覆盖丢失 ⭐⭐⭐

**现象**：重排脚本输出"表条目: 11 条"——旧表 44 条全部消失，只剩新增的 E1-E11。

**根因**：
```python
entries = {}                      # 表条目：键是 int（正则 \d+ 转 int）
for line in ref_lines:
    m = re.match(r'^\[(\d+)\]\s*(.*)$', line)
    entries[int(m.group(1))] = m.group(2)   # ← int 键

old_to_new = {}                   # 正文映射：键是 str（re.findall 捕获组）
for c in re.findall(r'\[(E?\d+)\]', body):
    old_to_new[c] = next_n        # ← str 键
    next_n += 1

# 致命行：
new_entries = [(old_to_new[k], e) for k, e in entries.items() if k in old_to_new]
# int 键 44 不在 str 键 dict 里 → 全部被判"未引用" → 表只剩 E 条目
```

**修复**：表条目键统一用 str：
```python
entries[m.group(1)] = m.group(2).strip()   # 不转 int
```

**教训**：重排脚本写完后先打印 `len(entries)` 和 `len(old_to_new)` 对比，相等才继续；任何"未引用条目"警告都要先核实是真实未引用还是键类型问题。

## 陷阱2：表覆盖丢失后无法恢复 ⭐⭐⭐

**现象**：陷阱1执行后，写回文件时用 `new_entries`（只剩11条）覆盖了整个参考文献表。旧44条永久丢失（除非有源文件）。

**根因**：重排脚本"解析旧表 → 过滤 → 写回"是破坏性操作，中间任何 bug 都会丢数据。

**修复原则**：
1. **永远从源文件（V2综述）一次性重建**，不要从"已被部分修改的中间文件"继续
2. 重排 = 读源 → 生成新文件，绝不 in-place 覆盖
3. 验证通过（唯一引用数==表条目数）后才写盘
4. 中间版本保留（V2/V3 都留档），方便回溯

## 陷阱3：锚点编号漂移 ⭐⭐

**现象**：在 V2 基础上插入新文献时，锚点字符串带编号（如"孙晓华等（2024）[11]..."）匹配失败——因为 V2 正文里该文献编号可能已经是 [12]（V3 第一次重排后编号变了）。

**修复**：
```python
# ❌ 锚点含编号（脆弱）
anchor = "孙晓华等（2024）[11]发现市场型环境规制..."
# ✅ 锚点用纯文本片段（稳健）
anchor = "企业优先选择末端治理而非研发投入。"
i = body.find(anchor)
body = body[:i+len(anchor)] + insert_text + body[i+len(anchor):]
```

**教训**：正文锚点一律用**不含编号**的文本片段；升级过编号的文件，插入前先 find 确认实际文本。

## 陷阱4：中文引号 SyntaxError ⭐

**现象**：execute_code 中字符串包含中文引号（"..."）报 `SyntaxError: invalid syntax`。

**根因**：编辑器/输入法把中文引号打成了 ASCII 双引号，嵌套在 Python 双引号字符串里。

**修复**：
```python
LQ, RQ = "\u201c", "\u201d"   # 中文引号
text = "这为" + LQ + "以效率差异为基础的分层定价" + RQ + "提供了锚点。"
```

**教训**：所有含引号的文案拼接，统一用 \u201c/\u201d 常量，不用字面量。

## 陷阱5：裸条目无编号前缀 → 静默丢失 ⭐

**现象**：往表里追加新文献时写成 `ref_part += "\n徐志伟,王思禹.排污权交易的产能重配效应..."`（无 `[E12] ` 前缀），正则 `^\[(E?\d+)\]` 匹配不上 → 条目在解析阶段就消失，重排后表里查无此人。

**修复**：所有表条目统一格式 `"[E12] 内容"`；追加时写完整：
```python
ref_part += f"\n[E12] 徐志伟,王思禹.排污权交易的产能重配效应[J].财经研究,2025,51(12):18-31."
```

**教训**：表条目追加后用 `"徐志伟" in ref_part` 验证落盘。

## 陷阱6：pandoc 自动编号（非 bug，认知陷阱）

**现象**：md 的 `1. MONTGOMERY...` 转 docx 后，python-docx 读段落 text 无编号前缀——以为编号丢失。

**真相**：pandoc 把 `1. xxx` 识别为有序列表 → Word 自动编号（numPr）→ 打开 Word 可见 1-48。python-docx 读不到 numPr 渲染的编号属正常。

**验证方法**：检查段落 XML 是否含 `w:numPr`：
```python
numPr = p._p.find(qn('w:pPr'))
has_num = numPr is not None and numPr.find(qn('w:numPr')) is not None
```

## 验证脚本模板

```python
import re
cites = re.findall(r'\[(\d+)\]', body)
uniq = []
for c in cites:
    if c not in uniq: uniq.append(c)
ordered = uniq == sorted(uniq, key=int)                    # 按序递增
continuous = [n for n,_ in entries] == list(range(1, len(entries)+1))  # 连续
n_25 = sum(1 for n,e in entries if re.search(r'[（(]?(202[56])[）)]?[,，]|, 202[56]', e))  # 近两年
print(f"引用{len(uniq)} 顺序:{ordered} | 表{len(entries)} 连续:{continuous} | 2025/26:{n_25}")
```
