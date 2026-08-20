# 每日CSSCI文献自动下载 — cron job 完整配置

创建于 2026-08-06，2026-08-07 更新（少帅指定变更：调度 10:00→01:00、下载量 18→10）。少帅要求：每天自动下载 10 篇 CSSCI 文献，直到喊"暂停"为止。

## Job 配置

| 项 | 值 |
|----|-----|
| 名称 | 每日CSSCI文献自动下载 |
| job_id | `72bf13a254cb` |
| 调度 | `0 1 * * *`（每天**01:00**——⚠️ 少帅指定，该时段API最便宜；勿改回10:00，曾误改被纠正） |
| 下载量 | `pw_download.py --max 10`（⚠️ 从18改10是少帅指定，预留8篇额度给手动下载补充文献） |
| repeat | forever |
| deliver | origin（当前会话） |
| enabled_toolsets | `["terminal", "file", "vision"]` |
| 类型 | LLM 驱动（非 no_agent）——因为登录可能需要 vision_analyze 识别验证码 |

## 为什么是 LLM 驱动而非纯脚本

登录环节需要验证码识别（vision_analyze）。纯脚本无法识别验证码，因此 cron 用 agent 模式：
agent 先跑 diag_page.py 判断状态，未登录时截图验证码 → vision_analyze 识别 → 跑 pw_login_full.py。

## 完整 prompt（重建任务时直接复用）

```
每日自动从文献云平台下载CSSCI中文文献（碳交易/碳市场主题），每天下载10篇，直到少帅喊暂停为止。

## 背景
少帅（冯泽宇，吉首大学）正在为湖南省自科基金申报补充中文文献。已通过文献云平台（wxy88.top）成功下载CSSCI论文到 D:\BaiduSyncdisk\AIKnowledgeBase\ObsidianVault\academia\文献库\碳排放权交易\。现在需要每天自动继续下载（每日限额约18-20篇，**每天只下载10篇，预留8篇额度给少帅手动下载补充文献**），直到少帅喊暂停。下载完成后自动将新文献增量接入《市场化环境治理研究文献矩阵库》。

## 今日任务步骤

### 1. 检查登录状态
先运行诊断脚本确认是否已登录、是否额度可用：
python "D:/BaiduSyncdisk/AIKnowledgeBase/Hermesagent/hermes-data/scripts/diag_page.py"
- 如果输出"您今天的下载次数已用尽, 请明天再来"→ 今日额度已用尽，直接结束任务，向少帅汇报"今日额度已用尽，明天继续"。
- 如果显示"已登录镜像"→ 跳到步骤3。
- 如果显示"未登录"→ 执行步骤2重新登录。

### 2. 重新登录（cookie过期时）
1. 写一个临时playwright脚本：打开 http://www.wxy88.top/ ，截图验证码元素（img[src*='ShowKey']）保存到 TEMP 目录
2. 用 vision_analyze 识别验证码（提示"只输出验证码字符，字母都是小写"）
3. 用识别结果运行 pw_login_full.py <验证码>，成功后会保存 pw_cookies.json
2. 确认登录成功（输出"已登录"），然后进入步骤3。

### 3. 运行批量下载（每日限额内只下载10篇）
python "D:/BaiduSyncdisk/AIKnowledgeBase/Hermesagent/hermes-data/scripts/pw_download.py" --max 10
脚本特性（无需额外配置）：
- CSSCI期刊过滤（非CSSCI自动跳过）
- 限速规则写死（3秒/篇、20篇/分、50篇/3分）
- 断点续传（已下载的自动跳过）
- 每日额度用尽自动停止
- 下载到 D:\BaiduSyncdisk\AIKnowledgeBase\ObsidianVault\academia\文献库\碳排放权交易\

### 4. 验证与更新清单
1. 检查下载数量：ls "D:/BaiduSyncdisk/AIKnowledgeBase/ObsidianVault/academia/文献库/碳排放权交易/"*.pdf | wc -l
2. 如果有新下载，重新生成GB/T 7714清单：python "D:/BaiduSyncdisk/AIKnowledgeBase/Hermesagent/hermes-data/scripts/gen_list.py"
3. 验证PDF有效性（文件头 %PDF）

### 5. 向少帅汇报
汇报内容：今日新增X篇、累计Y篇、下载了哪些期刊的论文、是否触发额度。用中文，称呼"少帅"。

## 重要规则
- 限速规则不可绕过：3秒/篇、20篇/分、50篇/3分
- 只下载CSSCI期刊（173本名单）
- 每日限额约18-20篇，达到后自动停止，不硬撑
- 如果连续失败3次以上，停止并汇报异常
- 账号密码在 D:\BaiduSyncdisk\知网查文献.txt（用户名418710404），不要写入任何交付物
- 本任务持续到少帅喊"暂停"为止
```

## 管理操作

- 暂停/停止：`cronjob action=list` → 找到 job_id → `cronjob action=pause`（暂停）或 `action=remove`（删除）
- 查看下次运行：`cronjob action=list`
- 手动触发一次：`cronjob action=run job_id=72bf13a254cb`
