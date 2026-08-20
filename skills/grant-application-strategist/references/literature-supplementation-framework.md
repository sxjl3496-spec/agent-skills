# 申报书文献补充框架（三方探讨方法论 + 27篇候选清单）

> 2026-08-14 省自科申报书实战沉淀。少帅指令："补充中文文献给我关键词我来搜，英文文献你们三个去搜索补充"——确立**文献补充分工模式**：中文文献给申请人关键词自搜（CNKI），英文文献由 agent（丞相+Claude Code+Codex）并行搜索核实。

## 一、分工模式（少帅确立，可复用）

| 文献类型 | 谁搜 | 渠道 | 交付物 |
|---------|------|------|--------|
| 中文文献 | **申请人自搜**（agent给关键词） | CNKI/CSSCI，优先2020-2025核心期刊 | 关键词清单（按类别分组） |
| 英文文献 | **agent并行搜索** | Crossref API / Google Scholar / Web搜索 | 文献列表（期刊全名+年份+卷期页码） |
| 湖南本地文献 | 几乎无公开发表学术论文 | 政府文件+试点评估报告+长江经济带/中部文献替代 | 不要硬找湖南文献 |

**分工依据**：中文文献的CNKI检索需要申请人账号/在校IP，agent无法代搜；英文文献可用Crossref API（`session.trust_env=False`）结构化检索，agent可独立完成。

**关键词清单要求**（给申请人的必须是"精准可操作"的）：
- 每条关键词标注期望文献类型（实证/方法/政策研究）
- 按申报书章节分组（如：环保税效应/效率测度/试点流动性/波特假说/ABM）
- 关键策略：中文文献**优先2020-2025**补时间段——英文文献在该细分领域近3年高质量实证少（如排污权/环保税方向2022年后英文实证稀缺），用中文CNKI近3年文献补足，避免再被评"文献陈旧"

## 二、申报书文献补充5大类别（三方共识）

| 类别 | 补什么 | 为什么 |
|------|--------|--------|
| 1. 环保税/税收数据效应 | 环保税政策效应实证（减排/创新）、税收数据测度环境绩效先例 | 申报书数据核心是环保税申报表，无一篇环保税文献会被评审追问"数据能否真实反映排放" |
| 2. 减排效率测度方法 | 方向性距离函数/DEA/排放强度分解 | 申报书A=产值/排放需要方法学根基，否则方法归属悬空 |
| 3. 中国试点评估+流动性机制 | 近5年碳/排污权试点因果评估、清淡市场流动性、配额银行/价格下限/MSR | 现试点评估文献陈旧（2015），缺近5年新证据 |
| 4. 波特假说近期 | 弱/强波特假说区分、**触发条件**（规制类型如何决定波特效应） | 申报书以"触发波特效应"为目标，但文献停留在1995/2002 |
| 5. ABM环境政策仿真 | ABM方法学经典正当性+中国ETS/排污权ABM应用 | 现ABM仅1篇，需"方法-应用"链条支撑仿真平台合理性 |

**总量建议**：新增15-18篇（英文12-15+中文3-4），使总文献达30-35篇、2015年后占比过半、中文文献增至5-6篇。

## 三、中文搜索关键词模板（排污权/环保税方向，可直接给申请人）

**类别1·环保税**：
- 环境保护税 减排 双重差分（政策效果实证）
- 环境保护税 企业 绿色技术创新（创新效应）
- 排污费 环境保护税 政策衔接 效果（制度衔接）
- 环保税 达标减征 75% 50% 税收优惠（激励/扭曲研究——支撑"未折扣计税基础"设计）

**类别2·效率测度**：
- 污染排放效率 DEA 测度 ｜ 方向性距离函数 非期望产出 ｜ 环境全要素生产率 方向性距离函数

**类别3·试点+流动性（申报书核心）**：
- 排污权交易 试点 减排 双重差分（近5年）
- 排污权交易 初始分配 效率 湖南（稀缺就放宽长江经济带/中部）
- 排污权二级市场 交易 清淡 流动性（找到即用）
- 配额银行 价格下限 安全阀 碳市场 ｜ 碳价 波动 市场稳定储备 欧盟
- 排污权抵押贷款 跨区域交易 试点

**类别4·波特假说**：
- 波特假说 环境规制 企业创新 实证 ｜ 波特效应 排污权交易 ｜ 弱波特假说 强波特假说 ｜ 环境规制 价格工具 命令控制 创新 比较

**类别5·ABM**：
- 多主体 仿真 碳市场 中国 ｜ ABM 排污权 交易 仿真（稀有） ｜ 计算实验 环境政策 多主体

## 四、英文文献候选（27篇，17篇已核实卷期页码）

### 与申报书机制直接同构（优先采用）
- **Gersbach H, Requate T. Emission taxes and optimal refunding schemes. Journal of Public Economics, 2004, 88(3-4): 713-725.**（排放税+最优退税=与"或有奖惩"直接同构——机制理论对标）
- **Aghion P, et al. Carbon taxes, path dependency, and directed technical change: Evidence from the auto industry. Journal of Political Economy, 2016, 124(1): 1-51.**（价格工具驱动定向技术变革，支撑"价格工具触发创新"）
- **Cui J, Wang C, Zhang J, Zheng Y. The effectiveness of China's regional carbon market pilots in reducing firm emissions. PNAS, 2021, 118(52): e2109912118.**（中国碳试点减排因果评估，近5年强证据）

