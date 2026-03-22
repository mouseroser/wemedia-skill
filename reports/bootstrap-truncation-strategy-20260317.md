# bootstrapMaxChars 截断策略说明

**日期**: 2026-03-17  
**状态**: 已落地机制说明 + 当前配置快照  
**适用范围**: OpenClaw session bootstrap / workspace files 注入阶段

---

## 1. 结论先看

当前 OpenClaw 已有可工作的 bootstrap 截断机制，核心规则如下：

1. **优先级顺序**：`L1-L6 > L7 > L8 > L9`
   - L1-L6 属于系统/开发者级指令，逻辑上优先于后续注入层
   - `bootstrapMaxChars` 直接控制的是 **bootstrap 注入内容**（典型是 L7 workspace files，以及由 bootstrap hook 追加的上下文文件）
   - 当 bootstrap 内容过大时，**先截断后注入**，不会反向覆盖更高层规则

2. **单文件上限**：当前配置 `bootstrapMaxChars = 32000`
   - 单个 bootstrap 文件超过 32000 字符时，会被截断
   - 截断不是只保留开头，而是 **保留头部 + 尾部**，中间插入说明

3. **总预算上限**：若未显式配置，则使用默认 `bootstrapTotalMaxChars = 150000`
   - 多个 bootstrap 文件会按顺序消耗总预算
   - 总预算不足时，后续文件会被截短或直接跳过

4. **当前主会话静态文件占用**：约 **17933 chars / 32000 chars = 56.0%**
   - 当前已注入主文件仍在安全区间内
   - 以当前快照看，距离单文件阈值还有较明显余量；真正风险更偏向“未来继续增肥”而不是“已经爆掉”

---

## 2. 当前配置快照

来自 `~/.openclaw/openclaw.json`：

```json
"bootstrapMaxChars": 32000
```

运行时代码默认值（来自 bootstrap 构建逻辑）：

- `DEFAULT_BOOTSTRAP_MAX_CHARS = 20000`
- `DEFAULT_BOOTSTRAP_TOTAL_MAX_CHARS = 150000`
- `DEFAULT_BOOTSTRAP_PROMPT_TRUNCATION_WARNING_MODE = "once"`
- `MIN_BOOTSTRAP_FILE_BUDGET_CHARS = 64`
- `BOOTSTRAP_HEAD_RATIO = 0.7`
- `BOOTSTRAP_TAIL_RATIO = 0.2`

说明：
- 当前实例已把单文件上限从默认 **20000** 提高到 **32000**
- 当前未见显式 `bootstrapTotalMaxChars` 配置，因此按默认 **150000** 处理
- 当前未见显式 `bootstrapPromptTruncationWarning` 配置，因此按默认 **once** 处理

---

## 3. 实际截断算法

运行时代码会对每个 bootstrap 文件执行如下逻辑：

### 3.1 单文件截断
若文件长度 `<= bootstrapMaxChars`：
- 原样注入（只做 `trimEnd()`）

若文件长度 `> bootstrapMaxChars`：
- 保留前 `70%`
- 保留后 `20%`
- 中间插入明确提示：
  - `[...,truncated, read <file> for full content...]`
  - `…(truncated <file>: kept <head>+<tail> chars of <original>)…`

也就是：

```text
[头部 70%]

[...truncated, read FILE for full content...]
…(truncated FILE: kept X+Y chars of Z)…

[尾部 20%]
```

这比“只截尾”更稳，因为：
- 头部通常保留定义、规则、身份、总览
- 尾部通常保留最近补充、更新日志、结论
- 中间最容易是展开解释和历史细节，优先牺牲合理

### 3.2 总预算控制
文件按注入顺序依次处理：
- 先检查剩余总预算
- 若剩余预算 `< 64 chars`，停止继续追加文件
- 当前文件允许使用的上限为：
  - `min(bootstrapMaxChars, remainingTotalChars)`
- 如仍超预算，再做一次硬裁剪（末尾省略号）

所以是 **“单文件上限” + “全局总预算” 双重限制**，不是只有一个 32000。

---

## 4. 截断优先级顺序

这里区分两层“优先级”：

### 4.1 指令层优先级
在系统提示词组合意义上，遵循：

```text
L1-L6 > L7 > L8 > L9
```

