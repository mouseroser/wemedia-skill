# Todo 每日检查报告

**检查时间**: 2026-03-19 07:00:52
**待办文件数**: 8
**统计来源**: master-execution-plan.md（canonical）

---

## 📊 任务统计

| 优先级 | 总任务 | 已完成 | 待完成 |
|--------|--------|--------|--------|
| P0（立即执行） | 3 | 3 | 0 |
| P1（本周执行） | 60 | 35 | 25 |
| P2（需要时执行） | 8 | 0 | 8 |
| P3（长期观察） | 15 | 0 | 15 |
| **总计** | **86** | **38** | **48** |

---

## 🎯 当前待办详情（来自 master）

### 🔴 P0（立即执行）

（无待办任务）

### 🟡 P1（本周执行）

- [ ] **4A.3** 9层架构自身适配计划同步维护
- [ ] **4B.5** 观察期与后端策略决策（见原计划文件）
- [ ] **4C.7** 等待 PR #206 maintainer 审批并合并
- [ ] **4E.6** Day 6（03-20）：同上
- [ ] **4E.7** Day 7（03-21）：同上 + 最终评估报告
- [ ] **4F.1** 超时阈值：确认 timeout=45s 默认值 + 50s 上限已在代码中生效
- [ ] **4F.2** 重试策略：实现时间感知单次重试（非固定指数退避）
- [ ] **4F.3** 结果截断：实现 3000 字符硬截断 + `[TRUNCATED n chars]` 尾注
- [ ] **4F.4** JSON 防御：验证分层防御解析已生效（清洗控制字符→直接parse→fenced JSON提取→降级）
- [ ] **4F.5** 基于 4E 观察期数据，决定是否调整 L3 触发阈值（minScore/minResults）
- [ ] **4F.6** 基于 4E 数据，决定是否需要 notebook 自动刷新机制
- [ ] **4F.7** 基于 4E 数据，决定是否实现预计算缓存（方案 C）
- [ ] **4G.1** 在 retriever.ts 添加 `local` rerank provider
- [ ] **4G.2** 本地测试验证
- [ ] **4G.3** 提交 PR 到 memory-lancedb-pro
- [ ] **4G.4** 创建独立 repo: `memory-lancedb-pro-rerank`
- [ ] **4G.5** 添加 Dockerfile
- [ ] **4G.6** 编写一键安装脚本
- [ ] **4G.7** 在 memory-lancedb-pro README 添加 "Using Local Rerank" 章节
- [ ] **4G.8** 部署示例 + 对比表 (本地 vs 云端)
- [ ] **4H.2** 用 PR #227 关闭反馈重置上游门槛
- [ ] **4H.3** 若未来恢复推进，PR-A 仍是首选入口（当前暂停）
- [ ] **4H.4** 先决策：新工具 vs behind flag
- [ ] **4H.5** 再起草 PR-B：strict fallback（contract-safe, opt-in）
- [ ] **4H.6** 整理 upstream-safe evidence skeleton + 两步走计划

---

## 💡 建议

- 📅 有 25 个待完成的 P1 任务需要本周推进

---

**报告路径**: /Users/lucifinil_chen/.openclaw/workspace/memory/todo-check-20260319.md
