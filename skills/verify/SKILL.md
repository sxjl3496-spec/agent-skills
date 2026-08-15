---
name: verify
description: >
  通用验证技能。当用户需要验证交付物质量、检查文档完整性、审查代码质量时触发。
  将 plan 技能中的 cross_model_verify 提取为独立能力，非 plan 任务也能调用。
  触发词：验证、verify、检查质量、审查、validate、质检。
---

# 通用验证 (verify)

## 何时使用

- 完成非 plan 任务后想验证交付物质量
- 用户要求"检查一下"或"验证一下"
- 代码写完后想要跨模型审查
- 文档写完后想要完整性检查

## 铁律：证据先行（Evidence Before Claims）⭐

**来源**：Superpowers verification-before-completion（obra/superpowers ★266K，2026-08-05 借鉴引入）

**核心原则**：声称"完成/修复/通过/正确"之前，必须先在本回合内实际运行验证命令并确认输出。

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**Gate Function（完成声明门禁）**——声称任何状态或表达满意之前：

1. 本消息内运行了验证命令（read_file / 运行代码 / 测试 / curl）
2. 看到了实际输出（不是推测输出）
3. 输出确认了声称的状态

**违规表现**：
- "应该没问题"、"我认为通过了"、"之前测试过应该还好"
- 声称完成但没有附上任何验证命令输出
- 用昨天的测试结果声称今天的代码通过

**正确做法**：
- ❌ "代码写完了，应该能运行"
- ✅ "代码写完了，验证输出：`python test.py` 返回 PASS，3个用例全过"

**例外**（需向用户说明）：一次性原型、生成代码、纯格式转换等明确不需要验证的场景。

## 对抗性怀疑审查（Doubt Review）⭐

**来源**：addyosmani/agent-skills 的 doubt-driven-development（★81.6K，2026-08-05 借鉴引入）

**核心原则**：**自信的答案 ≠ 正确的答案**。长会话会积累上下文，把假设悄悄变成"事实"。非平凡交付物定稿前，物化一个"新鲜上下文审查者"——偏向**证伪**而非批准。

**与证据先行的区别**：证据先行是"验证命令跑了吗"（事后证明），Doubt Review 是"这个决策对吗"（事中对抗）。

**非平凡判定**（满足任一即触发）：
- 引入或修改分支逻辑
- 跨越模块/服务边界
- 断言类型系统无法验证的属性（线程安全、幂等、顺序、不变量）
- 正确性依赖未来读者看不到的上下文
- 爆炸半径不可逆（生产部署、数据迁移、公共API变更）

**Doubt Review 流程（5步）**：
```
Step 1 CLAIM   写下主张+为什么重要
Step 2 EXTRACT 隔离工件+契约，剥离推理过程
Step 3 DOUBT   用对抗性提示问"这个哪里可能错？"（不找证据支持）
Step 4 RECONCILE 逐条分类发现（真问题/误报/改进点）
Step 5 STOP    停止条件：琐碎发现、3轮、或用户覆盖
```

**执行方式**：在 cross_model_verify 的 prompt 中显式要求对抗视角：
```
"你是对抗性审查者，任务是证伪以下交付物。逐条找它错在哪里：
1. 边界情况遗漏
2. 隐含假设错误
3. 环境/版本依赖风险
4. 与需求矛盾的逻辑
不要给改进建议，先找出所有可能的问题。"
```

**停止条件**：3轮对抗审查后仍只有琐碎发现 → 接受当前版本。

## 源码溯源纪律（Source-Cited Code）⭐

**来源**：addyosmani/agent-skills 的 source-driven-development（★81.6K，2026-08-05 借鉴引入）

**核心原则**：**每个框架特定代码决策必须由官方文档支撑**。不从记忆实现——验证、引用、让用户看到来源。训练数据会过时，API会废弃，最佳实践会演变。

**适用**：
- 构建框架特定代码（React/Vue/Django等）
- 样板代码/起始代码/会被复制的模式
- 框架推荐做法重要的功能（表单、路由、数据获取、状态管理、认证）
- 审查使用框架特定模式的代码

**不适用**：不依赖特定版本的纯逻辑（重命名、修拼写、移动文件）、用户明确要求速度优先

**流程**：DETECT（读依赖文件识别版本：package.json/go.mod/requirements.txt）→ FETCH（获取官方文档）→ IMPLEMENT（遵循文档化模式）→ CITE（展示来源URL）

**落地**：验证框架代码时，检查交付物是否引用了官方文档来源；无来源的框架代码标记为存疑。

## 前端反模式检测（Impeccable CLI 集成）⭐

**来源**：DevvGwardo/impeccable（Hermes原生移植，pbakaus/impeccable Apache 2.0，2026-08-05 集成）

**适用场景**：前端交付物（HTML/CSS/JSX/TSX/Vue/Svelte）完成或修改后，除了硬验证和跨模型验证，**增加反模式扫描**。

**检测命令**（任选其一，需 Node.js 18+）：

