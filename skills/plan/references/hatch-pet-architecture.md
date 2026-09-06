# Hatch Pet 架构分析

## 来源

OpenAI 官方 Codex Skills 仓库：`github.com/openai/skills`，路径 `skills/.curated/hatch-pet/`。

获取方式（GitHub sparse checkout，适用于大型仓库只需特定目录）：
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/openai/skills.git openai-skills
cd openai-skills
git sparse-checkout set skills/.curated/hatch-pet
```

## Hatch Pet 是什么

Codex 的官方 curated skill，把一张参考图（或文字描述）变成 Codex 可用的动画桌面宠物。核心是一套自动化流水线：生成主形象 -> 生成9组动作帧 -> 逐帧质检 -> 拼合精灵图集 -> 打包安装。

## 文件结构

```
hatch-pet/
├── SKILL.md                          # 539行，工作流编排（Codex agent 读的指令）
├── LICENSE.txt
├── agents/openai.yaml                # Codex 界面注册（display_name + default_prompt）
├── references/
│   ├── animation-rows.md             # 9行动画的状态/帧数/时长定义
│   ├── codex-pet-contract.md         # 精灵图集格式规范
│   └── qa-rubric.md                  # 质检评分标准
└── scripts/
    ├── prepare_pet_run.py            # 830行，创建运行目录/提示词/任务清单/布局参考图/选色键
    ├── extract_strip_frames.py       # 把横向条状图切割成 192x208 单帧
    ├── derive_running_left_from_running_right.py  # 镜像翻转 running-right 得到 running-left
    ├── inspect_frames.py             # 检查每帧质量（透明度/边缘/尺寸异常）
    ├── compose_atlas.py              # 把57帧拼成 1536x1872 精灵图集
    ├── validate_atlas.py             # 验证图集尺寸/透明通道/空白格子
    ├── make_contact_sheet.py         # 生成一张总览图供质检
    └── render_animation_previews.py  # 每行生成一个GIF预览动画
```

## 精灵图集格式（Codex Pet Contract）

- 尺寸：1536 x 1872 像素
- 网格：8列 x 9行
- 单格：192 x 208 像素
- 背景：透明
- 未使用的格子：完全透明（RGB 残留必须为零）

## 9行动画状态

| 行 | 状态 | 帧数 | 用途 |
|----|------|------|------|
| 0 | idle | 6 | 待机：呼吸/眨眼循环 |
| 1 | running-right | 8 | 向右移动 |
| 2 | running-left | 8 | 向左移动（可从 running-right 镜像派生） |
| 3 | waving | 4 | 挥手致意 |
| 4 | jumping | 5 | 跳跃 |
| 5 | failed | 8 | 失败/沮丧反应 |
| 6 | waiting | 6 | 等待用户输入 |
| 7 | running | 6 | 活跃工作中（不是跑步，是"运行任务"状态） |
| 8 | review | 6 | 检查/审查 |

共 57 帧，分布在 72 格中（8x9），空格透明。

## 核心技术：色键背景去除

不依赖 AI 直接生成透明背景，而是用确定性的色键技术：

1. `prepare_pet_run.py` 分析参考图的颜色分布，从候选色（品红/青色/黄色/蓝色/橙色/绿色）中自动选择与角色颜色距离最大的一个作为色键
2. 生成提示词中要求 AI 把角色放在"纯色 {色键名} {hex} 背景"上
3. `extract_strip_frames.py` 用 PIL 按色键颜色做背景去除（类似绿幕抠像）
4. `validate_atlas.py` 验证透明像素没有 RGB 残留

## 工作流

```
输入：参考图 / 文字描述 / 品牌名
  │
  ├─ (品牌名) -> 品牌 discovery 子agent -> 品牌简报
  │
  v
