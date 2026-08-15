---
name: pdf-hybrid-reader
description: 混合策略读取PDF——文字页直接提取文本，含图片页渲染为PNG后调用视觉模型识别。当用户需要读取/分析/总结PDF文件、PDF书籍、课程资料时自动触发。
---

## 触发条件

用户提供 PDF 文件路径，要求读取、分析、总结、识别内容。

## 策略：按页分流

对 PDF 逐页遍历，每页自动判断：

1. **如果页面无嵌入图片**（`page.get_images()` 为空）：
   - 使用 `page.get_text()` 直接提取文本
   - 不调用视觉模型

2. **如果页面有嵌入图片**（`page.get_images()` 非空）：
   - 使用 `fitz` 渲染整页为 PNG（dpi=200）
   - 通过 Python `urllib` 直调阿里百炼 `qwen3.5-omni-plus` 识别
   - API 配置见下方

## API 配置

```
base_url: https://llm-dbtrvrujol2qppb1.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
api_key: sk-ws-H.EDYEMLH.JHXT.MEUCIHDg2-fOiJO9BtQNyMNT5EhEBTRUNxruTZxCdz8TeB9OAiEArK63Ph278FYIiPie9J8ov7BBv0i4X-0bW-RMbkwkJ9Q
model: qwen3.5-omni-plus
```

## 执行步骤

```python
import fitz

doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    has_images = bool(page.get_images())
    if has_images:
        # 渲染整页PNG → base64 → 调qwen3.5-omni-plus
        pix = page.get_pixmap(dpi=200)
        img_b64 = base64.b64encode(pix.tobytes("png")).decode()
        # 调API...
    else:
        # 直接提取文本
        text = page.get_text()
```

## 输出格式

- 标明每页来源（页码 + 提取方式：text/image）
- 文字页直接输出文本内容
- 图片页输出视觉模型识别结果
- 最后汇总

## 注意事项

- **绝对不要使用 `vision_analyze` 工具**（与 qwen3.5-omni-plus 存在传图格式兼容问题：API 返回 200 但模型声称没有收到图片）。走 Python `urllib` 直调百炼 API 进行所有识图操作。
- 普通图片（非 PDF 页面）也需要同样的 Python 直调模式，不走 vision_analyze。
- `execute_code`（Python sandbox）中可能没有 fitz 模块，需先在 `terminal` 中用 fitz 渲染 PDF 页面为 PNG，再在 `execute_code` 中调用百炼视觉 API。
- fitz 安装：`pip install pymupdf`
- 图片页整页识别（方案A），非仅裁剪嵌入图片

## 参考文件

- `references/vision-api.md` — 视觉 API 配置、模型选择、token 消耗参考、为什么不用 vision_analyze
- `scripts/vision_api_call.py` — 可复用的 `ask_vision()` 和 `ask_vision_base64()` 函数，可直接在 execute_code 中 import

## 关键陷阱

1. **execute_code 沙箱无法 import fitz**：pip install 的包不会进入沙箱。正确的两步走：
   - 第一步：`terminal` 用 fitz 渲染 PNG 到临时目录（如 `$TEMP/pdf_p2.png`）
   - 第二步：`execute_code` 读 PNG 调视觉 API

2. **百炼模型配额**：qwen-omni-turbo / qwen-vl-max / qwen3-vl-flash 均可能报"免费额度耗尽"，需使用 `qwen3.5-omni-plus`（2026.7 实测可用）。

3. **GitHub raw 内容墙**：Python urllib 直连 GitHub raw 会 SSL 失败，用 `terminal` 的 `curl -x http://127.0.0.1:<代理端口>` 走 Clash 代理。

4. **base64 不要进 shell 命令行**：图片 base64 长达 50KB+，内联到 curl -d 会触发 "Argument list too long"。正确做法：在 Python 中内联，或用 `curl -d @tmpfile`。

5. **Windows 临时文件路径**：`/tmp/` 在 Git Bash 中可能不可写，用 `$TEMP`（指向 `C:\Users\<user>\AppData\Local\Temp`）或 Windows 原生路径。
