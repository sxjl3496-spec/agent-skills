# 全感官模型路由策略矩阵（Coding Plan优先）

> 更新日期: 2026-08-04
> 策略: Coding Plan包月（主力） -> DashScope免费千问（备用） -> MiniMax多模态（视觉/视频主力） -> 按量付费（DeepSeek兜底）

## 核心原则

1. **Coding Plan优先，质量优先**：火山方舟Coding Plan已续费，包月模型零边际成本。优先使用，且在Coding Plan内选择能力最强的模型保证交付质量，不必为省tokens而降级
2. **免费千问备用**：Coding Plan触发429限流时，降级到DashScope免费千问模型（11个×100万token），用完免费额度后启用付费
3. **MiniMax多模态补位**：Coding Plan和DashScope缺少的能力（视频生成、图片识别降级），由MiniMax按量付费补位。MiniMax-H3视频生成（768P/2K，4-15秒），MiniMax-M3图片理解（1M上下文多模态）
4. **付费DeepSeek兜底**：以上层均不可用时，按量付费优先选DeepSeek（价格低于Moonshot）

## 三层优先级架构

```
Tier 1: Coding Plan包月 (9个模型，零边际成本，质量优先)
Tier 2: DashScope免费千问 (11个 × 100万token ≈ 1100万免费)
Tier 3: 按量付费API (MiniMax多模态 + DeepSeek优先 -> Moonshot兜底)
```

## Coding Plan 模型清单（火山方舟，2026.7续费）

| 模型 | 能力定位 | 适用复杂度 | 注意 |
|------|---------|-----------|------|
| glm-5.2 | 旗舰通用 | M级标准任务 | 默认thinking，需关闭 |
| deepseek-v4-pro | 深度推理 | H级复杂任务 | 默认thinking，需关闭 |
| kimi-k2.7-code | 编程优化 | 代码生成/审查 | - |
| minimax-m2.7 | 推理增强 | 需推理的M/H级 | - |
| minimax-m3 | 通用均衡 | 各类通用任务 | - |
| kimi-k2.6 | 视觉理解 | 图片分析/OCR | 默认thinking，需关闭 |
| doubao-seed-2.1-turbo | 视觉备用 | 视觉任务兜底 | - |
| doubao-seed-2.0-lite | 超轻量 | L级简单任务 | 零成本 |
| deepseek-v4-flash | 轻量对话 | L级快速响应 | - |

**选型原则**：
- Coding Plan内选能力最强的模型（质量优先），而非最省的
- L级任务用doubao-seed-2.0-lite，把主模型额度留给复杂任务
- 需thinking的模型（glm-5.2, deepseek-v4-pro, kimi-k2.6）已在config.yaml中关闭thinking

## 当前免费千问模型清单（DashScope 薅羊毛池）

| 模型 | 到期日 | 剩余token | 使用优先级 | 说明 |
|------|--------|----------|----------|------|
| qwen3.7-max | 2026/08/20 | 1,000,000 | 1(主力) | 最强+最急，先用 |
| qwen3.7-max-2026-05-20 | 2026/08/20 | 1,000,000 | 2 | 同名备份 |
| qwen3.7-max-preview | 2026/08/24 | 1,000,000 | 3 | 预览版 |
| qwen3.7-max-2026-05-17 | 2026/08/24 | 1,000,000 | 4 | 同名备份 |
| qwen3.7-plus | 2026/09/01 | 1,000,000 | 5 | 中端 |
| qwen3.7-plus-2026-05-26 | 2026/09/01 | 1,000,000 | 6 | 同名备份 |
| qwen3.7-max-2026-06-08 | 2026/09/08 | ~999,908 | 7 | 已用92tok |
| kimi-k2.7-code | 2026/09/14 | 1,000,000 | 8 | 编程优化 |
| glm-5.2 | 2026/09/15 | 1,000,000 | 9 | 通用旗舰 |
| qwen3.7-flash-2026-07-15 | 2026/10/23 | 1,000,000 | 10 | 轻量 |
| qwen3.7-flash | 永不过期 | 1,000,000 | 11(兜底) | 最后防线 |

## 文本模型路由

### 复杂度分级标准

