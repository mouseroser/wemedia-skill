# OpenClaw memory / embeddings / memory_search / vector DB 摘要

## 1. Memory 系统架构与配置
- OpenClaw 当前至少有两条 memory 路径：
  - `memory.backend: builtin`：走 OpenClaw 内建 memory 能力。
  - `memory.backend: qmd`：走 QMD sidecar / 外部检索流水线。
- `memory.citations` 控制回复里记忆引用展示：`auto | on | off`。
- QMD 相关核心字段：
  - `memory.qmd.command`
  - `memory.qmd.mcporter.enabled`
  - `memory.qmd.mcporter.serverName`
  - `memory.qmd.mcporter.startDaemon`
  - `memory.qmd.searchMode`
  - `memory.qmd.includeDefaultMemory`
  - `memory.qmd.paths[].path`
  - `memory.qmd.paths[].pattern`
  - `memory.qmd.paths[].name`
  - `memory.qmd.sessions.enabled`
  - `memory.qmd.sessions.exportDir`
- 另有运行时级的 `memorySearch` 配置块，偏向文件/会话检索源控制：
  - `memorySearch.enabled`
  - `memorySearch.sources`（已见值：`memory`、`sessions`）
  - `memorySearch.extraPaths`

## 2. Embeddings provider 配置方法
- OpenClaw 已暴露 `memory-lancedb` 插件配置：
  - `plugins.entries.memory-lancedb.enabled`
  - `plugins.entries.memory-lancedb.config.embedding.apiKey`
  - `plugins.entries.memory-lancedb.config.embedding.model`
  - `plugins.entries.memory-lancedb.config.dbPath`
  - `plugins.entries.memory-lancedb.config.autoCapture`
  - `plugins.entries.memory-lancedb.config.autoRecall`
  - `plugins.entries.memory-lancedb.config.captureMaxChars`
- 当前文档显示 embedding provider 直接对接 OpenAI embeddings：
  - `embedding.apiKey`（支持 `${OPENAI_API_KEY}`）
  - `embedding.model` 可见枚举：`text-embedding-3-small` / `text-embedding-3-large`
- 说明当前官方案例更偏「provider 固定、模型可切换」，而不是通用多 provider 抽象层。

## 3. `memory_search` 工具实现原理
- 文档信号表明其本质是“多源记忆检索入口”，而不是单一数据库直查：
  - 一层是 `memorySearch.sources` 对源做路由（`memory` / `sessions`）
  - 一层是 `memory.backend` 决定底层检索引擎（`builtin` / `qmd`）
  - 若启用 `memory-lancedb`，则由插件提供向量化 long-term memory、auto-capture、auto-recall
- 因此实现上更像三层：
  1. 运行时工具入口（`memory_search`）
  2. source/router（memory files、session transcripts、extra paths）
  3. backend / plugin（builtin、QMD、LanceDB）
- 旁路优化信号：存在 SQLite embeddings cache 控制项（文档提到 `Embedding Cache Max Entries`），说明至少有本地缓存层来减少重复 embedding/重建成本。

## 4. 向量数据库集成最佳实践
- 配置建议：
  - 小规模本机优先 `memory.backend: builtin` + `memory-lancedb` 插件，不要一上来启 QMD。
  - 仅在需要更复杂索引/外部检索编排时切 `memory.backend: qmd`。
- 路径建议：
  - 明确设置 `plugins.entries.memory-lancedb.config.dbPath`，不要完全依赖默认路径，便于备份与迁移。
  - 对 QMD 使用 `memory.qmd.paths[].name` 设稳定 collection 名，避免跨机器路径变化导致 collection 漂移。
- 检索源建议：
  - `memorySearch.sources` 先只开 `memory`；确实需要历史会话召回时再加 `sessions`，否则噪声和索引 churn 都会上升。
- 自动化建议：
  - `autoCapture`、`autoRecall` 先灰度开启；生产环境要限制 `captureMaxChars`，避免长文本误收录和成本膨胀。
- 成本/性能建议：
  - 默认先用 `text-embedding-3-small`；只有在召回质量明显不足时再升级 `text-embedding-3-large`。
  - 若走 QMD 且冷启动明显，可启 `memory.qmd.mcporter.enabled` 降低每次 spawn 开销。
- 数据治理建议：
  - 开启 `memory.citations: auto`，让回忆内容可追踪。
  - 会话索引 `memory.qmd.sessions.enabled` 只在确有需要时打开，避免把短期上下文和长期知识混在一起。

## 5. LanceDB / 其他向量数据库集成案例信号
- 已明确存在官方插件：`@openclaw/memory-lancedb`
  - 定位：LanceDB-backed long-term memory plugin
  - 能力：`autoCapture`、`autoRecall`、OpenAI embedding、可配置 `dbPath`
- 已明确存在另一条后端路线：QMD
  - 通过 `memory.backend: qmd` + `memory.qmd.*` 字段接入
  - 更像“外部检索/索引管线”而非单纯内嵌向量库
- 在当前检索结果里，没有看到官方对 Pinecone / Weaviate / Milvus / pgvector 的同等级一方插件字段；现阶段最清晰、最落地的官方集成案例就是 LanceDB。

## 适合当前环境的落地建议
- 你当前环境是本地 OpenClaw workspace，最稳妥路线：
  1. 保持 `memory.backend: builtin`
  2. 启用 `plugins.entries.memory-lancedb.enabled: true`
  3. 配置 `plugins.entries.memory-lancedb.config.embedding.apiKey`
  4. 模型先选 `plugins.entries.memory-lancedb.config.embedding.model: text-embedding-3-small`
  5. 显式设置 `plugins.entries.memory-lancedb.config.dbPath: ~/.openclaw/memory/lancedb`
  6. `autoCapture: false` 起步，验证后再开
  7. `autoRecall: true` 可先开，但要观察召回噪声
  8. `captureMaxChars` 控制在 `300-800` 区间更稳
- 如果你要把 `memory` notebook 迁移到向量库，建议顺序：
  - 先迁静态高价值知识（MEMORY.md / memory/*.md）
  - 再决定是否纳入 `sessions`
  - 最后再考虑 QMD sidecar 或更重型检索架构
- 如果目标是“最少维护成本 + 本地可控”，优先 LanceDB；
- 如果目标是“统一多源知识索引 + 更复杂检索流程”，再评估 QMD。