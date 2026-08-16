---
title: gh-fix-ci解读
tags: [AI技能, GitHub, CI修复, Composio]
created: 2026-08-05
source: https://github.com/composio-community/awesome-codex-skills/tree/main/gh-fix-ci
---

# gh-fix-ci 解读

## 基本信息

- **来源**：Composio 社区 `composio-community/awesome-codex-skills`（★15.5K）
- **官方描述**：Inspect GitHub PR checks with gh, pull failing GitHub Actions logs, summarize failure context, then create a fix plan and implement after user approval
- **排行**：第6名
- **定位**：CI 挂了自动拉日志、定位、给修复方案

## 核心机制

用 gh CLI 定位失败 PR checks → 拉取 GitHub Actions 日志 → 摘要失败上下文 → 提出修复计划 → 用户批准后实施。

**依赖 plan 技能**：草拟和批准修复计划时使用 plan 技能（技能间协作的典范）。

## 工作流（8步）

1. **验证 gh 认证**
   - `gh auth status`（需要 workflow/repo scopes 提升权限）
   - 沙箱阻止 → 用 `sandbox_permissions=require_escalated` 重跑
   - 未认证 → 让用户先登录

2. **解析 PR**
   - 默认当前分支 PR：`gh pr view --json number,url`
   - 用户提供 PR 号/URL 则直接用

3. **检查失败 checks（仅 GitHub Actions）**
   - 首选内置脚本：`python scripts/inspect_pr_checks.py --repo "." --pr "<number>"`（处理 gh 字段漂移和 job-log 回退）
   - 手动回退：
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
     - 每个失败 check 从 detailsUrl 提取 run id：`gh run view <run_id> --json ...`
     - `gh run view <run_id> --log`
     - 日志仍在进行中 → 直接拉 job 日志：`gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs"`

4. **界定非 GitHub Actions checks**
   - detailsUrl 不是 GitHub Actions run → 标记为外部，只报告 URL
   - 不尝试 Buildkite 等其他 provider（保持工作流精简）

5. **为用户摘要失败**
   - 失败 check 名、run URL（如有）、简洁日志片段
   - 明确标注缺失的日志

6. **创建计划**：用 plan 技能草拟简洁计划并请求批准

7. **批准后实施**：应用已批准的计划，摘要 diffs/测试，询问是否开 PR

8. **复查状态**：变更后建议重跑相关测试和 `gh pr checks` 确认

## 附属脚本：inspect_pr_checks.py

- 拉取失败 PR checks、GitHub Actions 日志、提取失败片段
- 仍有失败时非零退出码（可用于自动化）
- 用法：`python inspect_pr_checks.py --repo "." --pr "123"` 或 `--json` 输出

## 与仓库现有技能对比

**本库无对应技能**。完全新增的 CI 修复能力。
相关但不同：
- debug-helper：通用调试（错误分类、日志分析、API诊断），非 GitHub 专用
- plan：修复计划草拟（gh-fix-ci 明确依赖它）

## 可借鉴的提升点

1. **技能间协作模式**：gh-fix-ci 依赖 plan 技能——技能显式引用其他技能的成熟协作范例
2. **脚本化诊断**：把 gh 命令封装成 Python 脚本（处理字段漂移、日志回退），agent 直接调用
3. **范围纪律**：非 GitHub Actions 的 check 不处理，保持工作流精简
4. **自动化友好**：非零退出码让脚本可集成 CI 管道

## 使用注意

- 实战需要 gh CLI 已认证（`gh auth login`）
