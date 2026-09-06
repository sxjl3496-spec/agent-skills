# CLI 渲染陷阱：计划文字为什么被吞掉

## 根因

Hermes CLI 中，Agent 文本输出和 clarify 弹窗共用 prompt_toolkit 渲染。在同一轮 Agent 响应中，先通过 `_cprint` 输出文本，再调用 `clarify()` 时，prompt_toolkit 的 `_invalidate()` 全屏重绘会覆盖尚未完成渲染的 stdout 文本。

## 错误做法

❌ 同轮输出计划文字 + 调 clarify 弹窗 → 用户只看到弹窗，看不到计划

## 正确做法

✅ 纯文字输出计划 + 末尾附带数字选项（不调 clarify）：
```
---计划---
任务：XXX
步骤1：...
1. 确认
2. 调整
3. 取消
回复数字选择。
```

## 格式规范

- 禁止 markdown 表格（CLI strip 模式会剥离 `|` 管道符）
- 禁止 `##` 标题和 `---` 分隔线（被 strip 引擎删除）
- 选项用数字编号，方便快速选择
- 多审批项底部汇总为 `[A][B]`，回复格式 `1 A B`
