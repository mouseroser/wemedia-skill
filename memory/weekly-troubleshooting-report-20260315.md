# 每周故障排查清理报告

**报告周期**: 2026-03-09 ~ 2026-03-15
**生成时间**: 2026-03-15 23:30 (Asia/Shanghai)
**执行者**: troubleshooting-weekly-cleanup cron

---

## 一、本周故障概况

### 错误统计（gateway.err.log）

| 日期 | 错误数 | 趋势 |
|------|--------|------|
| 03-10 | 200 | 📊 基线 |
| 03-11 | 131 | ✅ 下降 |
| 03-12 | 144 | ➡️ 持平 |
| 03-13 | 181 | ⬆️ 上升 |
| 03-14 | 399 | 🔴 峰值 |
| 03-15 | 581 | 🔴 最高（含 LanceDB 迁移错误） |

**总计**: 本周 2,609 条错误/警告日志
- API Rate Limit 错误: 389 次
- Timeout 错误: 341 次
- Gateway 重启次数: ~952 次（含热加载）

---

## 二、本周已解决的问题 ✅

### 1. Control UI CSS Regression（已解决 03-15）
- **症状**: context-notice 显示异常
- **根因**: OpenClaw 旧版本 CSS 选择器缺失
- **修复**: 升级到 v2026.3.13 后内置修复已足够，移除 hotfix override
- **状态**: ✅ 已关闭，hotfix 目录已清理

### 2. layer2-health-check.sh 使用不存在的 CLI 命令（已解决 03-15）
- **症状**: 健康检查连续 4 天报"缺少 openai 模块" + "unknown command 'memory-pro'"
- **根因**: AI 自动生成的脚本臆造了 `openclaw memory-pro` 命令
- **修复**: 改为 `openclaw memory search`，适配输出格式
- **状态**: ✅ 已关闭，健康评分 100/100

### 3. memory-lancedb-pro openai SDK 依赖冗余（已解决 03-15）
- **症状**: 使用 openai SDK 调用本地 Ollama，引入不必要的依赖
- **修复**: embedder.ts 和 llm-client.ts 改用原生 fetch
- **状态**: ✅ 已关闭

### 4. Cron 脚本路径全面清理（已解决 03-15）
- **症状**: 5+ 个 cron 任务引用不存在的脚本路径
- **修复**: 迁移脚本到正确目录，更新所有 cron payload
- **状态**: ✅ 已关闭

### 5. Layer 3 配置被升级清除（已解决 03-15）
- **症状**: OpenClaw 升级到 v2026.3.13 后 layer3Fallback 配置被清掉
- **修复**: 建立 runtime worktree 隔离 + post-upgrade-guard.sh 自动守护
- **状态**: ✅ 已关闭，稳态防护已落地

### 6. PR #210 Claude Code Review fork-PR 假失败（已解决 03-15）
- **症状**: fork PR 上 OIDC token 获取失败导致 CI 红灯
- **修复**: PR #210 已合并，fork PR 自动跳过 claude-review
- **状态**: ✅ 已关闭

### 7. Cron delivery 配置缺失（已解决 03-15）
- **症状**: 记忆压缩检查和 layer3-deep-insights 任务成功但通知投递失败
- **修复**: 补上 delivery.to 字段
- **状态**: ✅ 已关闭

---

## 三、未解决的问题 ⚠️

### 🔴 P0 — LanceDB 数据损坏/迁移不完整
- **症状**: memory_stats 返回 Total memories: 0；gateway.err.log 持续报 `Not found: ...0100110010010111010101101b37f846459ca2d0fa0b8c0fd7.lance`
- **影响**: 记忆系统 Layer 2 向量检索完全失效
- **根因**: 看起来是 embedding 模型迁移（nomic → bge-m3？）过程中，旧 LanceDB 数据文件被清理但新索引未完全建立。当前 `lancedb-pro/` 目录只有 2 个 data 文件，而备份目录 `lancedb-pro-backup-nomic-20260315/` 有数百个完整的数据文件
- **备份可用**: ✅ `memories-export-pre-bge-m3.json` (487KB) + `memory-backup-2026-03-15.jsonl` (481KB) + `lancedb-pro-backup-nomic-20260315/` (完整旧索引)
- **建议**: 需要晨星决定是回滚到旧 nomic 索引还是完成 bge-m3 重建
- **工作量**: ~1-2 小时