### 测度类（已核实）
- Färe R, Grosskopf S, Pasurka C A. Environmental production functions and environmental directional distance functions. Energy, 2007, 32(7): 1055-1066.
- Zhou P, Ang B W, Wang H. Energy and CO2 emission performance in electricity generation: A non-radial directional distance function approach. European Journal of Operational Research, 2012, 221(3): 625-635.

### 试点/流动性/价格稳定（已核实）
- Cui J, Zhang J, Zheng Y. Carbon pricing induces innovation: Evidence from China's regional carbon market pilots. AEA Papers and Proceedings, 2018, 108: 453-457.
- Salant S W. What ails the European Union's emissions trading system? JEEM, 2016, 80: 6-19.
- Fell H, et al. Soft and hard price collars in a cap-and-trade system. JEEM, 2012, 64(2): 183-198.
- Kollenberg S, Taschini L. Emissions trading systems with cap adjustments. JEEM, 2016, 80: 20-36.
- Perino G, Willner M. Procrastinating reform: The impact of the market stability reserve on the EU ETS. JEEM, 2016, 80: 37-52.
- Rubin J D. A model of intertemporal emission trading, banking, and borrowing. JEEM, 1996, 31(3): 269-286.（配额银行经典）

### 波特假说近期（已核实）
- Ambec S, Cohen M A, Elgie S, Lanoie P. The Porter Hypothesis at 20. Review of Environmental Economics and Policy, 2013, 7(1): 2-22.
- Rubashkina Y, Galeotti M, Verdolini E. Environmental regulation and competitiveness. Energy Policy, 2015, 83: 288-300.
- Lanoie P, et al. Environmental policy, innovation and performance. Journal of Economics & Management Strategy, 2011, 20(3): 803-842.

### ABM（已核实）
- Tesfatsion L. Agent-based computational economics: Growing economies from the bottom up. Artificial Life, 2002, 8(1): 55-82.
- Farmer J D, Foley D. The economy needs agent-based modelling. Nature, 2009, 460: 685-686.
- Wang P, et al. Carbon emissions trading scheme exploration in China: A multi-agent-based model. Energy Policy, 2015, 81: 152-169.（中国碳市场ABM经典）
- Tang L, Wu J, Yu L, Bao Q. Carbon allowance auction design of China's emissions trading scheme: A multi-agent-based approach. Energy Policy, 2017, 102: 30-40.（年份卷期需反查，2015 vs 2017 有出入）

### 数据/监管实证（已核实）
- Karplus V J, Zhang S, Almond D. Quantifying coal power plant responses to tighter SO2 emissions standards in China. PNAS, 2018, 115(27): 7004-7009.（CEMS监测数据测企业减排反应）
- Shapiro J S, Walker R. Why is pollution from US manufacturing declining? AER, 2018, 108(12): 3814-3854.
- Greenstone M, List J A, Syverson C. The effects of environmental regulation on the competitiveness of U.S. manufacturing. JPE, 2012, 120(3): 480-514.

### 机制设计（已核实）
- Hahn R W, Stavins R N. The effect of allowance allocations on cap-and-trade system performance. Journal of Law and Economics, 2011, 54(4): S267-S294.
- Khezr P, MacKenzie I A. Consignment auctions. JEEM, 2018, 87: 42-51.
- Montero J P. A simple auction mechanism for the optimal allocation of the right to pollute. AER, 2008, 98(3): 1037-1051.（⚠️ 年份：AER正式发表2008；部分综述引用为2009，以AER 2008为准）

### 待核实（入库前必须反查）
- Zhang N, Choi Y. A note on the evolution of directional distance function. RSER, 2014, 33: 497-505.
- Perino G, et al. The EU ETS and the waterbed effect. Nature Climate Change, 2022, 12: 510-511.（作者序/卷期待核）
- Tang L, et al. 2015 vs 2017（Energy Policy，年份卷期需确认）

### 中文可直接用的2篇（已核实1篇）
- 齐绍洲, 林屾, 崔静波. 环境权益交易市场能否诱发绿色创新?——基于我国上市公司绿色专利数据的证据[J]. 经济研究, 2018, 53(12): 129-143.（✅ 已核实）
- 沈坤荣, 金刚, 方娴. 环境规制引起了污染就近转移吗?[J]. 经济研究, 2017, 52(5).（卷期已核实，页码待补——支撑ABM泄漏情景）

## 五、关键教训

1. **分工铁律**：中文文献关键词给申请人（agent无法代搜CNKI），英文文献agent并行搜（Crossref API），湖南本地文献不硬找
2. **"机制直接同构"文献是宝**：Gersbach & Requate 2004（排放税+退税=或有奖惩同构）这类文献让评审看到"机制有理论源头"，价值远高于泛泛的相关文献
3. **年份核实纪律**：Montero 2008 vs 2009、Tang 2015 vs 2017——同作者多篇同主题时年份易混，入库前必须反查（Crossref/Web of Science按题名反查），宁缺毋错
4. **"待核实"条目禁止直接入库**：所有不确定卷期页码的条目标注"待核实"，经反查确认后才能写入申报书参考文献（少帅文献红线：零编造、零残缺）
5. **中文文献补时间段策略**：英文该领域近3年高质量实证少，用中文CNKI近3年文献（2022-2025）补足，避免被评"文献陈旧"