prepare_pet_run.py
  -> 创建 run/ 目录
  -> 自动选色键
  -> 生成9个布局参考图（references/layout-guides/）
  -> 生成提示词文件（prompts/base-pet.md + prompts/rows/*.md）
  -> 生成任务清单（imagegen-jobs.json）
  |
  v
生成主形象(base)
  -> $imagegen 生成一张角色定稿图
  -> 复制到 references/canonical-base.png 作为后续所有帧的身份参考
  |
  v
生成9行动画条（并行，每行一个轻量子agent）
  -> 每个子agent 收到：提示词 + 主形象参考 + 布局参考图
  -> 返回 selected_source 路径 + 一句话 QA note
  -> running-left 可从 running-right 镜像派生（需人工确认）
  |
  v
确定性图片处理（7个 Python 脚本，纯 PIL，无 AI）
  -> extract_strip_frames: 切割成单帧
  -> inspect_frames: 质量检查
  -> compose_atlas: 拼合图集
  -> validate_atlas: 验证格式
  -> make_contact_sheet: 生成总览图
  -> render_animation_previews: 生成 GIF 预览
  |
  v
视觉 QA（轻量子agent 看总览图+GIF）
  -> 检查角色一致性/动作合理性/背景干净度
  -> 不合格行 -> 重新生成该行
  |
  v
打包
  -> pet.json + spritesheet.webp
  -> 安装到 ~/.codex/pets/<pet-name>/
```

## 提示词设计要点

- **主形象提示词**：要求"单一居中全身姿态，纯色色键背景，紧凑可读，192x208 内清晰，无场景/文字/阴影/发光"
- **每行提示词**：包含身份锁定（与主形象一致）、状态动作描述、状态特定要求（如 idle 不允许挥手/走路）、动画连续性（表观尺寸稳定）、清洁提取规则
- **样式预设**：auto/pixel/plush/clay/sticker/flat-vector/3d-toy/painterly/brand-inspired
- **效果限制**：禁止速度线/灰尘/阴影/发光/运动模糊等脱离角色的装饰效果

## 适配 Hermes 的可行性分析

### 可直接复用（零修改）

7个 Python 脚本全部是纯 Python + Pillow，不依赖 Codex 任何东西：
- prepare_pet_run.py（830行，最复杂，负责整个运行目录初始化）
- extract_strip_frames.py（条状图切割）
- derive_running_left_from_running_right.py（镜像派生）
- inspect_frames.py（帧质量检查）
- compose_atlas.py（图集拼合）
- validate_atlas.py（图集验证）
- make_contact_sheet.py（总览图生成）
- render_animation_previews.py（GIF 预览）

### 需要适配

1. **生成层**：`$imagegen` -> Hermes 的 `image_gen` 工具。不确定点：image_gen 后端模型是否支持色键背景和多帧一致性
2. **编排层**：SKILL.md 从 Codex agent 指令格式改为 Hermes skill 格式
3. **质检层**：Codex 的"轻量子agent" -> Hermes 的 `vision_analyze` 或 `delegate_task`
4. **背景去除**：如果 image_gen 不支持指定背景色，可用 `rembg` 库（AI抠图）替代色键技术

### Hermes 的优势

1. `vision_analyze` 可直接看图做角色一致性检查，比 Codex 的"worker返回一句话"更直接
2. 可反复生成-检查-重新生成，循环比 Codex 更灵活
3. 可接入用户现有 API（豆包/千问生图），不依赖单一模型

### Hermes 的劣势

1. 图片生成质量取决于 image_gen 后端模型
2. 多帧一致性是硬伤（OpenAI 的 DALL-E 有专门优化）
3. 没有自动质检标准（需人工定义检查维度）

## 打包格式

```json
// pet.json
{
  "id": "pet-name",
  "displayName": "Pet Name",
  "description": "One short sentence.",
  "spritesheetPath": "spritesheet.webp"
}
```

文件放置：`~/.codex/pets/<pet-name>/pet.json` + `spritesheet.webp`

注：此格式是 Codex 专用。如果目标是 DyberPet，需要 DyberPet 的角色包格式（JSON 配置 + 图片帧目录），不是 Codex 的精灵图集格式。
