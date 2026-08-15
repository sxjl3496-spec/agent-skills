---
name: desktop-pet-creation
description: >
  桌面宠物制作全流程指南。当用户需要：(1) 用AI生成角色图制作桌面宠物，
  (2) 了解桌面宠物制作工具和方案选型，(3) 从照片生成动画精灵图集(sprite atlas)，
  (4) 适配OpenAI Hatch Pet技能到Hermes，(5) 配置DyberPet/Shimeji等桌宠框架时触发。
  触发词：桌面宠物、桌宠、desktop pet、Hatch Pet、sprite atlas、精灵图集、
  DyberPet、Shimeji、豆包桌宠、电脑宠物。
---

# 桌面宠物制作 (desktop-pet-creation)

## 概述

桌面宠物（Desktop Pet）在2025-2026年随AI生图技术普及而爆发。核心玩法：
用AI生成角色图（女朋友照片、宠物照片、动漫角色），做成可在桌面互动的程序。
互动包括拖拽、点击、自主走动、对话气泡、AI聊天等。

## 方案选型（6条路线，从易到难）

### 方案1：豆包客户端一键生成（最火、零代码）

- 工具：电脑版豆包客户端（非网页版/手机版）
- 流程：准备透明背景PNG -> 切换"办公任务Turbo模式" -> 开启"本地电脑"权限 -> 粘贴图片+万能指令 -> 等1-2分钟生成EXE -> 双击运行
- 互动：拖拽、点击触发动作、文字气泡、自主走动、窗口置顶、右键菜单、滚轮缩放
- 费用：免费
- 门槛：零代码，3分钟
- 平台：Windows优先（Mac可尝试）
- 关键：豆包客户端已安装时可直接使用，路径通常在 `C:\Users\<user>\AppData\Local\Doubao\Application\Doubao.exe`

万能指令模板（可直接复制）：
```
请使用我提供的角色图片，制作一个Windows桌面宠物程序。基本要求：去除图片背景，
窗口透明、无边框、始终置顶。桌宠可用鼠标左键拖动位置，点击角色时，轮流触发几种
简单互动，例如跳跃、更换表情，互动时随机显示简短、有趣的中文对话白气泡，气泡背景
不透明，不要遮挡角色。右键菜单包括：调整大小、置顶开关，退出程序，鼠标滚轮可以
调整桌宠大小，还有一个靠边吸附的效果，生成可直接双击的.exe文件。
```

### 方案2：Codex + Hatch Pet（多帧动画，效果最好）

- 工具：OpenAI Codex App + Hatch Pet Skill（OpenAI官方技能，开源）
- 流程：上传参考图 -> Hatch Pet自动生成主形象 -> 生成9组共57帧动画 -> 逐帧检查 -> 拼合精灵图集 -> 安装到Codex
- 互动：跟随Codex任务状态换动作（开始干活/忙起来/需要确认/任务失败）
- 费用：需要Codex订阅（约$20/月），消耗约60%周用量，耗时约1小时
- 门槛：低，但有订阅成本
- 源码：github.com/openai/skills，路径 skills/.curated/hatch-pet/
- 详见 `references/hatch-pet-architecture.md`

### 方案3：AI桌宠生成服务（在线一键）

- Petne（petne.cn）：上传猫狗照片，AI生成桌面宠物
- 伴生造物 PetDex Studio：AI桌宠生成平台
- Z-PET：治愈系AI桌面宠物，自定义桌宠下载
- DaDabb：AI生成专属桌面伙伴
- PicPets：AI桌宠生成
- 费用：部分免费、部分付费
- 门槛：极低，上传照片即可

### 方案4：DyberPet（开源Python框架，功能最全）

- GitHub：ChaozhongLiu/DyberPet，最新版v0.8.5
- 两种使用方式：直接下载EXE（双击即用）或源码运行（需conda+Python 3.9.18+PySide6）
- 功能：动画系统、交互系统、养成系统（好感度200级）、任务系统、商店、对话气泡、AI助手接入
- MOD生态：角色/道具/音效全可自定义，改JSON配置即可
- 费用：完全免费开源
- 门槛：EXE版零门槛，源码版需Python基础

#### DyberPet 精灵图集格式

DyberPet 使用独立帧文件而非整张 sprite sheet。每个动画状态一个子目录，内含6位零填充的编号 PNG 帧：

```
pets/<pet_name>/
├── pet_config.json      # 动画定义、时序、类型
├── icon.png             # 预览图标（第一帧 idle）
└── animations/
    ├── idle/       idle_000000.png ... idle_000005.png
    ├── run_right/  run_right_000000.png ... run_right_000007.png
    └── ...         （每个状态一个子目录）
```

pet_config.json 格式：
```json
{
  "petName": "TestCat",
  "petID": "testcat",
  "version": "1.0",
  "animations": {
    "idle": {
      "type": "loop",
      "frameCount": 6,
      "frames": ["idle_000000.png", ...],
      "frameDuration": [280, 110, 110, 140, 140, 320]
    }
  },
  "defaultAnimation": "idle",
  "scale": 1.0,
  "offsetX": 0,
  "offsetY": 0
}
```

#### Hatch Pet → DyberPet 转换

Hermes 的 hermes-hatch-pet 技能包含 convert_to_dyberpet.py 脚本，可一键将 Hatch Pet 运行目录的帧序列转换为 DyberPet 格式包：

```bash
python <hermes-hatch-pet>/scripts/convert_to_dyberpet.py --run-dir /path/to/run
```

状态名映射：idle→idle, running-right→run_right, running-left→run_left, waving→wave, jumping→jump, failed→fail, waiting→wait, running→run, review→review。前三个/后四个 loop 类型，wave/jump/fail 为 once 类型。

详见 references/dyberpet-format.md

### 方案5：Shimeji（经典老牌）

- 工具：Shimeji软件 + 透明背景PNG图片（需准备46-50帧不同动作）
- 流程：下载Shimeji -> 替换img目录中的图片帧 -> 配置动作XML
- 互动：攀爬窗口边框、拖拽、简单动画
- 费用：免费
- 门槛：需自备多帧图片，有现成角色包可用

### 方案6：Live2D Cubism Editor（专业级）

- 工具：Live2D Cubism Editor + VTube Studio等展示器
- 流程：绘制角色分层PSD -> Cubism中绑定变形器和动画 -> 导出模型 -> 展示器运行
- 互动：最自然的动画效果、可语音驱动、可面部捕捉
- 费用：Cubism Editor有免费版（PRO版付费）
- 门槛：最高，需绘画和动画制作能力

### 方案7：Python 自运行桌宠（零下载、跨平台备选）

当 DyberPet EXE 无法下载（GitHub 被墙）或不想安装额外框架时，用 Python + tkinter + win32 API 直接创建透明置顶窗口桌宠。