| 等级 | 预估token | 推理深度 | 创造性 | 上下文依赖 |
|------|----------|---------|--------|-----------|
| L | <2K | 单步 | 格式转换 | 无状态 |
| M | 2K-8K | 多步工具 | 结构化输出 | 需前序输出 |
| H | >8K | 深度推理 | 原创内容 | 需全局上下文 |
| H+ | >16K | 跨域综合 | 架构设计 | 复杂依赖 |

### 三层路由表

| 复杂度 | ① Coding Plan主力（火山方舟） | ② 免费千问备用（DashScope） | ③ 按量付费 |
|--------|-----------------------------|--------------------------|-----------|
| L | doubao-seed-2.0-lite | qwen3.7-flash (100万token) | deepseek-v4-flash (1元/百万T) |
| M | glm-5.2 | qwen3.7-max (100万token) | deepseek-v4-flash (1元/百万T) |
| H | deepseek-v4-pro | qwen3.7-max (100万token) | kimi-k2.6 (moonshot) |
| H+ | kimi-k3 [需审批] | kimi-k3 [需审批] | kimi-k3 [需审批] |

### fallback降级链（完整链路）

```
===== Tier 1: Coding Plan =====
doubao-seed-2.0-lite (volcano/Coding, L级)
  ↓ 或
glm-5.2 (volcano/Coding, M级)
  ↓ 或
deepseek-v4-pro (volcano/Coding, H级)
  ↓ 429 限流
===== Tier 2: DashScope 免费千问 =====
qwen3.7-max (dashscope, 免费, 08/20到期)
  ↓ 429/配额用完
qwen3.7-max-2026-05-20 (dashscope, 免费, 08/20)
  ↓ 429
qwen3.7-max-preview (dashscope, 免费, 08/24)
  ↓ 429
qwen3.7-max-2026-05-17 (dashscope, 免费, 08/24)
  ↓ 429
qwen3.7-plus (dashscope, 免费, 09/01)
  ↓ 429
qwen3.7-plus-2026-05-26 (dashscope, 免费, 09/01)
  ↓ 429
qwen3.7-max-2026-06-08 (dashscope, 免费, 09/08)
  ↓ 429
kimi-k2.7-code (dashscope, 免费, 09/14)
  ↓ 429
glm-5.2 (dashscope, 免费, 09/15)
  ↓ 429
qwen3.7-flash-2026-07-15 (dashscope, 免费, 10/23)
  ↓ 429
qwen3.7-flash (dashscope, 免费, 永不过期)
  ↓ 429
===== Tier 3: 按量付费 =====
deepseek-v4-flash (deepseek直连, 1元/百万T)
  ↓ 429
kimi-k2.6 (moonshot直连)
```

## 视觉模型路由

| 优先级 | 模型 | 来源 | 费用 | 说明 |
|--------|------|------|------|------|
| 1 | kimi-k2.6 | Coding Plan (volcano) | 免费 | Coding Plan 主力视觉 |
| 2 | kimi-k2.6 | moonshot 直连 | 按量 | 通道降级 |
| 3 | MiniMax-M3 | minimax 直连 | 按量 | 多模态图片理解，1M上下文 |
| 4 | qwen3.5-omni-plus | dashscope | 按量 | DashScope 视觉备用 |
| 5 | doubao-seed-2.1-turbo | Coding Plan (volcano) | 免费 | Coding Plan 视觉兜底 |

## TTS/STT/画图/视频（Coding Plan 无对应模型，保留 DashScope/MiniMax/本地配置）

| 感官 | Coding Plan是否对应 | 主模型 | 来源 | 费用 | 降级 |
|------|---------------------|--------|------|------|------|
| TTS | ❌ 无 | SAPI Huihui (本地) | 本地 | 免费 | cosyvoice-v3.5-flash |
| STT | ❌ 无 | faster-whisper small (本地) | 本地 | 免费 | paraformer-v2 |
| 画图文生图 | ❌ 无 | qwen-image-3.0-pro (dashscope) | dashscope | 限时免费 | image-01 (minimax, 按量) |
| 画图图生图 | ❌ 无 | qwen-image-edit-plus (dashscope) | dashscope | 0.2元/张 | wanx2.1-imageedit |
| 视频文生视频 | ❌ 无 | wanx2.1-t2v-turbo (dashscope) | dashscope | 0.24元/秒 | MiniMax-H3 (minimax, 按量) |
| 视频图生视频 | ❌ 无 | wanx2.1-i2v-turbo (dashscope) | dashscope | 0.24元/秒 | MiniMax-H3 (minimax, 按量) |
| 图片识别 | ✅ kimi-k2.6 (volcano) | kimi-k2.6 | volcano | 免费 | MiniMax-M3 (minimax, 按量) -> qwen3.5-omni-plus (dashscope) |

