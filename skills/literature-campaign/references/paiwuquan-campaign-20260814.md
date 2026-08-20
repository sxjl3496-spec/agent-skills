# 战役实例：省自科排污权课题（2026-08-14）

《税收数据驱动的排污权效率定价机制设计——基于ABM的湖南省政策仿真》申报书文献支撑战役。88条清单 → 84篇唯一 → 84篇解读（中文44+英文40）→ 综述V2 → 申报书V5草案。全程约3.5小时，13/13交付物通过。

## 任务分配表（可复用模板）

| 执行人 | 批次 | 篇数 |
|---|---|---|
| 丞相（leader） | ABM仿真+定价+湖南核心批次 | 17 |
| 太尉（Claude Code） | 环保税类（DID/准自然实验实证） | 12 |
| 大将军（Codex CLI） | 制度/协同/效率测度类 | 15 |
| 丞相（leader） | 英文经典理论（Montgomery/Weitzman/Hahn/Porter/Stavins/Gersbach/Schmalensee/Tesfatsion/Farmer/Salant） | 10 |
| 太尉 | 英文近5年SSCI实证（ETS/排污权） | 15 |
| 大将军 | 英文方法学经典实证（DDF/ABM/波特假说） | 15 |

## 关键发现与修正记录

### Crossref模糊检索错配（太尉+大将军独立发现，互证）
- Tang 2015碳配额拍卖ABM → 实际 DOI:10.1016/j.enpol.2016.11.041 = **Energy Policy 2017, 102: 30-40**（不是2015,84:155-165——那个DOI是Biomass文章）
- 同作者另有2015年ABM篇《Carbon emissions trading scheme exploration in China》（Energy Policy 2015, 81:152-169, DOI:10.1016/j.enpol.2015.02.032）
- Lange & Maniloff 2021 → 案例是**NOx Budget Program**（不是SO2 program）
- Greenstone 2012 JPE 正式版DOI在Crossref/OpenAlex均无记录（仅NBER WP 10.3386/w18392可核实）——引用时注明以NBER版核实
- Zhou 2021 Computational Economics → 实为**CGE模型**（非ABM），从ABM证据链中剔除，改引Tang 2017等真实ABM文献
- Montero 2008 → AER 98(1):496-518（非98(3):1037-1051）

### 期刊级别实测（CSSCI 2025-2026官方目录）
- **CSSCI扩展版**（易被误认为CSSCI来源）：科技管理研究、税务与经济、国际税收、工业技术经济、北京理工大学学报(社科版)、湖北社会科学、中国环境管理、环境经济研究、环境保护
- 科技管理研究按发表当年目录：2016/2017年发表时是CSSCI来源 → 标注"发表时CSSCI/现扩展版"
- 官方目录xlsx 5列结构：`序号|期刊|空|序号|期刊`，row[1]=来源、row[4]=扩展版；解析错列会得到"CSSCI仅1种、扩展版661"的荒谬结果

### 中文DOI验证
- Crossref查中文DOI（10.13653/j.cnki.jqte...等）全部404 → 中文DOI注册在chndoi.org
- doi.org HEAD请求全部302重定向（chndoi.org/万方）= 文献真实存在（10/10通过）

## 双agent审核闭环（价值实证）

太尉审核发现6处Crossref可核实错误+4处一致性问题；大将军独立勘误3处（与太尉互证）。全部修正后综述V2的41条引用经DOI验证通过。**结论：双agent独立审核对元数据红线的守护价值显著——单agent模糊检索+自报完成极易漏过这些可反查错误。**

## 交付物清单（13项）

知识库（ObsidianVault/academia/排污权课题/）：文献总表、解读模板、文献解读文档、文献综述V2、申报书V5草案、出口检验报告
工作目录（hermes-data/output/申报书/）：7份解读文件（含leader补写版）、2份审核报告

## 教训

1. 英文文献检索勿用OpenAlex泛搜索（噪声）——Crossref期刊定向一次到位
2. 任务派活时清单里的占位题名（如"近5年中国ETS创新"）必须事后用Crossref按DOI反查真实题名——本次太尉查出5处题名不符
3. teammate卡死（active_turn_slow）时leader补写兜底，事后对比择优，不让单点阻塞战役
4. 综述"引用原则"声明要与参考文献表自洽（非CSSCI要么删出表、要么在头部豁免声明）
