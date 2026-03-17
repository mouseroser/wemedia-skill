# PR-A Scope Draft — CLI Runner Hardening

**创建时间**: 2026-03-17 16:47
**所属主线**: 4H.3 / Layer 3 上游兼容路线
**定位**: infra-only, small PR, contract-safe

---

## 一句话目标

提交一个 maintainer 一眼能接受的 **纯基础设施加固 PR**：

> **只提升外部 CLI 调用链路的稳定性与可配置性，不改变 `memory_recall` 的默认契约，不引入新的 Layer 3 触发逻辑。**

---

## 为什么先做这个

基于 PR #206 / #227 的反馈，上游当前更容易接受的是：
- 小 diff
- 可独立验证
- 不改默认语义
- 不把本地高配方案强塞进公共仓库

PR-A 的作用不是“把能力做满”，而是先建立一个更稳、更干净的 runner 基座，为后续 strict fallback / opt-in 能力铺路。

---

## 推荐 PR 标题

### Preferred
`refactor: harden cli runner path for layer3 fallback`

### 备选
- `chore: harden external cli runner used by layer3 fallback`
- `refactor: isolate and harden layer3 fallback cli execution`

> 不建议标题里出现 `memory_recall` 行为增强、NotebookLM 深能力、layered output 等容易引发误解的词。

---

## In Scope（只做这些）

### 1. CLI 可执行路径可配置
目标：不要把 runner 永久写死在单一路径上。

建议：
- 为外部 CLI 增加**显式路径解析 helper**
- 支持 env override（如 `OPENCLAW_CLI_BIN`，或对当前 nlm gateway 路径继续保留 `NLM_GATEWAY_PATH` 这种模式）
- 默认路径保持现状，不改变已有默认行为

验收点：
- 未设置 env 时，行为与当前一致
- 设置 env 后，runner 使用指定可执行路径
- 错误信息能明确反映“路径不存在 / 不可执行”而不是模糊失败

---

### 2. workspace-aware `cwd`
目标：外部 CLI 执行时，不再隐式依赖当前进程工作目录。

建议：
- 为 CLI 调用显式设置 `cwd`
- 优先使用 runtime / tool context 中可解析到的 workspace
- 退回默认 workspace 时，也走统一 helper，而不是分散硬编码

当前本地实现里已有可借鉴边界：
- `resolveWorkspaceDir(...)`

验收点：
- 在不同 runtime / session 上下文下，runner 的 cwd 可预测
- 不因为宿主进程 cwd 漂移导致行为不稳定

---

### 3. 统一最小环境变量约束
目标：让 CLI 输出更稳定、更可解析，减少颜色/交互噪音。

建议：
- 为子进程注入最小、明确的 env
- 至少包含：`NO_COLOR=1`
- 保持 `PATH` / `HOME` 等必要继承，不做激进环境清洗

验收点：
- CLI 输出在测试环境 / CI / 本地环境更一致
- 不因为颜色码或交互样式变化影响解析

---

### 4. 外层 timeout / watchdog 收口
目标：让超时变成**明确、可诊断**的 infra 错误，而不是模糊的下游失败。

建议：
- 在现有 timeout 之上，统一错误分型与消息格式
- 明确区分：
  - process spawn failed
  - process timeout
  - process exited non-zero
  - empty output
  - json parse failed
- 保持 timeout 的默认语义不变，不借机调整触发门或策略门

当前本地实现里已有可借鉴触点：
- `buildNotebookLMFallbackCommand(...)`
- `runNotebookLMFallbackQuery(...)`
- `runNotebookLMFallbackQueryWithBudget(...)`

验收点：
- timeout 失败能稳定归因为 timeout，而不是混成一般 tool error
- 错误信息足够清晰，便于 maintainer 和 CI 直接判断失败类型

---

## Out of Scope（这次明确不做）

以下内容全部不进入 PR-A：

1. 改 `memory_recall` 默认输出格式
2. 改 Layer 3 触发策略
3. 关键词单独触发 / strict fallback 逻辑调整
4. 新工具设计（`memory_recall_v2` / `enhanced_memory_recall` 等）
5. richer output / layered output 默认化
6. Notebook 选择策略、私有 notebook ID、私有 `nlm-gateway.sh` 路径约定
7. 把本地 cron / worktree / runtime 特殊编排带进上游

---

## 预期触点（以当前本地实现为参考）

如果沿用当前本地结构，PR-A 大概率只会触碰少量 runner 相关 helper：

- `src/tools.ts`
  - `resolveWorkspaceDir(...)`
  - `resolveNlmGatewayPath(...)` 或对应 CLI path resolver
  - `buildNotebookLMFallbackCommand(...)`
  - `runNotebookLMFallbackQuery(...)`
  - `runNotebookLMFallbackQueryWithBudget(...)`

重点是：
- **抽整 runner 边界**
- **不扩散业务逻辑改动**
- **不顺手夹带 strict fallback 本体**

---

## 测试建议（最小集）

### Unit / focused tests
至少覆盖：
1. **CLI path override**
   - env 存在时使用 override
   - env 不存在时走默认解析
2. **cwd 解析**
   - runtime 提供 workspace 时使用该路径
   - 缺省时退回统一默认 workspace
3. **timeout 错误归类**
   - 超时应返回明确 timeout 语义
4. **non-zero exit / empty output / parse fail**
   - 错误类型彼此可区分

### 不建议在 PR-A 里做的测试
- Layer 3 触发门 benchmark
- `memory_recall` 端到端行为改写验证
- 新工具 / behind flag 行为矩阵

---

## Draft PR Body

### Summary
This PR hardens the external CLI runner used by the Layer 3 fallback path without changing `memory_recall`'s default contract or fallback trigger behavior.

### What changes
- make CLI path resolution explicit and overridable
- make child-process `cwd` workspace-aware and deterministic
- inject a minimal stable env (`NO_COLOR=1`)
- normalize timeout / spawn / exit / parse error handling for the runner path

### What this PR does NOT do
- no contract changes to `memory_recall`
- no new Layer 3 trigger logic
- no keyword-based fallback changes
- no new tool surface
- no layered/richer output changes

### Why this is useful
It reduces runner-specific fragility and makes future fallback work easier to validate without coupling this PR to any behavior change proposal.

### Validation
- focused tests for path resolution
- focused tests for workspace-aware cwd
- focused tests for timeout / exit / parse error classification

---

## 合并标准（我方内部）

只有同时满足以下条件，才认为 PR-A ready：
1. diff 足够小，maintainer 一眼能看懂
2. 不碰 `memory_recall` 默认 contract
3. 不夹带 strict fallback 争议
4. 测试覆盖 runner hardening 本身，而不是借题发挥扩散到 Layer 3 大方案

---

## 下一步接口

PR-A 完成后，才进入：
- **4H.4** 新工具 vs behind flag 决策
- **4H.5** PR-B（strict fallback, contract-safe, opt-in）

也就是说：

> **PR-A 的任务不是证明 Layer 3 很强，而是先把“外部 CLI runner 这条路可以被稳定、低风险地维护”证明出来。**