## 模型API调用注意事项（踩坑记录）

### kimi-k3 (Moonshot 直连)
- **temperature必须设为1**：0.6和0.7都会返回HTTP 400 `invalid temperature: only 1 is allowed for this model`（2026.7.30实测）。错误信息会先说"only 0.6 is allowed"，改0.6后又说"only 1 is allowed"，最终temperature=1才成功。
- 调用超时设>=300秒（深度分析约5分钟）
- max_tokens建议>=8000（kimi-k3默认输出含reasoning_tokens）
- thinking参数设`{"type": "disabled"}`可关闭推理模式（但temperature仍必须为1）
- API Key从`~/AppData/Local/hermes/.env`的`MOONSHOT_API_KEY`读取

### DashScope qwen-image 系列
- qwen-image-2.0-pro: 端点是 `compatible-mode/v1/chat/completions`（不是 images/generations）
- 返回格式：`message.content` 是 list，图片URL在 `{"image": "url"}` 字段（不是 `image_url`）
- 超时设>=300秒，生成约70秒/张
- qwen-image-edit-plus / wan2.7-image-pro: 用 `multimodal-generation` 端点，必须同步模式（不加 X-DashScope-Async header）
- 图文必须分两个content对象：`[{"image": url}, {"text": "指令"}]`，合并到一个对象会返回400

### Coding Plan (火山方舟)
- config.yaml 中 api_key 引用变量名必须是 `${ARK_API_KEY}`（不是 `${VOLCANO_API_KEY}`）
- .env 文件中变量名为 `ARK_API_KEY`
- 变量名不匹配时不会报错，但API请求会带空key导致401静默降级
- 排查方法：`echo ${变量名:+set}` 检查变量是否存在

### MiniMax (按量付费)
- 环境变量名: `MINIMAX_API_KEY`，base_url: `https://api.minimaxi.com/v1`（OpenAI兼容端点，Hermes用这个）
- Anthropic兼容端点: `https://api.minimaxi.com/anthropic`（直接调API时可用，但Hermes gateway用OpenAI SDK走/v1）
- **MiniMax-M3 图片理解**: content数组传 `{"type":"image","source":{"type":"url","url":"..."}}`，支持thinking参数 `{"type":"adaptive"}`
- **MiniMax-H3 视频生成**: 异步接口，POST `/v2/video_generation` 创建任务，GET `/v2/query/video_generation/{task_id}` 轮询状态，成功后取 `content.url`
- **视频生成参数**: 纯文生视频必须指定 `ratio`（16:9/4:3/1:1/3:4/9:16/21:9），`duration` 4-15秒，`resolution` 768P或2K
- **图片生成**: POST `/v1/image_generation`，model=`image-01`，同步返回 `data.image_urls[0]`
- 语音合成: POST `/v1/t2a_v2`，model=`speech-2.8-hd`/`speech-2.8-turbo`，支持mp3/pcm/flac/wav

## plan技能实现方式

Hermes单agent运行时模型由config.yaml的`model.default`决定。当前配置：
- 主模型: glm-5.2 (volcano/Coding Plan)
- 子agent: deepseek-v4-flash (volcano/Coding Plan, 经delegation.model配置)
- fallback: Coding Plan备用 → 11个DashScope免费模型 → 按量付费(deepseek/moonshot)

| 复杂度 | 实现方式 | 主选模型 | 费用 |
|--------|---------|---------|------|
| L | execute_code + API | doubao-seed-2.0-lite (Coding Plan) | 零成本 |
| M | 主agent | glm-5.2 (Coding Plan) | 零成本 |
| M(并行) | delegate_task | deepseek-v4-flash (Coding Plan) | 零成本 |
| H | delegate_task | deepseek-v4-pro (Coding Plan) | 零成本 |
| H+ | delegate_task [需审批] | kimi-k3 (moonshot) | 按量付费 |
