# 4H.2 — PR #227 上游收口说明

**日期**: 2026-03-21  
**作者**: 小光（todo-autopilot）  
**关联任务**: master-execution-plan.md 4H.2  
**类型**: 策略收口 / 接受边界固化

---

## 背景

2026-03-17，memory-lancedb-pro 上游 maintainer 关闭了 PR #227，给出的核心理由：

1. 本 PR 仅新增测试文件，**无任何运行时代码变更**
2. 新增的测试未接入 `npm test` / CI 主链，CI 默认不会运行
3. PR 对实际功能无任何影响，maintainer 认为不满足合并门槛

---

## 收口结论：什么时候才值得重提

PR #227 **不以原样重提**。重启上游推进（新 PR 形式）需满足以下**任一**硬性条件：

| 条件 | 说明 |
|------|------|
| 测试真正接入 `npm test` / CI 主链 | 不是孤立测试文件，而是在官方 CI pipeline 可以跑通的测试 |
| 变更包含真实运行时行为修复 | 不是"只加测试"，而是有实质功能改动（哪怕很小） |
| strict fallback 提案采用 opt-in / behind flag 形式 | 不改默认 response contract，允许用户显式开启 |

**不满足上述任一条件**，重提即浪费上游 reviewer 资源，概率极高再次关闭。

---

## 边界约束（固化为下一轮提案门槛）

### ✅ 可做（接受边界内）
- **PR-A 类**：纯基础设施加固——`OPENCLAW_CLI_BIN` override / workspace-aware `cwd` / `NO_COLOR` / outer timeout watchdog  
  - 要求：无默认行为变化、不改 response contract、不夹带 Layer 3 触发争议
- **新工具路线**：`enhanced_memory_recall` / `memory_recall_v2` 等，旧工具保持默认契约不变
- **opt-in strict fallback**：低置信度触发 L3，behind flag，不改旧工具默认输出格式

### ❌ 不做（已知被拒接受边界外）
- 原样重提 #227（测试孤岛 + 无 CI 接入）
- 机械复活 PR #206（历史冲突版本，不再回溯）
- 只加测试但不接 `npm test` 的 PR
- 直接修改 `memory_recall` 默认 response contract

---

## 推进顺序（若未来恢复）

```
PR-A（纯基础设施）
   ↓ 合并 + 稳定
接口边界决策（新工具 vs behind flag）
   ↓ 确认方案
PR-B（opt-in strict fallback）
```

**前置条件**：PR-A 合并后 + 4E 数据充分 + 接口边界已决策。三者未就绪前，不启动 PR-B。

---

## 当前状态

- **本轮不启动**：PR-A 起草 / PR-B 草案 / evidence skeleton 实际写作
- **保留策略**：上述推进顺序与接受边界已固化，随时可按序恢复
- **关联 deadline**：4H 整体 deadline 2026-03-24；若本周仍未推进，顺延至 2026-03-31

---

## 参考文件

- `reports/layer3-dual-track-roadmap-20260317.md`
- `reports/layer3-dual-track-mapping-20260317.md`
- `reports/layer3-upstream-priority-reset-20260317.md`
- master-execution-plan.md 4H 区块