```bash
# 方式1：npx 直接运行（首次会下载包，约30-60秒）
npx --yes impeccable detect src/                    # 扫描目录
npx --yes impeccable detect index.html              # 扫描单文件
npx --yes impeccable detect --fast --json .         # 纯正则+JSON输出

# 方式2：本地缓存路径（更快，包已下载过）
cd "C:/Users/<用户名>/AppData/Local/npm-cache/_npx/<hash>/node_modules/impeccable"
node cli/bin/cli.js detect <目标>
```

**注意**：impeccable CLI 的路径参数必须是 **Windows 路径**（`C:\...`），不能是 MSYS 路径（`/c/...` 或 `/tmp/...`），否则报 "cannot access"。

**退出码**：0 = 无问题，2 = 发现问题（`--json` 可机器解析）

**扫描内容**：25+ AI 反模式，包括：
- side-tab（侧边条彩色边框）—— AI生成UI的最显著标志
- cramped-padding（内边距过小）
- ai-color-palette（紫色/青色渐变）
- gradient-text、glassmorphism-as-default、hero-metric-template
- identical-card-grids、modal-as-first-thought

**处理方式**：
1. 检测到反模式 → 在验证报告中列出（反模式名 + 位置 + 修复建议）
2. 逐项修复后重新检测，直到退出码0
3. 检测结果作为前端交付物"证据先行"的一部分

**示例输出**：
```
C:\...\bad.html
  [side-tab] border-left: 3px → Thick colored border on one side...
  [ai-color-palette] Purple/violet accent colors detected
3 anti-patterns found.
```

## 技能评测循环（Evals-Driven Skills）⭐

**来源**：AminBlg/SimpleEnglish（★1,611，MIT，2026-08-05 借鉴引入）

**背景**：SimpleEnglish 仓库自带 `evals/pressure-tests.md`（压力测试）和 `evals/results/RESULTS.md`（评测结果记录）——开源技能"有评测、有结果"的范例。Hermes 技能大多无评测，质量靠使用中迭代。

**适用场景**：新建技能、大改技能、或技能多次被纠正后。

**执行**（3步）：
1. **写压力测试**：为该技能设计 3-5 个"压力场景"prompt（边界情况、易错场景、用户高频误用）
2. **跑测试**：用测试 prompt 实际调用技能，记录输出
3. **记结果**：结果写入 `evals/RESULTS.md`（场景、输出摘要、通过/失败、改进点）

**示例**（simple-english 的测试思路）：
- 输入一篇"AI味浓"的中文技术文档 → 输出是否 STE 合规
- 输入含大量同义词轮换的文本 → 是否压缩为一词一义
- 输入超长句（>25词）→ 是否拆分

**价值**：
- 技能质量可量化、可回归（改技能后重跑评测）
- 开源分享时附评测结果 → 增强可信度（用户开源知识库受益）
- 防止"技能越改越差"（无评测时的常见问题）

---

## 验证流程

### 1. 硬验证（先执行）

根据交付物类型选择验证方式：

| 交付物类型 | 验证方式 | 通过标准 |
|-----------|---------|---------|
| 代码/脚本 | 实际运行 | 无报错，输出符合预期 |
| 文件 | read_file 读回 | 文件存在，内容完整，格式正确 |
| 配置 | 解析验证 | 语法正确，字段完整 |
| 文档 | 完整性检查 | 覆盖所有要求的章节 |
| 数据分析 | 结果可复现 | 数据准确，结论有支撑 |

### 2. 跨模型验证（execute_code + cross_model_verify）

```python
import sys
sys.path.insert(0, r"<Hermes数据目录>\skills\plan\scripts")
from cross_model_verify import cross_model_verify

# 读取交付物内容
content = open("交付物路径").read()

result = cross_model_verify(
    prompt="[验证指令：列出要检查的维度和验收标准]",
    content=content,
    api="dashscope",        # 推荐
    model="qwen3.7-flash",  # 默认，快且便宜
)
if result["success"]:
    print(result["content"])
else:
    print(f"验证失败: {result['error']}")
```

可用 API：
- dashscope: qwen3.7-flash（推荐）、qwen3.7-max
- deepseek: deepseek-chat
- moonshot: moonshot-v1-8k

### 3. 生成验证报告

```markdown
## 验证报告

### 硬验证
- [x] 文件存在
- [x] 语法正确
- [x] 内容完整

### 跨模型验证（qwen3.7-flash）
- 评分：X/10
- 发现问题：[列表]
- 修复状态：[已修复/待修复]

### 结论
✅ 验证通过 / ❌ 需修复N项
```

## 注意事项

- content 参数控制在 4000 字符以内，超出时拆分多次调用
- 代码类交付物优先用关键函数片段，不传整个文件
- 如果 API 调用失败，换一个 API 重试，不要跳过验证
- 跨模型验证是参考，不是最终结论 -- 仍需硬验证确认

## 参考

- `<Hermes数据目录>\skills\plan\scripts\cross_model_verify.py`
- plan 技能的阶段4验证流程