含义：
- **L1-L6**：系统 / 开发者 / 安全 / 运行约束，不应被低层重写
- **L7**：静态文件（如 AGENTS.md / SOUL.md / USER.md / THESIS 等）
- **L8**：bootstrap hook / 动态注入
- **L9**：实时流量、消息元数据、相关记忆等

因此“截断风险最大”的通常是 **L7/L8/L9 的补充性上下文**，不是 L1-L6。

### 4.2 bootstrap 文件预算顺序
在 bootstrap 文件内部，按**注入顺序**消耗预算；越靠后的文件越容易被预算挤压。

这意味着如果希望关键文件更稳：
- 核心规则文件应尽量短
- 关键文件应尽量排在前面
- 大体积参考材料不应和核心身份文件抢同一预算池

---

## 5. 当前上下文使用情况（主会话静态文件快照）

以下是当前主会话已加载核心静态文件的字符数快照：

| 文件 | 字符数 | 占 32000 比例 |
|------|--------|---------------|
| AGENTS.md | 4427 | 13.8% |
| SOUL.md | 881 | 2.8% |
| IDENTITY.md | 508 | 1.6% |
| USER.md | 742 | 2.3% |
| TOOLS.md | 921 | 2.9% |
| MEMORY.md | 4512 | 14.1% |
| THESIS.md | 3185 | 10.0% |
| FEEDBACK-LOG.md | 2757 | 8.6% |
| **合计** | **17933** | **56.0%** |

**剩余余量（相对 32000）**：`14067 chars`

注意：
- 这是“当前主会话静态文件快照”，不是完整 prompt 全量 token 统计
- 它足够回答“bootstrap 文件是否已经明显逼近阈值”这个问题
- 当前结论：**尚未逼近单文件 32000 阈值，但总量管理仍值得持续关注**

---

## 6. 已有日志机制

运行时已具备**截断告警**，并非完全黑箱。

### 6.1 已存在的 warning 文案
当文件被截断时，会产生类似 warning：

```text
workspace bootstrap file <file> is <originalLength> chars (limit <maxChars>); truncating in injected context
```

当总预算过低时，会产生类似 warning：

```text
remaining bootstrap budget is <n> chars (<64); skipping additional bootstrap files
```

### 6.2 当前模式
默认 warning 模式为：

```text
bootstrapPromptTruncationWarning = "once"
```

可理解为：
- `off`: 不提示
- `once`: 每次 prompt 构建链路做一次告警
- `always`: 每次都明确提示

### 6.3 现状判断
所以“日志机制”严格来说**已经有基础版**，缺的是更产品化的呈现：
- 还没有专门的上下文占用面板
- 还没有每层 token/char 可视化
- 还没有统一的“本轮哪些文件被截断”摘要卡片

也就是说：
- **P0 里的“日志机制”可以视为已有基础能力，文档化已完成第一步**
- 更好的可视化和预警面板，仍应归入后续 P1/P2 工作

---

## 7. 实际建议

### 7.1 当前可执行口径
对外/对内统一这样描述最稳：

> OpenClaw 在 bootstrap 注入阶段使用 `bootstrapMaxChars` 控制单文件大小，默认采用“保留头部 70% + 尾部 20% + 中间插入截断说明”的策略；多文件还受总预算控制。高优先级系统层（L1-L6）逻辑上高于 L7/L8/L9，后者即使被截断，也不应反向覆盖高层约束。

### 7.2 后续建议
1. 给 `/status` 或独立报告补一个 **bootstrap context usage** 小节
2. 记录“本轮注入了哪些文件、各自 chars、多大比例、是否截断”
3. 对 AGENTS.md / MEMORY.md / THESIS.md 做持续瘦身，优先控制大文件
4. 若未来 L8/L9 继续增肥，优先新增 **分层预算**，而不是继续无脑抬高 32000

---

## 8. 本次交付物

本轮已完成：
- ✅ 补齐 `bootstrapMaxChars` 实际行为文档
- ✅ 明确优先级顺序：`L1-L6 > L7 > L8 > L9`
- ✅ 说明现有截断 warning 机制
- ✅ 给出当前主会话静态上下文使用快照

待后续继续推进（不在本轮自动做）：
- ⏳ 可视化上下文面板
- ⏳ 更细粒度的 per-layer token 统计
- ⏳ 截断预警产品化展示
