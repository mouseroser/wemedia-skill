# CRON-MATRIX.md

> 定时任务总表（模型 / 执行方式 / 通知链路 / 风险等级）
> 维护者：main
> 更新时间：2026-03-15

## 规则

### 模型使用分层
- **minimax**：只用于“单脚本 / 单动作 / 少判断”任务
- **sonnet / opus**：用于多步工具调用、复杂判断、NotebookLM 维护、记忆整理

### 风险分级
- **低**：单脚本、无复杂分支
- **中**：脚本 + 简单汇报
- **高**：多步工具调用、清理/删除、NotebookLM source 维护

---

## 当前 Cron 总表

| 名称 | Job ID | 模型 | 执行方式 | 通知 | 风险 | 备注 |
|------|--------|------|----------|------|------|------|
| post-upgrade-guard | `9ec9bae9` | minimax | 单脚本 | 静默，异常才通知 | 低 | 只看 RESULT |
| layer2-health-check | `ff027bc7` | minimax | 单脚本 | 监控群摘要 | 低 | 已简化 |
| todo-daily-check | `aa381c31` | minimax | 单脚本 | 监控群摘要 | 低 | 已简化 |
| layer1-compress-check | `8adbf556` | minimax | 单脚本 | 监控群摘要 | 低 | 已简化 |
| openclaw-runtime-audit | `02f73862` | minimax | 单脚本 | 无 | 低 | 原样返回输出 |
| openclaw-docs-update | `772acaf3` | minimax | 单脚本 | 珊瑚群 + 监控群 | 中 | 已从长 prompt 改为脚本 |
| memory-compression | `87c9ad41` | sonnet | 工具型 | 监控群 | 中 | 只统计，不删除 |
| memory-archive-weekly-sync | `6cf8cc6e` | sonnet | 单脚本 + 汇报 | 监控群 | 中 | 调 `sync-memory-to-notebooklm.sh` |
| MEMORY.md 维护 | `7daf5324` | opus | 多步维护 | 晨星 | 中 | 周日晚维护 |
| troubleshooting-weekly-memory-update | `f76b7c1a` | opus | 多步 NotebookLM | 晨星 | 高 | 显式避免跳步 |
| 记忆压缩检查 | `2ac159af` | opus | 多步维护 | 晨星 | 中 | 原 notebooklm 默认任务已加显式模型 |
| memory-quality-audit | `925f0906` | opus | 脚本 + 报告 | 晨星 | 中 | 审计型 |
| NotebookLM 记忆同步 | `39618059` | opus | 单脚本 | 晨星 | 中 | 每日同步 |
| daily-memory-report | `fd541668` | opus | 单脚本 + 双目标推送 | 晨星 + 监控群 | 中 | 已稳定 |
| notebooklm-daily-query | `dd9cb82e` | opus | 单脚本 | 晨星 | 中 | 查询报告 |
| troubleshooting-weekly-cleanup | `8353d365` | opus | 多步整理 | 晨星 | 中 | 周报型 |
| layer3-monthly-archive | `6b710ea9` | opus | 脚本 + 汇报 | 晨星 | 高 | 月度归档 |
| layer3-deep-insights | `739abc98` | opus | 脚本 + 汇报 | 晨星 | 高 | 深度洞察 |
| check-memory-lancedb-pr-status | `496eeea6` | main/systemEvent | 系统提醒 | 静默/按需 | 低 | 非 agentTurn |

---

## 已修复问题

### 1. minimax 跳步问题
- 症状：长 prompt 中漏执行删除/推送等步骤
- 修复：改为单脚本 + 缩短说明 + 降低判断量

### 2. openclaw-docs 旧 source 堆积
- 根因：长 prompt + minimax 跳过删除步骤
- 修复：独立脚本 `update-openclaw-docs.sh`

### 3. memory-compression 复杂度过高
- 根因：minimax 不适合工具链判断任务
- 修复：改 Sonnet，且只统计不删除

---

## 后续维护原则

1. 新增 cron 时，先归类：
   - **脚本型** → minimax 可用
   - **工具型** → sonnet
   - **编排/清理型** → opus

2. 涉及以下内容时，不用 minimax：
   - NotebookLM source 删除 / 清理
   - 多步条件判断
   - memory_list / memory_stats / memory_recall 联动
   - 双目标/多目标通知编排

3. 任何 cron 新建后都要同步更新本文件。
