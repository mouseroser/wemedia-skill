# Layer 3 上游路线重排（基于 PR #206 / #227 反馈）

**创建时间**: 2026-03-17 16:40
**目的**: 把 4H 从“跟进旧 PR”重排为“基于 maintainer 接受边界的两步走路线”。
**当前状态**: 暂停执行。该文档仅保留为策略参考，不作为当前立即开工指令。

---

## 一句话结论

上游现在不该继续围着旧 PR 打转，而应改成：

1. **先做纯基础设施 / hardening 小 PR**
2. **再做 contract-safe、opt-in 的 strict fallback 提案**

PR #206 和 PR #227 都应视为**路线校正样本**，不是必须机械复活的执行对象。

---

## 这次反馈暴露出的上游接受边界

### 来自 PR #206 的边界
- maintainer 不接受“大一统 Layer 3 改造”直接进入默认路径
- 不接受破坏现有 `memory_recall` response contract 的做法
- 对真实 agent E2E 回归非常敏感

### 来自 PR #227 的边界
- “只有测试、没有运行时代码改动”的 PR 价值很低
- 新增测试如果**没有接进 `npm test` / CI 主链**，maintainer 不认为它构成真正回归保障
- 为了修一个很小的问题，也仍然要求 PR 本身有独立工程价值，而不是补形式作业

---

## 重排后的优先级

## A. 该做（先做）

### A1. PR-A：CLI runner hardening
目标：做一个 maintainer 一眼能接受的“稳定性修补 PR”。

范围只限：
- `OPENCLAW_CLI_BIN` override
- workspace-aware `cwd`
- `NO_COLOR`
- outer timeout / watchdog

要求：
- 纯基础设施
- 无默认行为变化
- 不改 `memory_recall` contract
- 不夹带 Layer 3 触发逻辑争议

### A2. 固化 `#227` 的处理原则
把 #227 明确降级为**接受边界样本**，不是当前开放推进线。

只有满足以下任一条件时，才考虑“以新 PR 形式”重新利用这条线：
1. 测试真正接进 `npm test` / CI 主链；
2. 变成真实 runtime 行为修复，而不是测试孤岛。

### A3. 准备 upstream-safe evidence skeleton
只整理可泛化证据：
- strict fallback 为什么必要
- runner hardening 为什么值当
- 哪类低置信度查询真的从深查受益

不带这些本地私货：
- 本地 notebook id
- `nlm-gateway.sh` 私有脚本路径
- 本地 cron / worktree / runtime 编排细节

---

## B. 可做（排在 A 后）

### B1. 先决策：新工具 vs behind flag
在推进 strict fallback 之前，必须先决定接口形态：

- **方案 1：新工具**
  - `enhanced_memory_recall`
  - `memory_recall_v2`
  - `memory_recall_explain`

- **方案 2：旧工具 behind flag**
  - 默认保留旧 contract
  - 开 flag 才进入 enhanced / layered 模式

当前判断：
- maintainer 更可能接受“**新工具**”或“**behind flag**”
- 不太可能接受“直接改旧工具默认行为”

### B2. PR-B：contract-safe strict fallback
只有在 B1 决策完成、且 4E 数据足够支撑后才推进。

要求：
- 只允许低置信度时触发 Layer 3
- 关键词不能单独触发
- 不改旧默认 contract
- 优先 non-default path / behind flag / new tool

---

## C. 暂不做

以下内容明确暂不进入上游当前排期：

1. 机械复活 PR #206
2. 原样重提 PR #227
3. 只加测试、但不接 `npm test` 的 PR
4. 默认改写 `memory_recall` 输出契约
5. 把本地 richer output / NotebookLM / `nlm-gateway` 路线直接绑定为上游默认前提
6. 关键词单独触发 Layer 3 的默认增强路径

---

## 两步走路线（锁定版）

### 第一步
先推 **PR-A（runner hardening / infra-only）**。

成功标准：
- diff 小
- 行为稳定
- maintainer 一眼看懂
- 不引发“你又想重写 memory_recall”警觉

### 第二步
再决定 **strict fallback 走新工具还是 behind flag**，随后才准备 PR-B。

成功标准：
- contract-safe
- 证据驱动
- opt-in / non-default
- 不和本地高配私有方案绑死

---

## 对 4H 的直接影响

4H 后续不再按“PR #227 继续推进”来写，而改为：
- **先做**：PR-A + acceptance boundary 收口 + evidence skeleton
- **后做**：新工具 vs behind flag 决策 + PR-B 草案
- **不做**：旧 PR 机械复活 / contract 改写 / 测试孤岛 PR

---

## 最终判断

> 上游现在要追求的不是“证明我的方案更强”，而是“给 maintainer 一个足够小、足够稳、足够不吓人的下一步”。

也就是说：

- **先把可合并性做出来**
- **再把能力做进去**
