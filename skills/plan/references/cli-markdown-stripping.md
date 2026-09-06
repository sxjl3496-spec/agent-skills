# Hermes CLI 输出渲染陷阱

> 发现日期：2026-07-23 | 影响技能：task-planner, expression-polish

## 问题

Agent 在 CLI 中输出 markdown 格式文本时，用户看不到内容。

## 根因

Hermes CLI 配置 `final_response_markdown: strip`（当前值），会调用 `_strip_markdown_syntax()` 删除以下 markdown 标记：

- `---` → 被视为水平线，整行删除
- `##` 或 `#` 开头的行 → 被视为标题，`#` 号删除
- `**bold**` → `**` 删除，仅保留文字
- `` `code` `` → 反引号删除
- ```` ```代码块``` ```` → 整个标记删除

普通文本不受影响，但不小心用了 markdown 标记的内容会被截断。

## 对比

| 渲染路径 | markdown处理 | 用户可见 |
|----------|:--:|:--:|
| Agent 普通输出 | `_strip_markdown_syntax()` | 标记被删除 |
| `clarify()` 弹窗 | 无（Rich TUI 直接渲染） | 完整保留 |

## 解决方案

**所有需要用户确认的内容（计划、优化后的文本）必须放在 `clarify()` 的 `question` 参数中。**

```python
# 正确：内容在弹窗内，不被 strip
clarify(question="计划：\n步骤1：... → DeepSeek\n...\n\n少帅，是否可行？")

# 错误：内容在弹窗外，被 strip 吃掉
输出("--- 计划 ---")  # → 整行被删除
clarify(question="确认吗？")
```

## 注意事项

- `clarify()` 弹窗内可以安全使用 markdown（不会被 strip）
- 非 clarify 输出避免使用 `---`、`##`、`**` 等标记
- 此行为依赖 `final_response_markdown: strip` 配置，改动需重启
