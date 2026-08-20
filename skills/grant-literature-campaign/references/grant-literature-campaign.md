# 省自科排污权课题文献战役实例（2026.8.14）

## 资产位置（少帅环境）

- 中文文献清单：`ObsidianVault/academia/排污权课题/排污权科研申报书中文文献清单.txt`（88条，编号[1]-[80]+[91]-[98]，含摘要/DOI/非CSSCI标注）
- PDF库：`ObsidianVault/academia/文献库/排污权交易/`（约75篇PDF + _paiwu_ingested.json 摄入记录）
- 英文文献清单（**无PDF**）：`Hermesagent/hermes-data/output/申报书/文献探讨_ClaudeCode.md`（27篇，17篇已核实，3篇待核实；Codex 版本同名文件）
- 申报书定稿：`ObsidianVault/academia/排污权课题/申报书_税收数据驱动的排污权效率定价_V4_20260813.md`
- 相关资产：`文献库/市场化环境治理研究文献矩阵库.md`（碳排放58+排污权12条交叉归类）、`文献库/_非CSSCI待清理/`（3篇碳交易非CSSCI）

## 重复模式（本课题实测）

- 清单内部4对：宋德勇[55]=[78]、孙晓华[57]=[79]、斯丽娟[58]=[91]、王振兴[61]=[80]——编号跳跃段藏重复
- PDF目录 `(1)` 后缀重复文件（如 王振兴 (1).pdf / 王振兴.pdf、斯丽娟 (1).pdf）
- 清单外PDF 3篇：邓海峰（排污权抵押，北核）、车秀珍（深圳抵押贷款）、吴朝霞&冯泽宇（**申请人自己论文→作研究基础，不列为引用**）

## 分类方案（7类，按申报书机制要素）

排污权交易制度与政策评估 / 排污权定价机制与市场运行 / ABM多主体仿真 / 环境保护税 / 排放效率测度(SBM·DDF·ML指数) / 协同治理与碳市场衔接 / 英文文献

## 相关度优先序（ABM课题视角）

机制设计（双费率定价/或有奖惩）> ABM仿真方法（Netlogo/强化学习/演化博弈）> 税收数据（环保税）> 湖南地方实践 > 政策评估DID > 泛效率测度。重点批次：仇蕾2016（Multi-agent排污权仿真）、张凯2022（水排污权演化博弈仿真）、赵爱武2018（政策组合计算实验）、连旭2024（强化学习多智能体）、欧中浩/黄懿（湖南实践）。

## 英文文献（已核实关键篇目，供同类课题复用）

- 机制同构：Gersbach & Requate 2004 (JPubE) 排放税+最优退税=与"或有奖惩"同构；Aghion et al. 2016 (JPE) 碳税驱动定向技术变革；Cui et al. 2021 (PNAS) 中国碳试点减排因果评估
- 测度：Färe et al. 2007 (Energy)、Zhou et al. 2012 (EJOR)
- 流动性/机制：Salant 2016 (JEEM)、Kollenberg & Taschini 2016 (JEEM)、Fell et al. 2012 (JEEM)
- 波特：Ambec et al. 2013 (REEP)、Rubashkina et al. 2015 (Energy Policy)、Lanoie et al. 2011 (JEMS)
- ABM方法学：Tesfatsion 2002 (Artificial Life)、Farmer & Foley 2009 (Nature)、Tang et al. 2015 (Energy Policy)
- **待核实3篇**：Zhang & Choi 2014 (RSER)、Perino et al. 2022 (Nature Climate Change)、Tang et al. 2015 卷期页码

## 解读模板9维度（本战役定稿）

研究背景 / 研究问题 / 方法 / 数据 / 主要发现 / 局限 / 与本课题相关性评分(1-5) / 可引用点 / 期刊级别

## 任务分配（本次战役方案）

- lead（丞相）亲办：步骤1/2（去重分类标注）、核心批次精读（ABM+定价+湖南≈14篇）、英文文献、汇总、综述撰写、终审
- Claude Code（太尉，opus）：环保税类≈25篇解读 + 双agent审核之一
- Codex（大将军）：效率测度+其余≈30篇解读 + 双agent审核之一
- delegate_task 子agent：先测可用性（v0.20 曾报 bug 未修），不可用则由上表覆盖
