# Memory Retrieval Baseline — 2026-03-14

## 目标
建立当前记忆系统的真实基线，区分：
1. 生产主链路（memory-lancedb-pro）
2. OpenClaw builtin memorySearch（当前处于影子链路 / 评估态）

---

## 一、当前架构基线

### A. 生产主链路：memory-lancedb-pro
- `plugins.slots.memory = memory-lancedb-pro`
- 版本：`memory-lancedb-pro@1.1.0-beta.8`
- embedding：`nomic-embed-text`（Ollama）
- rerank：本地 sidecar `BAAI/bge-reranker-v2-m3`
- 能力：
  - `memory_recall`
  - `memory_stats`
  - autoCapture
  - autoRecall
  - memoryReflection hooks

### B. 影子链路：OpenClaw builtin memorySearch
- `agents.defaults.memorySearch.enabled = true`
- provider：`ollama`
- model：`nomic-embed-text`
- FTS：ready
- sqlite-vec：ready
- embedding cache：enabled
- 当前不是主链路，只用于评估最新 OpenClaw 自带记忆能力

---

## 二、主链路健康状态（memory-lancedb-pro）

### memory_stats
- Total memories: **324**
- Scope: `agent:main`
- Retrieval mode: **hybrid**
- FTS support: **Yes**

### 类别分布
- fact: 102
- preference: 34
- decision: 116
- other: 38
- entity: 18
- reflection: 16

### 抽样 recall 结果

#### 命中良好
1. `TODO 文件应该放在哪里？`
   - 正确召回：`~/.openclaw/todo/`
2. `升级到 memory-lancedb-pro@1.1.0-beta.8 后出现了什么回归？`
   - 正确召回：`memory_list` / `memory_stats` 默认返回 0
3. `OpenClaw 有新版本时要做什么联动？`
   - 正确召回：立即更新 `openclaw-docs` notebook
4. `主私聊会话有什么约束？`
   - 正确召回：main 不承载长时间编排
5. `同一问题三次未解决怎么办？`
   - 正确召回：必须切换方向

#### 发现的歧义点
6. `scripts 应该放在哪里？`
   - 同时召回两类记忆：
     - `~/.openclaw/scripts/`（系统级脚本）
     - skill 内 `scripts/`（skill 自带脚本）
   - 结论：不是“召回失败”，而是**术语层面存在歧义**，benchmark 要拆分成“系统级脚本”和“skill 脚本”两个问题

### 主链路结论
**memory-lancedb-pro 当前工作正常，主要问题不是可用性，而是：**
- 少数查询存在术语歧义
- 中文召回质量仍需要 benchmark 验证
- 需要持续观察噪音与重复召回

---

## 三、builtin memorySearch 基线

### 当前状态（main）
- Sources: `memory`
- Indexed: **40 / 126 files**
- Chunks: **143**
- Dirty: no
- Vector: ready
- FTS: ready
- Embeddings: ready

### 关键发现 1：`sources = ["memory", "sessions"]` 但实际只看到 `memory`
当前 config 里声明了 `sessions`，但 `openclaw memory status --deep` 只显示：
- `Sources: memory`

这说明：
- session transcript recall 当前**并未真正生效**
- docs 中最新机制要求同时开启 `experimental.sessionMemory = true`
- 当前配置属于“写了 sessions，但没有完整启用 session memory”

### 关键发现 2：builtin memorySearch 当前会被超长文件卡住
实际测试 `openclaw memory search` 时出现稳定报错：

```text
[memory] sync failed (session-start): Error: Ollama embeddings HTTP 500: {"error":"the input length exceeds the context length"}
[memory] sync failed (search): Error: Ollama embeddings HTTP 500: {"error":"the input length exceeds the context length"}
```

### 高概率根因
builtin memorySearch 默认索引：
- `MEMORY.md`
- `memory/**/*.md`

而当前 `memory/` 下仍包含超大归档文件：
- `memory/archive/notebooklm-daily-20260313.md` — **395,782 bytes**
- `memory/archive/notebooklm-daily-20260314.md` — **256,592 bytes**
- `memory/archive/MEMORY-2026-03-14-before.md` — **26,951 bytes**

这意味着：
> **Layer 1 的“archive 仍在 memory/ 目录内”与 builtin memorySearch 的默认索引范围天然冲突。**

### builtin 实测结果
#### 查询：`TODO 文件应该放在哪里？`
- 结果：`No matches`
- 同时伴随 sync failed（超长输入）

#### 查询：`Telegram`
- 结果：`No matches`
- 同时伴随 sync failed（超长输入）

#### 查询：`monitor-bot`
- 结果：可命中旧日志中的相关段落
- 但仍伴随 sync failed

### builtin 结论
builtin memorySearch **不是“稍微差一点”**，而是当前被 Layer 1 archive 布局显著拖垮：
- 可部分命中
- 但每次 search 都可能触发 sync 失败
- 当前不适合直接升级为主检索链路

---

## 四、子 Agent memorySearch 卫生状态
`openclaw memory status --deep` 显示多个 agent 处于：
- `Indexed: 0`
- `Dirty: yes`
- `memory directory missing`

典型包括：
- monitor-bot
- coding
- brainstorming
- wemedia
- nano-banana
- gemini
- notebooklm

### 结论
当前 builtin memorySearch 在多 agent 上有明显噪音：
- 从“系统可用性”看不是故障
- 但从“运行卫生”看，会持续制造 dirty / missing directory 提示

---

## 五、当前判断

### 已验证可用
- `memory-lancedb-pro` 主链路：**可用**
- `memory_recall`：**可用**
- `memory_stats`：**可用**

### 当前阻塞点
- builtin memorySearch 被 `memory/archive/` 中的大文件拖垮
- sessionMemory 没有真正启用完整
- 中文 recall 质量还没有形成系统 benchmark

---

## 六、下一步建议
1. **先不切主插件**
2. **先不直接应用 builtin memorySearch 增强配置**（因为索引超长文件问题未解）
3. **先完成 benchmark 查询集与评分口径**
4. **先决定 archive 布局是否要移出 `memory/`**
5. **再评估 hybrid / MMR / temporalDecay / sessionMemory 是否值得正式启用**

---

## 七、一句话结论
> 当前真正稳定的记忆主链路还是 `memory-lancedb-pro`；builtin memorySearch 的主要问题不是排序策略，而是**默认索引范围与 `memory/archive/` 布局冲突**。