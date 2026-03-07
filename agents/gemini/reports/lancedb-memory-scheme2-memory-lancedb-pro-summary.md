# 方案2摘要：`memory-lancedb-pro`

仓库：`https://github.com/win4r/memory-lancedb-pro`

定位：
- OpenClaw 的增强长时记忆插件
- 相比内置 `memory-lancedb`，增加更强的检索、重排、隔离和管理能力

README 关键点：
- 特性：
  - Vector search
  - BM25 full-text search
  - Hybrid fusion (Vector + BM25)
  - Cross-encoder rerank（Jina / custom endpoint）
  - Recency boost / time decay / length normalization / MMR diversity
  - Multi-scope isolation
  - Noise filtering
  - Adaptive retrieval
  - Management CLI
  - Session memory
  - Auto-capture & auto-recall
- 架构：
  - `store.ts`：LanceDB 存储 + FTS + vector search
  - `embedder.ts`：OpenAI-compatible embedding provider abstraction
  - `retriever.ts`：混合检索、融合、重排、后处理
  - `scopes.ts`：scope 隔离（`global` / `agent:<id>` / `custom:<name>` / `project:<id>` / `user:<id>`）
  - `tools.ts`：记忆工具
  - `cli.ts`：list/search/stats/delete/export/import/reembed/migrate
  - `migrate.ts`：从内置 `memory-lancedb` 迁移
- Hook：
  - `before_agent_start`：auto-recall
  - `agent_end`：auto-capture
  - `command:new`：session memory
- 默认理念：
  - 每个 agent 默认可访问 `global` + 自己的 `agent:<id>` scope
- README 的安装建议：
  - 用绝对路径或 clone 到 `<workspace>/plugins/` 下
  - 修改插件配置后 `openclaw gateway restart`
  - 配 embedding / rerank 时，注意 gateway service 不一定继承 shell 环境变量
- README 也提醒：
  - `autoRecall` 可关闭
  - 若开 autoRecall，要避免模型把 `<relevant-memories>` 原样输出
  - rerank/embedding 的 API 依赖是额外复杂度和成本来源
