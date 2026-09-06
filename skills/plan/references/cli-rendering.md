# Hermes CLI 渲染陷阱

## 核心问题：stdout 与 prompt_toolkit 双通道冲突

Hermes CLI 有两套独立的渲染通道：

- **通道 A (stdout)**：Agent 的文本输出通过 `_console_print` → `ChatConsole.print()` → `_cprint()` → `print_formatted_text(ANSI(...))`
- **通道 B (prompt_toolkit)**：clarify/approval 等弹窗通过 HSplit 布局中的 `ConditionalContainer` 渲染

**同轮冲突**：Agent 在同一响应中先输出文字再调 clarify() 时，prompt_toolkit 的 `_invalidate()` 触发全屏重绘，覆盖 stdout 文本。

## 解决方案

**所有交互式内容（计划确认、表达确认）必须放入 clarify() 的 question 参数**，确保在 prompt_toolkit 通道内渲染。

```python
# 正确
clarify(question="计划\n任务：XXX\n步骤1：...\n\n确认？")

# 错误
print("计划\n任务：XXX")  # 会被覆盖
clarify(question="确认？")
```

## Markdown 剥离

`display.final_response_markdown: strip` 会删除：
- `#` `##` 标题标记
- `**` 粗体标记
- `---` 水平线（仅当整行只有 `---` 时）
- 代码块标记

不影响：纯文本、带文字的 `--- 文字 ---` 行、编号列表。

## 相关

- task-planner 技能：弹窗确认机制
- expression-polish 技能：弹窗确认机制