- **原理**：tkinter 创建无边框置顶窗口 -> 透明像素填充品红色(#FF00FF) -> win32 `SetLayeredWindowAttributes` 设置品红色为透明色键 -> 实现逐像素透明效果
- **依赖**：Python 3.x + Pillow + pywin32（Windows），均为 pip 可装
- **功能**：idle呼吸动画循环、左键拖拽移动、左键点击触发互动（眨眼/微笑轮替）、右键菜单（重置/退出）
- **帧格式**：与 DyberPet 相同的独立帧 PNG（透明背景），`pet_config.json` 定义动画状态和时序
- **优势**：零外部下载、完全可定制、代码透明可改
- **限制**：无养成系统/好感度/AI助手接入（需自行扩展）
- **模板**：`templates/run_pet.py` -- 完整可运行的桌面宠物运行时脚本

**使用方式**：
```bash
# 帧目录结构（与DyberPet兼容）：
# pet_name/
# ├── pet_config.json
# ├── icon.png
# └── animations/
#     ├── idle/       idle_000000.png ...
#     ├── wave/       wave_000000.png ...
#     └── ...

cd pet_name/
python run_pet.py
```

**适配 DyberPet 状态名**：run_pet.py 直接读取 pet_config.json，兼容 DyberPet 标准状态名（idle/run_right/run_left/drag/fail/jump/wave/wait）。已有 DyberPet 宠物包可直接用 run_pet.py 运行。

## 方案对比

| 方案 | 门槛 | 费用 | 互动丰富度 | AI生图 | 可定制性 |
|------|------|------|-----------|--------|---------|
| 豆包 | 零代码 | 免费 | 中 | 需自备图 | 低（EXE黑盒）|
| Codex+HatchPet | 低 | $20/月 | 高 | 内置 | 中 |
| AI在线服务 | 极低 | 部分免费 | 中 | 内置 | 低 |
| DyberPet | EXE零/源码中 | 免费 | 最高 | 需自备图 | 最高（MOD生态）|
| Shimeji | 中 | 免费 | 低 | 需自备图 | 中 |
| Live2D | 高 | 免费/付费 | 最高 | 需自备图 | 高 |
| Python自运行 | 低(需pip) | 免费 | 中高 | 需自备图 | 高（代码全开源）|

## 照片变桌宠：完整工作流

适用场景：想把女朋友/宠物/自己的照片变成一个活蹦乱跳的桌面宠物。

### ⚠️ 风格选择：chibi vs 非chibi

**风格默认值**：默认推荐非 chibi 路线，除非用户明确要求 Q 版风格——chibi 化真实人物照片"很容易失真"。

三条非chibi路线（按还原度排序）：

| 路线 | 还原度 | 动画丰富度 | 门槛 | 适用场景 |
|------|--------|-----------|------|---------|
| 豆包客户端直出 | 100%真人 | 低（弹跳/平移） | 零代码3分钟 | 最快出效果 |
| 真人抠图+DyberPet | 100%真人 | 低（微动画2-4帧） | 需Python | 要DyberPet养成系统 |
| 半写实Hatch Pet | ~80% | 高（57帧9种动作） | 自动化流水线 | 要丰富动画+可接受插画风格 |

**路线1：豆包客户端直出（零失真，最快）**
- 直接用真实照片，不经过任何风格转换
- 豆包自动抠背景 -> 生成透明窗口桌面宠物EXE
- 详见上方"方案1：豆包客户端一键生成"的万能指令
- 注意：复杂背景照片抠图可能不干净，可先用 remove.bg 或 rembg 去背景

**路线2：真人照片抠图 + DyberPet（零失真 + 互动系统）**
- 用 rembg/remove.bg 去背景 -> 透明PNG -> 生成2-4帧微动画 -> 装进DyberPet
- 微动画方案：idle=同一张图上下移2px（呼吸感），click=放大2%（弹跳感）
- DyberPet 提供拖拽、养成、好感度、对话气泡等完整互动功能
- 动画有限但100%是真人

**路线3：半写实插画风 Hatch Pet（折中方案）**
- 仍走 Hatch Pet 全流程，但风格从"chibi"改为"半写实插画"
- 保留真实比例（5-6头身，不缩头身比），面部特征尽量还原
- 提示词关键修改：`Turn this person into a semi-realistic anime illustration. NOT chibi. Keep realistic proportions.`
- 动画最丰富（9种动作状态57帧），但仍是AI重绘，有轻微风格化

### ⚠️ 风格选型（必须先问用户）

**关键**：用户提供真实人物照片时，**不要默认推荐 chibi/Q版风格**。很多用户觉得 Q版"很容易失真"、"不像本人"。必须先询问用户的风格偏好，再选路线。

| 风格 | 还原度 | 动画丰富度 | 制作方式 |
|------|--------|-----------|---------|
| 真人直出（零失真） | 100% | 低（程序级弹跳/平移） | 豆包客户端一键 或 抠图+DyberPet |
| 半写实插画 | ~80% | 高（57帧9种动作） | Hatch Pet 流水线，style改 semi-realistic |
| Q版 chibi | ~60% | 高（57帧9种动作） | Hatch Pet 流水线，默认 chibi |

**建议**：先给路线1（豆包）快速出效果，不满意再走路线2（真人+DyberPet）或路线3（半写实）。
详见 `references/non-chibi-routes.md` 获取三条路线的完整操作步骤。

### 方法论对比

| 方法 | 原理 | 效果 | 适用 |
|------|------|------|------|
| 豆包客户端直出 ✅ | 真人照片 + 万能指令 -> 豆包自动抠背景 -> 一键EXE | 100%真人，交互固定但零门槛 | 快速出效果首选 |
| 真人抠图+DyberPet ✅ | rembg/remove.bg 抠背景 -> 2-4帧微动画 -> DyberPet | 100%真人，可拖拽/养成/对话 | 要丰富互动且不失真 |
| 半写实Hatch Pet ✅ | 图生图半写实化（不缩头身比）-> 57帧动画 -> DyberPet | 80%还原，动画最丰富 | 要动画又要辨识度 |
| 图生图chibi还原 | 照片作为参考图 -> qwen-image-edit-plus chibi化 -> wan2.7-image-pro逐行生成动画态 -> Hatch Pet全流程 -> DyberPet | Q版卡通，9种动画状态 | 用户明确想要Q版风格时 |
| 纯文生图chibi还原 ❌ | vision分析照片特征 -> qwen-image-2.0-pro文生图生成Q版角色 -> Hatch Pet全流程 | ❌ 像不像全凭文字描述精度，容易不像 | 仅在没有图生图模型时使用 |
| 视频模型生动画帧 ❌ | 用i2v模型生成动作视频 -> 逐帧提取 -> 拼图集 | ❌ 不可行（见下方陷阱） | - |

### ⚠️ 关键决策：chibi化 vs 保留真人形象

**关键决策**：当桌宠素材是真实人物照片时，用户可能拒绝 Q 版/chibi 化，因为"很容易失真"——AI 重绘后不像本人。此时必须提供非 chibi 路线，而不是默认推 chibi 工作流。

三条非chibi路线（按还原度排序）：

| 路线 | 原理 | 还原度 | 动画丰富度 | 门槛 |
|------|------|--------|-----------|------|
| **A: 豆包客户端直出** | 真人照片直接喂豆包 -> 抠背景 -> 生成EXE | 100%真人 | 低（弹跳/平移） | 零代码3分钟 |
| **B: 真人抠图 + DyberPet** | rembg抠图 -> 透明PNG -> 2-4帧微动画 -> DyberPet | 100%真人 | 低（微动画2-4帧） | 需Python基础 |
| **C: 半写实插画 Hatch Pet** | 照片 -> qwen-image-edit-plus半写实化（不缩头身比）-> 57帧动画 -> DyberPet | ~80% | 高（9种动作57帧） | 自动化流水线 |

**决策规则**：
- 用户素材是真人照片 + 明确不想失真 -> **路线A**（最快出效果），不满意再走**路线B**
- 用户接受轻微风格化但不要Q版大头 -> **路线C**（将 Hatch Pet 的 style 从 chibi 改为 semi-realistic，保留5-6头身比）
- 用户素材是宠物/动漫角色/非真人 -> chibi路线仍为首选

#### 路线A：豆包客户端直出（零代码，保留100%真人）

1. 下载电脑版豆包客户端（非网页版）：https://www.doubao.com/download
2. 设置中开启「办公任务Turbo模式」和「本地电脑」权限
3. 粘贴照片 + 万能指令（见下方），等1-2分钟生成EXE
4. 注意：复杂背景照片抠图可能不干净，先用rembg去背景效果更好

**豆包万能指令**：
```
请使用我提供的角色图片，制作一个Windows桌面宠物程序。基本要求：去除图片背景，
窗口透明、无边框、始终置顶。桌宠可用鼠标左键拖动位置，点击角色时，轮流触发几种
简单互动，例如跳跃、更换表情，互动时随机显示简短、有趣的中文对话气泡，气泡背景
不透明，不要遮挡角色。右键菜单包括：调整大小、置顶开关，退出程序，鼠标滚轮可以
调整桌宠大小，还有一个靠边吸附的效果，生成可直接双击的.exe文件。
```

#### 路线B：真人抠图 + DyberPet 微动画

1. AI抠图去背景：`pip install rembg onnxruntime`，然后 `rembg i photo.jpg output.png`
2. 裁剪到角色主体，统一尺寸（建议 384x512）
3. 生成2-4帧微动画（idle: 上下浮动2px; click: 放大2%弹跳）
4. 组装 DyberPet 格式（pet_config.json + animations/目录）
5. 复制到 DyberPet 的 pets/ 目录运行

#### 路线C：半写实插画 Hatch Pet

将 prepare_photo_pet.py 的 prompt 模板中所有 chibi 相关描述替换为半写实：
- "chibi cartoon character" -> "semi-realistic anime illustration character"
- 去掉 "NOT chibi, keep normal 5-6 head ratio"（关键：不缩头身比）
- 动画提示词也去掉萌系描述，强调 "natural body movement, realistic proportions"

然后走标准 Hatch Pet 流水线：image_gen_adapter -> extract_strip_frames -> compose_atlas -> validate -> qa -> convert_to_dyberpet

### 推荐工作流（chibi路线）：照片 -> 图生图chibi化 -> 57帧动画 -> DyberPet (~15分钟)

**核心原则**：用户提供真实照片时，**必须优先用图生图模型**（qwen-image-edit-plus / wan2.7-image-pro），通过参考图输入保持主体特征。纯文生图（qwen-image-2.0-pro）从文字描述生成的角色容易"不像同一个人"，不适合照片变桌宠场景。

**⚠️ chibi 风格失真风险**：图生图 chibi 化虽然能保留面部特征，但Q版风格本身会大幅改变头身比和五官比例，部分用户会觉得"不像本人"。**提供真实人物照片时，务必先询问风格偏好**（chibi Q版 vs 半写实 vs 真人直出），不要默认走 chibi 路线。
1. **先问风格偏好**：用户提供真实人物照片时，不要默认走 chibi。问一句"你想要Q版卡通风格还是保留真实形象？"——很多用户明确表示 chibi"很容易失真"。
2. **图生图优先于文生图**：确定要AI重绘时，必须用图生图模型（qwen-image-edit-plus / wan2.7-image-pro）通过参考图保持主体特征。纯文生图从文字描述生成的角色容易"不像同一个人"。
3. **多角度参考**：如果用户提供了多张照片（正面/背面/半身），用 vision_analyze 逐张分析并整合成角色特征文档，后续 prompt 可精确引用。模板见 `templates/character-profile-template.md`。

**前提**：hermes-hatch-pet 技能已部署（DashScope 图生图/文生图均通过同一 API Key）

#### 自动化方式（推荐）：prepare_photo_pet.py

hermes-hatch-pet 技能包含 `prepare_photo_pet.py`，一键将照片转换为完整的 hatch-pet 运行目录：

```bash
python <hermes-hatch-pet>/scripts/prepare_photo_pet.py \
    --photo photo.jpg \
    --pet-name "Name" \
    [--description "可爱女孩蓝裙子"] \
    [--style chibi] \
    [--output-dir output/run-<timestamp>]
```

该脚本自动：
1. 复制照片到运行目录
2. 用 qwen-image-edit-plus（edit 模式）将照片 chibi 化
3. 用 wan2.7-image-pro（ref 模式）为每个动画状态创建参考生成 job
4. 生成完整 imagegen-jobs.json + prompt 文件 + README

然后直接跑流水线：
```bash
python <hermes-hatch-pet>/scripts/image_gen_adapter.py --run-dir <run-dir> --all
# 后续：extract_strip_frames → compose_atlas → validate → qa → convert_to_dyberpet
```

#### 手动方式（不推荐，仅用于调试）

**步骤1：照片chibi化（图生图）**

用 qwen-image-edit-plus 将真实照片转为 Q 版角色，同时保持长相特征：

```
端点：POST /api/v1/services/aigc/multimodal-generation/generation（同步）
模型：qwen-image-edit-plus
输入：照片URL + 文字指令
返回：chibi化后的角色图片URL（保持脸型、发型、五官）
```

提示词模板：
```text
Turn this person into a cute chibi cartoon character.
Keep the SAME face features, hairstyle, and expression.
On a pure magenta (#FF00FF) background.
```

详见 `references/dashscope-image-api.md` 的"图生图/图像编辑 API"章节和 `scripts/qwen_image_gen.py`。

**步骤2：逐行生成动画（多图参考生成）**

用 wan2.7-image-pro 基于 chibi base 图逐行生成9个动画状态的条状图：

```text
端点：POST /api/v1/services/aigc/multimodal-generation/generation（同步）
模型：wan2.7-image-pro
输入：chibi base图 + 动作描述
返回：该动画状态的条状图（如 idle 6帧横条）
```

提示词模板（每行不同动作）：
```text
[chibi角色描述], [动作描述 e.g. waving hand / jumping up / running right],
on a pure magenta (#FF00FF) background, simple chibi style,
8-frame strip animation layout, consistent character across all frames
```

**步骤3~6**：跑 hermes-hatch-pet 剩余流程（帧提取 → 拼图 → 验证 → 质检 → DyberPet转换）

**步骤3：跑 hermes-hatch-pet 全流程**

```bash
cd <hermes-hatch-pet>/scripts
python prepare_pet_run.py --pet-name "Name" \
  --pet-notes "特征描述" --reference path/to/chibi_base.png \
  --output-dir output/run-<timestamp>
python image_gen_adapter.py --run-dir output/run-<timestamp> --all
```

后续自动执行帧提取(extract_strip_frames) → 拼图(compose_atlas) → 验证(validate_atlas) → 质检(qa_adapter) → DyberPet转换(convert_to_dyberpet)。

**步骤4：安装到 DyberPet**

复制 `dyberpet_pack/<pet_name>/` 到 DyberPet 的 `pets/` 目录。

### 真人照片直出路线（不chibi化，路线2优化版）

当用户要求"100%保留真人长相"时走此路线。不经过AI重绘角色，直接抠图+局部叠加+物理动画。

**关键陷阱（kimi-k3深度分析发现，2026.7.30）**：

1. **必须用半身照（胸部以上）**：全身照缩到384x512后脸部仅60x80px，AI表情变体肉眼不可见。半身照脸部可达150x200px。
2. **局部叠加法（核心技巧）**：AI生成"闭眼版"后不整图采用，只裁眼部矩形区域（带羽化）贴回原图。除眼部外像素100%一致 -> 零闪烁。嘴部微笑同理。
3. **变体像素级对齐**：AI编辑输出的图头部位置必然偏移几像素 -> 帧动画播放时头部抖动。用 `cv2.phaseCorrelate` 计算平移量并校正，误差容忍<1.5px。
4. **高分辨率母版策略**：全程保持768x1024以上母版做所有操作（抠图、AI编辑、对齐、动画），最后一次性缩放到交付尺寸。不要先缩再编辑（两次重采样损失）。
5. **固定画布**：所有动画帧在固定尺寸透明画布内做位移/缩放。禁止逐帧 getbbox()（每帧裁剪结果不同 -> 尺寸不一致 -> 播放跳动）。
6. **GIF预览验证**：用Pillow合成每状态GIF（10行代码）检查闪烁/抖动/节奏。豆包客户端无法加载DyberPet宠物包，不能用于预览。
7. **拥抱"纸片立牌"设定**：不要假装能走路。用squash&stretch（挤压拉伸）制造喜剧感：拖拽纵向拉长5%、落地压扁85%->回弹105%->归位、happy快速小幅度弹跳。真人立牌+夸张变形是成熟表现手法。

**优化版帧设计（44帧，8状态）**：

| 状态 | 帧数 | 时长 | 内容 |
|------|------|------|------|
| idle | 8 | 500ms | 锚定底部纵向缩放98.5%-100%呼吸（4秒循环） |
| walk_left | 6 | 120ms | 倾斜摇摆+起伏，移动2-4px/帧 |
| walk_right | 6 | 120ms | 镜像walk_left |
| drag | 4 | 100ms | 纵向拉伸5%+惊讶表情 |
| fall | 3 | 150ms | 旋转下落（喜剧效果） |
| land | 3 | 120ms | 压扁85%->回弹105%->归位 |
| interact_1 | 6 | 150ms | 局部叠加眨眼+微笑 |
| interact_2 | 6 | 150ms | 微笑+Pillow程序化贴爱心图案 |

**照片筛选标准**：正面或微侧面、双臂自然下垂贴身体、头发完整入镜、无遮挡物、光线均匀、纯色背景最佳、源图高度>=1500px。

**AI表情变体失败备选**：MediaPipe Face Mesh标注特征点 -> Delaunay三角剖分 -> 对嘴角/眉毛/眼睑做微位移warp。完全无身份漂移风险（像素全部来自原图）。

**⚠️ 白色矩形框陷阱（2026.7.30实测发现）**：

AI编辑API（qwen-image-edit-plus）生成的变体图是白底RGB，如果直接裁矩形区域贴回透明背景原图，白色边缘像素会形成可见的白色矩形框，动画播放时表现为"闪白框"。

**修复方案 -- 差异掩码法（diff-based mask extraction）**：

```python
import cv2, numpy as np
from PIL import Image

# 1. 计算变体与原图的逐像素差异
diff = np.abs(variant.astype(np.int16) - original.astype(np.int16))
diff_max = diff.max(axis=2)  # RGB取最大差异

# 2. 阈值化：只保留真正变化的像素（眼睛闭合/嘴巴微笑）
threshold = 35  # 25-35之间效果最佳
change_mask = (diff_max > threshold).astype(np.uint8) * 255

# 3. 形态学清理：去噪+填洞
kernel = np.ones((5, 5), np.uint8)
change_mask = cv2.morphologyEx(change_mask, cv2.MORPH_OPEN, kernel)
change_mask = cv2.morphologyEx(change_mask, cv2.MORPH_CLOSE, kernel)

# 4. 限制到人物alpha区域内（排除背景变化）
change_mask = cv2.bitwise_and(change_mask, person_alpha)

# 5. 高斯羽化边缘
mask_blurred = cv2.GaussianBlur(change_mask, (9, 9), 0)

# 6. 组装RGBA补丁（只含变化像素，其余透明）
patch_rgba = np.dstack([variant_rgb, mask_blurred])
```

**关键参数**：threshold=35（过低会包含全局色调差异导致整图补丁，过高会丢失眨眼细节）；限制到面部区域（眼部y=12%-30%、嘴部y=22%-40%）可进一步减少噪声。

详见 `references/real-photo-route-analysis.md`

### 身体动作动画路线（图生图生成全身动作变体，2026.7.30）

当用户需要身体动作动画（下跪、蹦跳、鞠躬、双手捂脸、两手张开等）而非面部表情微动画时走此路线。用 qwen-image-edit-plus 图生图生成不同姿态的全身图，再用 alpha 混合做过渡帧。

**与面部表情路线的区别**：面部表情路线只裁眼部/嘴部局部叠加（零闪烁），身体动作路线整张图替换（人物姿态完全变化），因此不需要差异掩码，但需要白底去除。

**工作流**：
1. 选全身正面照 -> GrabCut 抠图 -> 标准化母版（384x576 或 512x768）
2. 母版贴白底 -> qwen-image-edit-plus 图生图生成 N 个动作变体（每个 0.2 元）
3. 白底去除（`remove_white_bg` 函数）-> 透明背景动作图
4. alpha 混合生成过渡帧（站立 -> 动作 -> 站立）
5. 组装 tkinter 桌宠程序（含文字气泡互动系统）

**动作 prompt 模板**（英文，保持人物一致性）：
```
Same person, same clothes, same hairstyle. [动作描述]. IMPORTANT: full body must be completely visible including all hair, both hands, both feet, and the entire body within the frame. Do not crop any body parts. Plain white background, full body shot.
```
示例：`now kneeling on the ground with both knees on the floor, hands clasped in front of chest in a respectful gesture, head slightly bowed`
示例：`standing with both feet firmly on the ground, both arms spread wide open to the sides at shoulder height in a welcoming gesture, smiling happily`

⚠️ **prompt 必须强调完整身体可见**：不写"full body completely visible including all hair, both hands, both feet"时，AI容易裁切手脚。特别是 open_arms 动作，不写"both feet firmly on the ground"会生成单脚站立。

**白底去除函数 -- flood fill strict 法（2026.7.30 验证通过，8.5/10）**

⚠️ **关键陷阱**：简单的 `remove_white_bg`（threshold=240）和 GrabCut 都会误删白色衣服（白裙、白袜）。因为白色衣服和白色背景像素值接近，基于颜色阈值的方案无法区分。需要用 **flood fill from edges** -- 只删除与图像边缘连通的白色区域，保留被身体包围的白色衣物。

```python
import cv2, numpy as np
from PIL import Image

def floodfill_bg_removal(img, threshold=245):
    """Flood fill from edges: removes only white connected to border.
    Preserves enclosed white regions (white skirt, white socks)."""
    rgba = np.array(img.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(np.int16)
    H, W = rgb.shape[:2]

    # Strict threshold: only nearly-pure-white is background
    # White clothing has shadows/texture, won't hit 245+
    min_channel = rgb.min(axis=2)
    is_white = min_channel > threshold
    white_binary = np.where(is_white, 255, 0).astype(np.uint8)

    # Connected components: find white regions connected to border
    num_labels, labels = cv2.connectedComponents(white_binary, connectivity=4)
    border_labels = set()
    for x in range(W):
        if labels[0, x] > 0: border_labels.add(labels[0, x])
        if labels[H-1, x] > 0: border_labels.add(labels[H-1, x])
    for y in range(H):
        if labels[y, 0] > 0: border_labels.add(labels[y, 0])
        if labels[y, W-1] > 0: border_labels.add(labels[y, W-1])

    bg = np.zeros((H, W), dtype=np.uint8)
    for label in border_labels:
        bg[labels == label] = 255

    # Foreground = NOT background
    fg = np.where(bg > 0, 0, 255).astype(np.uint8)

    # Cleanup: close holes, largest component, erode fringe, feather
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel, iterations=3)
    num_fg, fg_labels, fg_stats = cv2.connectedComponentsWithStats(fg, connectivity=8)[:3]
    if num_fg > 1:
        largest = 1 + np.argmax(fg_stats[1:, cv2.CC_STAT_AREA])
        fg = np.where(fg_labels == largest, 255, 0).astype(np.uint8)
    fg = cv2.erode(fg, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    alpha = cv2.GaussianBlur(fg, (3, 3), 0)

    rgba[:, :, 3] = alpha
    alpha_float = alpha.astype(np.float32) / 255.0
    for c in range(3):
        rgba[:, :, c] = (rgba[:, :, c] * alpha_float).astype(np.uint8)
    return Image.fromarray(rgba)
```

**为什么 threshold=245 而非 240**：白裙有褶皱阴影、纹理变化，RGB 值通常在 200-240 范围。纯白背景在 245-255 范围。245 是分界点 -- 只删"几乎纯白"的背景，保留有阴影的白色衣物。实测 open_arms 动作图（含白裙+白袜+黑鞋）得分 8.5/10，头发/双手/白裙/双脚/白袜全部完整。

**6种方案实测对比（2026.7.30）**：

| 方案 | 白裙保留 | 头发 | 手指 | 双脚 | 评分 |
|------|---------|------|------|------|------|
| threshold=240 白色去除 | ❌ 删掉 | 部分 | 部分 | 缺失 | 3/10 |
| threshold=225+形态学 | ❌ 删掉 | 部分 | 部分 | 缺失 | 3/10 |
| GrabCut v2（底3%标BGD）| ❌ 删掉 | OK | OK | ❌ 截断 | 6/10 |
| GrabCut v3（仅顶标BGD）| ❌ 删掉 | OK | OK | ❌ 截断 | 4/10 |
| Hybrid flood+GrabCut | ❌ 删掉 | OK | OK | ❌ 截断 | 3/10 |
| **flood fill strict 245** | **✅** | **✅** | **✅** | **✅** | **8.5/10** |

GrabCut 持续失败的原因：GrabCut 基于颜色+纹理建模，白色衣物与白色背景颜色分布几乎相同，GMM 无法区分。flood fill 不依赖颜色建模，只看连通性 -- 背景白连通到边缘，衣物白被身体包围不连通。

**绿幕色键法 -- 当 flood fill 仍不够完整时（2026.7.31 验证通过）**：

当 flood fill strict 245 对某些动作图效果仍不理想（如 open_arms 手脚头发边缘有残缺），改用**绿幕方案**：让 AI 生成纯绿色背景的动作图，再用 HSV 色键抠图。核心优势：绿色与人物肤色/黑衣/白裙完全无重叠，抠图边界精确。

**步骤**：
1. 用 qwen-image-edit-plus 图生图，prompt 中要求纯绿背景：`The background must be PURE BRIGHT GREEN (chroma key green #00FF00), solid color, no texture.`
2. HSV 色键检测绿色背景：`hsv[:,:,0] >= 35 & hsv[:,:,0] <= 90 & hsv[:,:,1] > 50` = 绿色区域
3. 形态学清理 + 最大连通域 + 侵蚀1px去绿边 + 高斯羽化
4. **绿色溢出清除（despill）**：对所有前景像素，如果 G > max(R, B)，将 G 降至 max(R, B)。消除手指/头发边缘的绿色偏色。

```python
# despill 核心逻辑（向量化，不用逐像素循环）
r_ch, g_ch, b_ch = rgb[:,:,0].copy(), rgb[:,:,1].copy(), rgb[:,:,2].copy()
max_rb = np.maximum(r_ch, b_ch)
spill_mask = g_ch > max_rb + 3
g_ch[spill_mask] = max_rb[spill_mask]
```

**实测对比**：open_arms 动作图，flood fill strict 245 得分 8.5/10 但头发边缘有残缺；绿幕+despill v2 得分 7/10（指尖微量绿色残留，但在 192x288 显示尺寸下不可见）。绿幕方案对手指/脚趾等细枝末节的保留更好，适合对边缘精度要求高的场景。

**rembg (U2Net) 在绿幕上的表现（2026.7.31 验证）**：

⚠️ **rembg 在白色背景上对白色衣物同样失败** -- 与 GrabCut 一样，rembg 的 U2Net 模型虽然能处理头发，但白色衣物在白色背景上的边界判定同样不准（kneel 3/10，jump 4/10，白裙严重破损）。

**rembg 在绿幕背景上表现**：

| 动作 | rembg on 白底 | rembg on 绿幕 | 色键+despill on 绿幕 | 最佳方案 |
|------|-------------|-------------|-------------------|---------|
| kneel | 3/10 (白裙没了) | 7.5/10 (无绿残留，但脚被源图截断) | 5/10 (边缘粗糙) | rembg on 绿幕 |
| jump | 4/10 (白裙破损+手截断) | 8/10 (全身完整，无绿残留) | 7/10 (无绿残留) | rembg on 绿幕 |
| bow | 8/10 | - | - | rembg on 白底即可 |
| cry | 9/10 | - | - | rembg on 白底即可 |
| open_arms | 6/10 (绿残留) | 6/10 (指尖绿残留) | 7/10 (微量绿残留) | 色键+despill on 绿幕 |

**策略**：
1. 白底图先直接用 rembg -- 如果人物穿深色衣服，效果就够好（bow 8/10, cry 9/10）
2. 白裙/白袜被误删 -> 重新用绿幕背景生成 -> rembg 抠图
3. rembg on 绿幕有绿色残留 -> 改用色键+despill
4. **没有万能方案，需要逐图验证**：用 vision_analyze 检查6项（头发/双手/白裙/双脚/白袜/绿色残留），低于7分换方案
5. **以上方案均不理想（头发/手脚反复不完整）-> 放弃原图，全部用AI文生图生成**（见下方"终极方案"）

### 终极方案：用AI图生图生成全部动作图（2026.7.31 验证通过）⭐⭐⭐

**触发条件**：原图抠图经过 threshold/GrabCut/flood fill/绿幕色键/rembg 多轮尝试后，头发/双手/双脚仍然反复不完整。用户明确说"不要用原图抠图了，直接生成一个没有背景的任务图"。

**核心思路**：不再从真人照片抠图，而是用 qwen-image-edit-plus 图生图 API，以真人照片为参考输入，生成全部6张图（master + 5动作），再用 rembg 去背景。图生图模型能保持面部特征一致性，避免"像换了一个人"的问题。

### ⚠️ 陷阱7：纯文生图导致面部失真（2026.7.31 实测发现）⭐⭐⭐

**问题**：用 wanx2.1-t2i-turbo 纯文生图生成角色图时，AI从文字描述"凭空想象"一个人物面部，生成的脸与真人照片完全不像。用户反馈"面部失真了，像换了一个人"。即使 prompt 描述再详细，文生图模型也无法还原特定人物的面部特征。

**根因**：wanx2.1-t2i-turbo 是纯文生图模型，没有参考图输入接口，无法"看到"目标人物长什么样。它只能根据文字描述生成一个"大致符合描述"的随机面孔。

**修复**：改用 qwen-image-edit-plus（图生图模型），将真人照片作为参考输入：

```python
# ❌ 纯文生图 -- 面部失真，像换了一个人
# wanx2.1-t2i-turbo 没有 image 输入接口，只接受 text prompt
payload = {"model": "wanx2.1-t2i-turbo", "input": {"prompt": "cute young East Asian woman..."}}

# ✅ 图生图 -- 保持面部特征一致
# qwen-image-edit-plus 接受 image + text 输入，能看到参考照片
payload = {
    "model": "qwen-image-edit-plus",
    "input": {
        "messages": [{
            "role": "user",
            "content": [
                {"image": "data:image/jpeg;base64," + img_b64},  # 参考照片
                {"text": "Same person in the reference photo - keep her face EXACTLY the same. [动作描述]..."}
            ]
        }]
    },
    "parameters": {"size": "768*1024"}
}
```

**prompt 关键**：必须写 `Same person in the reference photo - keep her face, hairstyle, and facial features EXACTLY the same`，强调保持面部一致性。

**双参考照片（2026.7.31 验证）⭐**：当用户提供了多张照片（如半身照+全身照）时，将两张照片同时传给 qwen-image-edit-plus，效果显著优于单张。API 的 `content` 数组支持多张 image 输入：

```python
payload = {
    "model": "qwen-image-edit-plus",
    "input": {
        "messages": [{
            "role": "user",
            "content": [
                {"image": "data:image/jpeg;base64," + photos["halfbody_gazebo.jpg"]},   # 半身照（面部细节）
                {"image": "data:image/jpeg;base64," + photos["front_bridge.jpg"]},      # 全身正面照
                {"text": prompt}
            ]
        }]
    },
    "parameters": {"size": "768*1024"}
}
```

prompt 中加入面部特征详细描述（先用 vision_analyze 分析两张照片提取）：`oval face, round almond eyes with double eyelids, natural straight eyebrows, small delicate nose, full lips with slightly upturned corners, long straight black hair past shoulders`。

### ⭐⭐⭐ Master 面部参考法（2026.7.31 验证 -- 面部一致性最优方案）

**触发条件**：用户反馈"面部失真，像换了一个人"或"后面的图片都用第一张面部"。

**核心思路**：先生成 master/idle 图（用双参考照片），用户确认面部像后，**用 master 原始图作为唯一参考图**生成全部5个动作图。因为 master 的面部已经被用户"批准"，用它做参考能确保所有动作面部一致。

**为什么比双参考照片更好**：双参考照片传的是原始照片，AI 需要同时理解面部+服装+姿势。改用 master 原始图做参考后，AI 只需要改姿势，面部/服装/风格已经统一，一致性大幅提升。

**工作流**：
1. 用双参考照片（半身+全身）生成 master -> rembg 抠图 -> 用户确认面部
2. 用 master 原始图（`master_dualref_raw.png`，768x1024）作为**唯一参考图**传给 qwen-image-edit-plus
3. prompt 强调 `Same person in the reference photo - keep her face EXACTLY the same. Only change the body pose.`
4. 每个动作的 prompt 必须**极其详细地描述姿势** + **明确否定错误姿势**：
   - kneel(磕头): `KOWTOW (FULL PROSTRATION). The person is lying face-down on the ground. Both knees are on the floor. Her chest and torso are bent forward all the way down. Her forehead is touching the ground. Both arms are extended forward on the floor in front of her head, palms flat on the ground. She is in a full prostration/kowtow position. View from the side so you can see the full prostration pose.`
   - jump: `Both feet are OFF the ground. She is airborne. Both arms are raised straight UP above her head with fingers spread wide. Legs are bent at knees. She is NOT standing. She MUST be in the air.`
   - ⚠️ **kneel 必须用"KOWTOW"+"forehead touching ground"+"full prostration"**：简单写"kneeling on the ground"或"hands clasped in front of chest"时，AI会生成站立姿势。必须用极端描述（额头触地、趴在地上）才能让AI生成正确的跪拜姿势（2026.7.31 实测验证）。
5. 生成后**逐张用 vision_analyze 验证**姿势正确性（见下方"动作姿势验证"）

**prompt 模板（master 面部参考法）**：
```python
base_prompt = (
    "This is the SAME person in the reference photo. Keep her face EXACTLY the same - "
    "same eyes, same nose, same mouth, same hairstyle, same face shape. Do NOT change her face at all. "
    "Only change the body pose. "
    "She wears: [服装描述]. Full body visible from top of head to bottom of shoes. "
    "Background must be PURE SOLID BRIGHT GREEN chroma key color (#00FF00), completely flat. "
    "Studio lighting, sharp focus, high quality."
)
# 每个动作的 pose 描述必须包含：
# 1. 正面描述（应该是什么姿势）
# 2. 否定描述（不是什么姿势）
# 3. 关键身体部位位置（膝盖在哪、手在哪、脚在哪）
```

**实测结果（2026.7.31）**：5/5 动作图全部通过视觉验证 -- kneel 双膝着地✅、jump 双脚离地✅、bow 上半身前倾✅、cry 双手捂脸✅、open_arms 双臂伸展✅。面部与 master 一致。

**⭐⭐⭐ 相机角度技巧 -- 迫使AI脱离站立构图（2026.7.31 最终方案）**：

**问题**：即使用 master.png 做唯一参考 + 极端化 prompt，AI 仍经常生成站立姿势 -- 因为 master.png 本身是正面站立图，AI 倾向于复制参考图的构图和姿态。

**突破**：在每个动作的 prompt 中指定**不同的相机角度**，迫使AI改变构图布局，从而生成正确姿势：

| 动作 | 相机角度 | prompt 关键描述 | 效果 |
|------|---------|---------------|------|
| kneel(磕头) | 侧视地面视角 | `CAMERA: Side view, shot from the right side at ground level` | ✅ 双膝着地、额头触地 |
| jump(跳跃) | 仰视低角度 | `CAMERA: Low angle shot from below, looking up at the person` | ✅ 双脚离地、双臂高举 |
| bow(鞠躬) | 左侧视角 | `CAMERA: Side view from the left, full body visible` | ✅ 前倾45-60度 |
| cry(哭泣) | 俯视高角度 | `CAMERA: Front view, slightly above eye level looking down` | ✅ 双手捂脸 |
| open_arms(展臂) | 正面平视 | `CAMERA: Front view, eye level, full body` | ✅ T形展臂 |

**为什么有效**：相机角度改变了画面构图的约束。当 master 是正面站立、prompt 要求侧视地面视角时，AI 必须重新构图，无法简单复制参考图的站立姿态。不同角度 = 不同构图 = 不同姿势。

**完整 prompt 模板（含相机角度）**：
```python
actions = {
    "kneel": (
        "Same person as the reference photo - keep her face EXACTLY the same. "
        "Same oval face, almond eyes, small nose, full lips, long straight black hair. "
        "Same outfit: [服装描述]. "
        "Background: PURE SOLID GREEN (#00FF00). "
        "CAMERA: Side view, shot from the right side at ground level. "
        "POSE: FULL PROSTRATION / KOWTOW. The person is lying face-down on the ground. "
        "Both knees on floor. Forehead touching the floor. "
        "Both arms extended forward on ground, palms flat. "
        "Body MUST be LOW and HORIZONTAL, NOT standing."
    ),
    "jump": (
        "... CAMERA: Low angle shot from below, looking up at the person. "
        "POSE: JUMPING HIGH IN AIR. Both feet OFF the ground, legs bent at knees. "
        "Both arms raised straight UP above head. She is NOT standing. She is in MID-AIR."
    ),
    # ... 其他动作同理
}
```

**v4 脚本**：`scripts/gen_actions_v4.py` -- 完整实现此方案的生成脚本。

**废弃方案**：
- ~~face_replace.py（面部裁贴替换）~~ -- 产生"两张脸"诡异效果，已废弃
- ~~双参考照片生成动作图~~ -- AI 无法同时保持面部+改变姿势，面部失真严重
- ~~gen_actions_masterface.py（单参考无相机角度）~~ -- AI 倾向复制站立姿势，kneel/jump 生成错误

### ⚠️ 面部替换后处理 -- 已废弃（2026.7.31 实测失败）⭐⭐⭐

**废弃原因**：面部裁贴替换会产生"两张脸"重影效果。用户反馈"有些动作上面两张脸，太诡异了"。即使使用椭圆 alpha 遮罩和高斯羽化，master 的面部与 AI 生成的面部在不同角度/光照下无法自然融合，视觉上形成双重面部。

**根因**：
1. 面部区域估算不准确 -- 侧面/低头动作（kneel、bow）的面部位置偏移，裁贴位置错误
2. 光照/色调不匹配 -- master 的面部光照条件与动作图不同，混合后有明显接缝
3. 透视角度不匹配 -- master 是正面面部，贴到侧面动作图上产生"两张脸"视觉

**正确方案**：不要做面部替换。用 master.png 做唯一参考图 + 不同相机角度生成（见上方"相机角度技巧"）。面部一致性靠生成端控制，不靠后处理裁贴。

~~旧方案（已废弃，仅存档参考）：从 master.png 裁剪面部区域，用椭圆 alpha 遮罩混合到每张动作图上。~~

⚠️ **OpenCV 5.0 破坏性变更**（如需其他人脸检测场景）：OpenCV 5.0.0 移除了 `cv2.CascadeClassifier`。替代方案：alpha 通道边界框估算或 `cv2.FaceDetectorYN_create()`。

### 动作姿势验证（vision_analyze 逐张检查）⭐

**生成动作图后必须验证**：AI 经常不按 prompt 生成正确姿势（如跪姿生成为站姿、跳跃生成为站立）。每张动作图生成后立即用 vision_analyze 检查：

```python
# 检查清单（每个动作都要问）
vision_analyze(
    image_url=f"{name}_masterref_raw.png",
    question=(
        f"这是'{action_name}'动作图。检查："
        f"1) 姿势是否正确（{expected_pose}）"
        f"2) 是否错误姿势（{wrong_pose}）"
        f"3) 全身是否完整可见"
        f"4) 面部是否清晰"
    )
)
```

**验证标准**：
| 动作 | 正确姿势 | 错误姿势（必须排除） |
|------|---------|-------------------|
| kneel | 双膝着地、双手合十 | 站立 |
| jump | 双脚离地、双臂高举 | 站立 |
| bow | 上半身前倾45度 | 站直 |
| cry | 双手捂脸 | 手放下 |
| open_arms | 双臂水平伸展 | 手臂下垂 |

**不通过时**：重新生成，在 prompt 中加强否定描述（如 `She is NOT standing. Her knees MUST be on the ground.`）。

**AI 不按 prompt 生成绿幕的降级策略**：实测6张图中只有2张生成绿幕，其余为白/灰底。不强求绿幕，统一用 rembg 处理即可。但当白底+白裙导致 rembg 失败（填充率>50%）时，该图改用单参考图版本（单张照片输入时 AI 更可能生成非白底）。

**规则**：当桌宠素材是特定真实人物（女朋友、家人、自己）时，生成动作图必须用图生图（qwen-image-edit-plus），不能用纯文生图（wanx2.1-t2i-turbo）。纯文生图只适用于不特定人物（如"一个动漫猫娘"）。

**AI 生成跪姿的脚截断问题（2026.7.31 发现）**：

AI 图生图模型（qwen-image-edit-plus）在生成跪姿时，即使 prompt 明确要求 "show full body from head to feet, zoom out, leave space below feet" 仍会在膝盖/小腿处截断。这是 AI 模型的固有局限。应对：接受跪姿不显示脚的自然限制，或改用侧跪姿势。

**图生图工作流（qwen-image-edit-plus，2026.7.31 验证通过）**：

```python
session = requests.Session()
session.trust_env = False  # 绕过系统代理SSL错误

# 读取参考照片为 base64
with open(photo_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
payload = {
    "model": "qwen-image-edit-plus",
    "input": {
        "messages": [{
            "role": "user",
            "content": [
                {"image": "data:image/jpeg;base64," + img_b64},
                {"text": prompt}  # "Same person... keep face EXACTLY the same. [动作]..."
            ]
        }]
    },
    "parameters": {"size": "768*1024"}
}
resp = session.post(API_URL, headers=headers, json=payload, timeout=90)
# 返回同步，不需要轮询
img_url = resp.json()["output"]["choices"][0]["message"]["content"][0]["image"]
```

**prompt 模板（图生图面部保持 + 绿幕背景）**：
```text
Same person in the reference photo - keep her face, hairstyle, and facial features EXACTLY the same.
She wears [服装描述]. Full body visible from top of head to bottom of shoes with space above head and below feet.
Background must be PURE SOLID BRIGHT GREEN chroma key color (#00FF00), completely flat.
Studio lighting, sharp focus, high quality, centered in frame. Pose: [动作描述].
```

**⚠️ 注意**：AI 可能不按 prompt 生成绿幕背景（实测6张中只有2张生成绿幕，其余为白/灰底）。不强求绿幕，统一用 rembg 处理即可 -- rembg 对 AI 生成图的白/灰底效果好（14%-22% 填充率，头顶留白2%-5%，脚部完整84%-99%）。

**质量检查（Python 脚本，不依赖 vision API）**：
```python
alpha = np.array(img)[:,:,3]
nonzero = np.count_nonzero(alpha > 128)
pct = 100 * nonzero / alpha.size  # 目标: 15%-25%
rows = np.where(np.any(alpha > 128, axis=1))[0]
top_pct = 100 * rows[0] / alpha.shape[0]  # 目标: >2%
bottom_pct = 100 * rows[-1] / alpha.shape[0]  # 目标: >84%
# 绿色残留: foreground中 G > max(R,B) + 10 的像素比例 < 5%
```

**⚠️ session.trust_env = False 必须**：DashScope API 通过系统代理（Clash Verge）访问时会产生 SSL EOF 错误。

**alpha 混合过渡帧**（⚠️ 已废弃 -- 会导致鬼影，见下方修复）：

~~每状态 4-6 帧，过渡曲线如 `[0.0, 0.5, 1.0, 0.5]`（站 -> 半 -> 动作 -> 半 -> 站）。~~

**改为硬切法**：每状态 4 帧纯动作图，不混入 master，不做半透明过渡。详见下方"推荐帧设计"。

⚠️ **alpha 混合会产生鬼影/双重影像（2026.7.31 实测发现）**：

`alpha_blend(master, action, t=0.5)` 在 t=0.5 时两个姿态各占50%透明度叠加，视觉上表现为两个动作的鬼影叠加（如站立+下跪同时出现），用户反馈为"两个动作叠加"。

**修复 -- 硬切法（唯一正确方案）**：不用 alpha 混合，每帧都是纯单姿态图。过渡帧也是纯动作图，不做半透明渐变：
```python
# ❌ 会产生鬼影 -- 两姿态半透明叠加
frame = alpha_blend(master, kneel, 0.5)  # 站立+下跪叠加

# ✅ 硬切：每帧只有一个姿态，不混入 master
frames = [kneel, kneel, kneel, kneel]  # 纯动作帧，无 master 覆盖
```
硬切虽然过渡不如 alpha 混合"平滑"，但避免了鬼影问题。对于真人照片桌宠，硬切更自然 -- 因为真人动作切换本来就是瞬间的，不需要半透明渐变。

**推荐帧设计（纯动作帧，无 master 覆盖，2026.7.31 验证）**：

⚠️ **关键修复**：之前的帧设计 `[master, action, action, action]` 会在动作动画的首帧显示 idle 站立姿态，造成"第一个动作覆盖了跳跃动作"的视觉问题。正确做法是**所有动作帧都是纯动作图，不混入 master**：

```python
# ✅ 正确：纯动作帧，无 master 覆盖
kneel_frames = [kneel, kneel, kneel, kneel]      # 跪 -> 保持 -> 保持 -> 保持
jump_frames = [jump, jump, jump, jump]             # 跳 -> 保持 -> 保持 -> 保持
bow_frames = [bow, bow, bow, bow]                  # 鞠躬 -> 保持 -> 保持 -> 保持
cry_frames = [cry, cry, cry, cry]                   # 捂脸 -> 保持 -> 保持 -> 保持
open_arms_frames = [open_arms, open_arms, open_arms, open_arms]  # 张开 -> 保持 -> 保持 -> 保持

# ❌ 错误：首帧或尾帧混入 master 会导致动作叠加/覆盖
# kneel_frames = [master, kneel, kneel, kneel]     # 首帧显示站立，叠加跪姿
# jump_frames = [master, jump, jump, master]      # 首尾都是站立，跳跃被覆盖
```

idle 状态独立循环（6帧呼吸动画），不与动作帧混合。双击切换动作时，从动作的第0帧开始播放，播完后保持最后一帧（`animation_finished=True`），不回 idle。

**互动系统 -- 双击切动作 + 单击换话术（2026.7.30 v3）**：

- **双击**：切换到下一个动作动画（idle->kneel->jump->bow->cry->open_arms->idle...），动画播完**保持最后一帧**不回idle
- **单击**：在当前动作绑定的3条话术中循环显示1条，气泡3秒消失
- **右键**：菜单（放大/缩小/恢复大小/重置位置/退出）
- **拖拽**：左键按住拖动

**右键缩放功能（2026.7.31 新增）**：

右键菜单支持放大/缩小/恢复大小，每次缩放1.25倍，范围0.25x-4.0x。缩放时重新加载全部帧到新尺寸，更新窗口大小和颜色键：

```python
def _set_zoom(self, new_zoom):
    new_zoom = max(0.25, min(4.0, new_zoom))
    self.zoom_level = new_zoom
    effective_scale = self.scale * self.zoom_level
    # 重新加载所有帧到新尺寸
    for state in self.states:
        # 读取原始帧 -> resize(effective_scale) -> 转color key
        ...
    # 更新窗口大小
    self.root.geometry(f"{self.frame_w}x{self.frame_h}+{x}+{y}")
    self.canvas.config(width=self.frame_w, height=self.frame_h)
    # 重新设置颜色键透明
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x00FF00FF, 0, LWA_COLORKEY)
```

**实现要点**：缩放后必须重新调用 `SetLayeredWindowAttributes` 重新设置颜色键透明，否则新尺寸的窗口不透明。

关键实现：用 `animation_finished` 标志控制 -- 动作动画播完后设为True，帧不前进也不回idle；idle状态循环不受影响。单击/双击通过300ms阈值区分（`DOUBLE_CLICK_THRESHOLD=300`）。

```python
# 每个动作绑定3条专属话术（共6动作x3条=18条）
phrases = {
    "idle":     ["嗯？~", "在呢~", "叫我吗？"],
    "kneel":    ["用户大人", "陛下奴婢给您请安了", "奴婢参见用户"],
    "jump":     ["好开心！", "嘿嘿嘿~", "用户用户！"],
    "bow":      ["用户万安", "用户您辛苦了", "给您行礼了"],
    "cry":      ["呜呜呜...", "用户别凶我...", "人家好委屈"],
    "open_arms":["亲爱的用户", "过来抱抱~", "想你了~"],
}
# 单击时显示当前动作的话术（按 action 循环）
# 双击时切换到 action_cycle 中的下一个动作
```

详见 `references/real-photo-route-analysis.md` 第 8 节。

### ⚠️ 为什么视频模型不适合照片变桌宠

DashScope 视频模型（wan2.7-r2v、happyhorse-1.1-i2v）理论上支持参考图生视频，实际多个不可行原因：

1. **API 不可用**：视频模型用原生 video_synthesis 接口，不走 OpenAI 兼容模式。2026.7.30 测试全部返回 400 "url error"，可能需 DashScope 控制台手动开通
2. **无法控制透明背景**：视频背景是实景/风景，不是纯色 chroma key，无法自动去除
3. **帧规格不匹配**：Hatch Pet 每帧 192x208，视频输出分辨率不同，逐帧裁剪+缩放导致质量损失
4. **9个动作需分别生成**：每个动画状态需要一段独立视频，生成+提取成本远高于直接文生图
5. **一致性无法保证**：不同 prompt 生成的视频中角色外貌可能不一致

**结论**：视频模型路线目前不实用。推荐走"chibi角色还原"路径。

## AI生图：透明背景角色图生成

桌面宠物制作的第一步是获取透明背景PNG角色图。方法：

1. **DashScope qwen-image-2.0-pro**（推荐，已验证可用）：通过OpenAI兼容模式调用，免费100次，约70秒/张，生成1728x2368 PNG。在prompt中指定纯色背景（如 `pure magenta background`）即可用于后续色键抠图。详见 `references/dashscope-image-api.md`，可复用脚本 `scripts/qwen_image_gen.py`
2. **豆包生图**：在指令中说明"透明背景"或生成白底图后用豆包抠图功能
3. **PNGMaker.ai**：在线文字转PNG，支持透明背景
4. **rembg库**：Python AI抠图，`pip install rembg onnxruntime`，可批量处理
   - **⚠️ 中国大陆Fallback**：rembg首次使用会从GitHub下载u2net.onnx模型（176MB），GitHub被墙时下载失败。备选方案：
     - 方案A：OpenCV GrabCut（本地运行，零下载）：用初始矩形框+迭代分割前景背景，效果略逊于rembg但不需要任何下载
     - 方案B：在线抠图 remove.bg（免费低分辨率）
     - 方案C：GitHub镜像下载模型文件后放到 `~/.u2net/u2net.onnx`

### DashScope qwen-image-2.0-pro 快速调用

```bash
# 命令行直接调用（需要 DASHSCOPE_API_KEY 环境变量）
python scripts/qwen_image_gen.py \
  --prompt "A cute chibi cat, standing pose, on a pure magenta background, no text" \
  --output pet_base.png
```

关键：端点是 `compatible-mode/v1/chat/completions`（不是 images/generations），超时设≥300秒，
返回的 `message.content` 是 list，图片URL在 `{"image": "url"}` 字段中。
失败的端点详见 `references/dashscope-image-api.md` 的"失败端点记录"表格。

## Hermes image_gen 后端检查

Hermes的image_gen工具集有5个内置provider，每个需要特定API key：
- FAL.ai（默认）：需要 FAL_KEY
- Krea：需要 KREA_API_KEY
- OpenAI：需要 OPENAI_API_KEY
- OpenAI Codex：需要 Codex OAuth token
- xAI：需要 XAI_API_KEY

检查脚本：`scripts/check_image_gen_backend.py`
配置方法：`hermes tools` -> Image Generation -> 选择provider -> 输入API key

## 适配 Hatch Pet 到 Hermes

Hatch Pet的8个Python脚本是纯Pillow图片处理，不依赖Codex，可直接复用。
已构建好的完整技能位于：
`<Hermes数据目录>\skills\hermes-hatch-pet\`

### 适配的三个层面（2026.7.30 已完成）

1. **生图层**：从 $imagegen 改为 `image_gen_adapter.py`，支持3种模式——
   - `t2i`: qwen-image-2.0-pro（文生图，chat/completions 端点）
   - `edit`: qwen-image-edit-plus（图片编辑，multimodal-generation 端点）
   - `ref`: wan2.7-image-pro（参考图生成，multimodal-generation 端点）
2. **编排层**：SKILL.md 从 Codex 格式改为 Hermes 技能格式
3. **质检层**：从 Codex 轻量 worker 改为 qa_adapter.py（结构质检 + Moonshot kimi-k2.6 视觉质检），详见 `references/hatch-pet-architecture.md` 的"适配层设计"章节

### 新增照片→桌宠辅助脚本

| 脚本 | 功能 |
|------|------|
| `prepare_photo_pet.py` | 接收一张照片，自动创建完整 imagegen-jobs.json（先 edit 模式 chibi 化，再 ref 模式逐行动画生成），含 README 操作指引 |

### 四个新适配脚本

| 脚本 | 功能 |
|------|------|
| `image_gen_adapter.py` | 读取 imagegen-jobs.json，按依赖顺序调用 qwen-image（t2i/edit/ref 三模式），输出到 decoded/；running-left 自动镜像推导 |
| `prepare_photo_pet.py` | 接收照片一步创建 imagegen-jobs.json（edit 模式 chibi 化 + ref 模式逐行动画生成） |
| `qa_adapter.py` | 结构质检（inspect_frames）+ 视觉质检（kimi-k2.6 vision API），输出 qa_report.json |
| `remove_bg.py` | 色键去除（默认）+ rembg AI抠图（可选），支持单文件/批量模式 |

### 关键接口：DashScope qwen-image-2.0-pro 返回格式

```python
# API返回的 message.content 中，图片URL在 {"image": "url"} 字段
content = data["choices"][0]["message"]["content"]
# content 是 list: [{"image": "https://..."}]
img_url = content[0]["image"]  # 注意字段名是 "image" 不是 "image_url"
```

**常见错误**: 从 OpenAI DALL-E 接口迁移的用户容易写成 `content[0]["image_url"]`，会 KeyError。字段就是 `"image"`。

### 端到端工作流

```
prepare_pet_run.py
  → image_gen_adapter.py (10个job: base + 8行生成 + 1行镜像)
  → extract_strip_frames.py (色键去除 + 帧提取)
  → compose_atlas.py (拼合1536x1872图集)
  → validate_atlas.py (验证)
  → qa_adapter.py (质检)
  → convert_to_dyberpet.py (可选：转换为DyberPet格式)
```

详见 `references/hatch-pet-architecture.md`

### DyberPet 格式输出

hermes-hatch-pet 的 `scripts/convert_to_dyberpet.py` 将提取后的帧转换为 DyberPet 格式包：

```bash
# 从 Hatch Pet 运行目录转换
python <hatch-pet>/scripts/convert_to_dyberpet.py --run-dir /path/to/run
```

输出到 `run-dir/dyberpet_pack/<pet_name>/`，含 pet_config.json + 57 帧 + icon.png + README。复制 `pet_name/` 文件夹到 DyberPet 的 `pets/` 目录即可安装。详见 `references/dyberpet-format.md`。

## 百度搜索技术（当web_search不可用时）

当需要在Python脚本中搜索中文内容时，用requests直连百度：
```python
session = requests.Session()
session.trust_env = False  # 关键：绕过系统代理
resp = session.get("https://www.baidu.com/s",
                  params={"wd": keyword, "rn": 10},
                  headers={"User-Agent": "Mozilla/5.0 ..."})
# 用正则提取 <h3> 标签中的链接和标题
results = re.findall(r'<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
```

关键点：`session.trust_env = False` 必须设置，否则会走系统代理导致SSL错误。

## 常见陷阱

### 陷阱1：qwen-image-edit-plus 最小尺寸 512px

API 参数 `size` 的宽和高都必须 >= 512px，否则返回 HTTP 400：
```
{"code":"InvalidParameter","message":"Width and height must be between 512 and 2048 pixels. Got width=576, height=384."}
```
母版如果是 384x576，需要先放大到 512x768 再发送。交付时再缩回目标尺寸。

### 陷阱2：tkinter Font 对象创建方式

`tk.Font(...)` 会报 `AttributeError: module 'tkinter' has no attribute 'Font'`。必须显式导入：
```python
from tkinter import font as tkfont
font_obj = tkfont.Font(family="Microsoft YaHei", size=12)
```

### 陷阱3：execute_code 沙箱字符串字面量损坏

execute_code 沙箱在处理包含 API key 变量名的字符串字面量时会损坏（字符串被截断导致 SyntaxError: unterminated string literal）。表现是代码中 `"DASHSCOPE_API_KEY=..."` 这类字符串被破坏。

**修复**：不用 execute_code 内嵌代码，改用 `write_file` 写 .py 脚本到磁盘，再用 `terminal` 运行。对于包含敏感变量名的代码这是唯一可靠方式。

### 陷阱4：DyberPet EXE 在中国大陆无法下载

GitHub 被墙时 DyberPet EXE 无法下载，所有 GitHub 镜像（ghproxy/gh-proxy/ghfast/mirror.ghproxy）实测均失败或超时，Gitee 无镜像。使用方案7（Python 自运行桌宠）替代。

### 陷阱5：GrabCut/rembg + 白色衣服 = 灾难 ⭐⭐

**问题**：GrabCut 在白色背景上处理穿白色衣服的人物时，会把白裙、白袜、白鞋也判定为背景删除。无论怎么调初始化矩形、边缘标记策略、迭代次数，GrabCut 的 GMM 颜色模型始终无法区分"白衣服的白"和"白背景的白"。**rembg (U2Net) 同样失败** -- 虽然 rembg 能处理头发，但白色衣物在白色背景上的分割精度不足（kneel 3/10, jump 4/10，白裙大面积破损/半透明）。

**实测方案对比**：6种白底方案全部失败，仅 flood fill strict 成功（详见上方"白底去除函数"章节的对比表）。rembg 的 `alpha_matting=True` 模式同样无效（填充率不变），GrabCut 从四角初始化背景也无法区分白裙与白背景。解决方案是改用绿幕背景生成 + rembg/色键抠图（详见上方"绿幕色键法"章节），或直接放弃原图用 AI 图生图重新生成（见"终极方案"）。

**规则**：人物穿白色衣物时：
1. **白底图**：禁止使用 GrabCut 和 rembg，改用 flood fill strict（threshold=245）
2. **flood fill 效果仍不理想**：重新用绿幕背景生成图，用 rembg 或色键+despill 抠图
3. **没有万能方案**：不同动作图的最佳抠图方法可能不同，需逐图验证

### 陷阱6：qwen-image-edit-plus 生成全身动作时裁切四肢

**问题**：prompt 不强调"full body visible"时，AI 生成的动作图会裁切手脚 -- 特别是 open_arms（单脚站立）和 jump（手被裁掉）。

**修复**：prompt 中必须包含 `IMPORTANT: full body must be completely visible including all hair, both hands, both feet, and the entire body within the frame. Do not crop any body parts.` 对于站姿动作还需加 `both feet firmly on the ground`。

**验证**：生成后用 vision_analyze 检查6项（头发/双手/白裙/双脚/白袜/整体），低于8分重新生成。

### 陷阱7：OpenCV 5.0 移除 CascadeClassifier（2026.7.31 发现）⭐

**问题**：OpenCV 5.0.0 移除了 `cv2.CascadeClassifier`，调用时报 `AttributeError: module 'cv2' has no attribute 'CascadeClassifier'`。同时 `cv2.data.haarcascades` 目录为空（只有 `__init__.py`），Haar 级联 XML 文件不再随包分发。

**影响**：无法用 Haar 级联检测人脸来做面部替换的自动定位。

**替代方案 -- alpha 通道边界框估算法**：不依赖人脸检测，而是通过 rembg 输出的 alpha 通道找到人物边界框，面部估算在顶部25%处。详见上方"面部替换后处理"章节的 `estimate_face_region()` 函数。

**如果确实需要 Haar 级联**：从 GitHub 下载 XML 文件（需代理）：
```python
import requests
session = requests.Session()
session.proxies = {"http": "http://127.0.0.1:<代理端口>", "https": "http://127.0.0.1:<代理端口>"}
url = "https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml"
resp = session.get(url, timeout=30)
```

**或用 OpenCV 5.0 新 API**：`cv2.FaceDetectorYN_create()` 替代 CascadeClassifier。

### 陷阱8：AI 不按 prompt 生成正确姿势（2026.7.31 发现）⭐⭐⭐

**问题**：qwen-image-edit-plus 经常不按 prompt 生成正确姿势 -- 如要求"kneel"时生成站立姿势，要求"jump"时也生成站立姿势。AI 倾向于生成默认的正面站立全身照。

**表现**：生成的图片看起来质量很好（人物完整、面部清晰），但姿势完全错误。如果不验证就直接使用，用户会看到所有动作动画都像是"站着不动"。

**根因**：AI 模型倾向复制参考图的构图。当参考图是正面站立图时，AI 会"懒惰"地也生成正面站立图，忽略 prompt 中的姿势描述。

**修复方案（按优先级排序）**：
1. **⭐ 相机角度技巧（最优方案）**：在 prompt 中指定与参考图不同的相机角度（如侧视、仰视、俯视），迫使 AI 重新构图。详见上方"相机角度技巧"章节。这是最可靠的方法 -- 构图约束改变了，AI 无法复制参考图的站立姿态。
2. **prompt 极端化**：不用"kneeling"而用"KOWTOW (FULL PROSTRATION)"+"forehead touching ground"。不用"jumping"而用"both feet OFF the ground"+"airborne"
3. **逐张验证**：生成后立即用 vision_analyze 检查姿势是否正确
4. **重试策略**：不通过时重新生成。连续2次失败时，检查是否相机角度描述不够明确

**验证清单**：
   | 动作 | 必须确认 | 错误信号 |
   |------|---------|---------|
   | kneel | 双膝着地、额头触地 | 站立 |
   | jump | 双脚离地、双臂高举 | 站立 |
   | bow | 上半身前倾45度 | 站直 |
   | cry | 双手捂脸 | 手放下 |
   | open_arms | 双臂水平伸展 | 手臂下垂 |

### 陷阱9：面部裁贴替换导致"两张脸"重影（2026.7.31 实测发现）⭐⭐⭐

**问题**：用 face_replace.py 从 master.png 裁剪面部区域，通过椭圆 alpha 遮罩混合到动作图上时，产生"两张脸"诡异效果。用户反馈"有些动作上面两张脸，太诡异了"。

**根因**：
1. master 面部是正面，贴到侧面/低头动作图（kneel、bow）上，透视角度不匹配
2. 光照/色调差异导致混合后有明显接缝
3. 面部区域估算（顶部25%）对侧面动作不准确

**修复**：废弃面部替换方案。用 master.png 做唯一参考 + 相机角度技巧在生成端保证面部一致性。不要做任何后处理面部裁贴。

**规则**：面部一致性靠生成端（prompt + 参考图）控制，不靠后处理裁贴。AI 生成的不完美面部远好于裁贴造成的"两张脸"。

### 陷阱10：双参考照片生成动作图导致面部失真（2026.7.31 实测发现）⭐

**问题**：将两张真实照片（半身照+全身照）同时传给 qwen-image-edit-plus 生成动作图时，AI 无法同时保持面部一致性 + 改变身体姿势。生成的面部"像换了一个人"。

**根因**：AI 需要同时处理面部理解、服装识别、姿势变换三个任务，能力不足。多张参考图输入时，AI 的注意力被分散。

**修复**：用 AI 已生成的 master 图（用户已确认面部）作为**唯一参考图**，而非原始照片。master 的面部/服装/风格已经统一，AI 只需改姿势。

## 参考

- `references/non-chibi-routes.md` - 三条非Q版路线详细操作步骤：豆包直出、真人抠图+DyberPet、半写实Hatch Pet
- `references/dyberpet-format.md` - DyberPet 精灵图集格式规范：目录结构、pet_config.json 配置、状态映射、帧命名规则、Hatch Pet 转换桥接（含时序映射表）
- `references/dashscope-image-api.md` - DashScope qwen-image-2.0-pro 文生图 API 完整调用方式、失败端点记录、视频模型清单、色键色域重叠陷阱
- `references/hatch-pet-architecture.md` - Hatch Pet源码完整分析：架构、8个脚本功能、精灵图集规格、适配层设计（image_gen_adapter/qa_adapter/remove_bg）、端到端运行结果、Moonshot vision 模型兼容性
- `references/desktop-pet-tools-landscape.md` - 桌面宠物工具生态调研详情
- `references/vision-api-compat.md` - 视觉 API 兼容性速查（kimi-k2.6/moonshot-v1-8k/qwen-vl-max）
- `scripts/qwen_image_gen.py` - DashScope qwen-image-2.0-pro 文生图可复用脚本（支持命令行和函数调用）
- `scripts/gen_all_t2i.py` - wanx2.1-t2i-turbo 异步文生图生成全部6张角色图（master+5动作）+ rembg 去背景，当原图抠图反复失败时使用此脚本从零生成。⚠️ 注意：纯文生图会导致面部失真，推荐改用 gen_all_img2img.py
- `scripts/gen_all_img2img.py` - qwen-image-edit-plus 图生图生成全部6张角色图，以真人照片为参考保持面部一致性 + rembg 去背景（2026.7.31 推荐方案）
- `scripts/gen_all_dualref.py` - qwen-image-edit-plus 双参考照片（半身+全身）图生图，最大化面部一致性 + rembg 去背景（2026.7.31 面部最优方案）
- `scripts/gen_actions_masterface.py` - 用 master 原始图作为唯一面部参考，生成全部5个动作图（2026.7.31，已被 v4 替代）
- `scripts/gen_actions_v4.py` - ⭐ 最终方案：master 唯一参考 + 不同相机角度生成5个动作图（2026.7.31 验证通过，5/5 姿势正确+面部一致+无两张脸）
- `scripts/face_replace.py` - ⚠️ 已废弃：面部裁贴替换产生"两张脸"重影，不再使用（2026.7.31 实测失败）
- `scripts/check_image_gen_backend.py` - 检查Hermes image_gen后端可用性的脚本
- `templates/doubao-pet-prompt.txt` - 豆包客户端桌面宠物万能指令（直接复制粘贴）
- `templates/dyberpet-minimal-config.json` - DyberPet 最少动画配置模板（仅idle+click，适合真人照片微动画）
- `templates/run_pet.py` - Python 自运行桌宠脚本 v3（双击切动作+单击换话术+18条话术+win32色键透明+右键缩放菜单+DyberPet帧格式兼容）
- `templates/character-profile-template.md` - 照片角色特征档案模板（多角度照片整合为结构化文档）
