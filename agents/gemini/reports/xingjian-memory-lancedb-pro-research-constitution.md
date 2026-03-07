# 星鉴流水线研究宪法：memory-lancedb-pro

## 1. 问题定义
**核心目标**：评估并定义 `memory-lancedb-pro` 作为 OpenClaw 增强长期记忆插件的适用性、功能边界与集成策略。

**项目背景**：
- **项目名称**：`memory-lancedb-pro` (v1.1.0)
- **类型**：OpenClaw 增强记忆插件
- **解决的痛点**：OpenClaw 内置的 `memory-lancedb` 插件仅提供基础的向量搜索，在长文本、高频对话场景下存在召回不精准、无法区分时效性、缺乏作用域隔离等问题。
- **核心增强机制**：引入了混合检索（Vector + BM25）、多层评分（如 Jina Rerank、时效加权、重要性加权、MMR 多样性去重）、多 Scope 数据隔离以及专门的自动抓取/召回生命周期钩子，并具备基于 `memoryReflection` 和 `systemSessionMemory` 的会话策略支持。

## 2. 边界与假设

### 2.1 功能边界
1. **职责限定**：它是一个**存储与检索引擎插件**，为 Agent 提供工具调用（`memory_recall`, `memory_store`, `memory_forget`）和自动上下文注入，但不应直接接管或替代主控 Agent 的推理与决策。
2. **检索机制**：默认使用混合搜索（语义 + 关键词）加交叉编码器重排（Reranker），这意味着它的召回质量**高度依赖于所配 Embedding 与 Reranker 接口的稳定性和质量**。
3. **隔离机制**：支持 `global`（全局）、`agent:<id>` 等作用域。对于特定的领域知识或私有偏好，需严格定义作用域隔离。
4. **长文本处理**：自带 Document Chunking，解决长文本超过模型 Context 限制的问题。

### 2.2 核心假设
1. **运行环境支持**：LanceDB 作为底层引擎在目标环境中读写正常，并且不出现 Node 环境下混合 BigInt 的类型崩溃（v1.1.0 已在此方面做了类型收敛处理）。
2. **外部依赖可用**：预设 Gemini（通过代理）或者本地 Ollama 能够提供标准的 OpenAI-compatible Embedding 接口；能够配置有效的 Reranker API（如 Jina 免费层或其它替代品）。
3. **Session 机制**：假定使用 OpenClaw 原生 `systemSessionMemory`（更安全）或开启它的 `memoryReflection`（依赖额外计算和 token）来维护会话上下文。

## 3. 风险评估

### 3.1 兼容性风险 (Embedding & Reranker)
- **Gemini 代理**：通过 `want.eat99.top` 提供 Gemini 接口，需配置 `baseURL` 为兼容 OpenAI 的格式。由于 Gemini Embedding 维度较高（3072），首次入库后维度即被 LanceDB 固化。如果代理服务不稳定导致 Embedding 失败，会自动退化或报错。
- **Ollama 本地**：使用如 `nomic-embed-text` 时，需指定 `baseURL` 为 `http://localhost:11434/v1`。好处是免费稳定，坏处是可能占用本地资源且效果略逊于大厂 API。需通过配置 `embedding.dimensions` 锁定维度。
- **Reranker 强依赖**：高级重排功能强烈依赖 Jina API 等外部服务，存在网络波动或 API 限流超时（5s 超时回退）的风险。

### 3.2 部署与运行风险
- **资源与 Token 开销**：`memoryReflection` 开启时（特别是在 `/new` 或 `/reset` 时），会触发额外的生成任务。如果频繁触发，可能会导致 API token 消耗加剧或本地模型响应慢。
- **上下文污染**：自动注入 `<relevant-memories>` 可能会被 Agent 误读为系统指令或原样输出导致“暴露长期记忆”的尴尬对话。
- **Jiti 缓存坑**：OpenClaw 插件更新或修改 ts 代码时，必须手动清空 `/tmp/jiti/` 缓存，否则会静默加载旧代码。

### 3.3 与现有 Memory 系统的冲突
- 只能有一个 memory 插件处于激活状态。如果启用该 Pro 插件，必须先禁用 OpenClaw 内置的 `memory-lancedb`。
- 旧有数据需要迁移，否则 Agent 会丢失之前存储的历史记忆（虽然提供了 `migrate` 工具，但迁移存在一定数据校验风险）。

## 4. 推荐路线

### 4.1 集成策略 (推荐开启的特性)
1. **替换原生插件**：将 `memory-lancedb-pro` 克隆至 workspace 的 `plugins/` 目录，并配置为 OpenClaw 的 `memory` slot，彻底停用原 `memory-lancedb`。
2. **配置 Embedding**：
   - 优先建议使用 **Ollama + nomic-embed-text**（维度 768 或配置项指定的维度）作为底座，确保最基础的检索不需要消耗外部 API 额度，保证离线可用性。
   - 备选方案：使用代理的 Gemini API（需配好 OpenAI 兼容的 baseURL 比如 `/v1beta/openai/`）。
3. **配置 Reranker**：开启 `cross-encoder` 模式，并配置 Jina API 密钥提升混合检索后的 Top-K 准确度。
4. **Session 策略**：先期配置为 `sessionStrategy: "systemSessionMemory"` 保持与 OpenClaw 核心功能的稳定对接，暂缓启用消耗较大的 `memoryReflection`，直到确定需要强大的反思提取再开启。
5. **Auto-Recall 控制**：建议 `autoRecall: false` 或在系统 prompt 中强制约束 "不要在回复中直接引用或展示 `<relevant-memories>` 区块，仅作内部参考"，防止幻觉或回复冗杂。

### 4.2 部署步骤
1. **环境准备**：确认环境变量（如 API Keys）在 OpenClaw Gateway 守护进程的环境中切实存在。
2. **数据迁移 (按需)**：若旧库中有高价值记忆，使用 `openclaw memory-pro migrate run` 命令执行平滑迁移。
3. **调试与监控**：启用后，利用自带的 CLI（`openclaw memory-pro search` 和 `openclaw memory-pro stats`）进行抽样查验，验证 Vector+BM25 融合与 Rerank 返回质量。
4. **更新维护规范**：将“变更插件代码必须执行 `rm -rf /tmp/jiti/`” 写入团队或系统运维标准。