### 🟡 P1 — memory_list/stats 上游 PR #187 未合并
- **症状**: memory_list 本地补丁每次升级被覆盖
- **状态**: PR #187 等待上游合并
- **影响**: 每次 OpenClaw 升级后需要手动重新 apply 补丁
- **缓解**: post-upgrade-guard.sh 可自动检测但不能自动重新 apply 代码补丁

### 🟡 P1 — PR #206 等待上游合并
- **症状**: feat/layer3-notebooklm-fallback PR 处于 CLEAN + MERGEABLE 状态
- **状态**: 代码就绪，依赖 maintainer 审批
- **影响**: Layer 3 fallback 功能继续运行在本地 worktree，上游未集成

### 🟡 P1 — Cron 任务超时
- **症状**: memory-compression-check (6cf8cc6e) 最近一次运行超时（300016ms）
- **根因**: 任务执行时间超过 5 分钟限制
- **建议**: 增加 timeoutSeconds 或拆分为更小的子任务

### 🟢 P2 — auto-capture 噪音偏多
- **症状**: 单日产生 30+ 条 auto-capture 记忆，约 40% 是低质量内容
- **状态**: 建议调高 minScore 到 0.5（当前 0.35）
- **影响**: 增加记忆系统存储和检索负担

### 🟢 P2 — Gateway 日志文件过大
- **症状**: gateway.log 已达 40.5MB，gateway.err.log 1.5MB
- **建议**: 考虑日志轮转或定期清理

---

## 四、清理结果

### 已清理项目
1. ✅ Control UI hotfix 目录已删除（control-ui-hotfix-20260314 + backup）
2. ✅ 旧 cron 脚本路径已迁移
3. ✅ openai SDK 依赖已移除
4. ✅ 冗余 gateway.controlUi.root 配置已移除
5. ✅ P2.3 双轨路线决策已关闭（放弃 builtin memorySearch）

### 保留但需关注
1. ⚠️ `lancedb-pro-backup-nomic-20260315/` — 等 LanceDB 修复后可清理
2. ⚠️ `memories-export-pre-bge-m3.json` — 等 LanceDB 修复后可清理
3. ⚠️ `lancedb-pro.backup-20260310-110747/` — 较旧备份，确认新数据稳定后清理
4. ⚠️ `.openclaw/memory/*.sqlite` (多个 scope) — 10 个 scope 数据库共 ~30MB，均未更新（03-14 16:45），可能是迁移残留

---

## 五、系统健康评分

| 指标 | 状态 | 评分 |
|------|------|------|
| 记忆审计 | ✅ 0 告警 0 错误 | 100/100 |
| Layer 2 向量检索 | 🔴 LanceDB 数据损坏 | 0/100 |
| Layer 3 Fallback | ✅ 配置已恢复 + 守护 | 90/100 |
| Cron 任务 | 🟡 1/11 超时 | 80/100 |
| 日志健康 | 🟡 日志过大 | 70/100 |
| 配置守护 | ✅ post-upgrade-guard 运行中 | 95/100 |
| **综合评分** | | **72/100** |

---

## 六、下周优先行动项

| 优先级 | 任务 | 预计工作量 |
|--------|------|-----------|
| P0 | 修复 LanceDB 数据损坏（回滚或重建） | 1-2h |
| P1 | 跟进 PR #187 和 #206 上游合并 | 持续 |
| P1 | 修复 memory-compression-check 超时 | 30min |
| P2 | 调整 auto-capture minScore 阈值 | 10min |
| P2 | 实施日志轮转 | 30min |

---

**报告路径**: `~/.openclaw/workspace/memory/weekly-troubleshooting-report-20260315.md`
**下次生成**: 2026-03-22 23:30 (每周日晚)

*此报告由 troubleshooting-weekly-cleanup cron 自动生成*
