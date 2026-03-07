# memory-lancedb-pro 研究宪法

## 一、 问题定义

### 1. 核心目标
本项目 `memory-lancedb-pro` 是为 OpenClaw 开发的一款增强型长期记忆插件，旨在解决内置基础插件 (`memory-lancedb`) 检索能力薄弱、缺乏作用域隔离和治理工具的问题，从而提升 OpenClaw Agent 在复杂交互中对历史信息的召回准确率和记忆管理效率。

### 2. 关键痛点与解决方案
*   **单一向量检索导致精确度不足**：引入混合检索 (Vector 向量查询 + BM25 全文查询)，并通过 RRF (Reciprocal Rank Fusion) 策略融合。
*   **检索结果缺乏上下文和时效性权重**：引入多阶段打分流水线（交叉编码器重排、近期提升/时间衰减机制、长度归一化、MMR 多样性、硬性最低分过滤）。
*   **多 Agent 记忆污染**：提供多作用域 (Multi-Scope) 隔离，支持 global, agent, project, user 等层级。
*   **记忆垃圾数据过多**：增加自适应检索和噪声过滤（过滤拒绝回复、元提问、日常寒暄）。
*   **管理与运维成本高**：提供全套 CLI 命令用于管理、审查、统计、导出/导入及从基础版本无缝迁移。
*   **内省与自进化的缺失**：集成支持 sessionMemory 和 memoryReflection（基于 JSONL 会话蒸馏），从而实现从聊天记录中提取可复用的知识。

## 二、 边界

### 1. 分析范围
*   **功能矩阵**：混合检索管线、自适应检索策略、打分机制的参数敏感性。
*   **架构集成**：与 OpenClaw Plugin API 的挂载机制（`before_agent_start`, `agent_end` 钩子），及与底层 LanceDB (`@lancedb/lancedb` >=0.26.2) 的交互。
*   **生态兼容性**：支持多种 OpenAI 兼容的 Embedding 接口 (Jina, OpenAI, Gemini, Ollama 等) 以及主流的 Rerank API (Jina, SiliconFlow, Voyage, Pinecone)。

### 2. 限制与非目标
*   **不涉及基础数据库开发**：直接复用 LanceDB 的向量和 FTS（全文检索）能力，不修改底层数据存储结构或重写索引算法。
*   **不包含纯独立 UI**：主要通过 OpenClaw 提供的 CLI 和工具函数 (`memory_store`, `memory_recall` 等) 以及 Agent System Prompt 结合使用，不涉及单独的 GUI 前端开发。
*   **不承担核心决策**：记忆插件主要提供可信的信息获取途径，最终对话输出依赖大语言模型（LLM）的分析。

## 三、 风险

### 1. 部署风险
*   **API 依赖与延迟**：交叉编码器（Rerank）默认通过 API 访问（如 Jina、SiliconFlow），网络延迟或限流可能导致每次记忆检索的额外延时。需配置降级策略（Graceful Degradation）以防接口失败。
*   **环境依赖问题**：LanceDB 底层依赖 Apache Arrow，对于特定类型的处理（如 0.26+ 版本的 BigInt 处理）可能会报错（如 "Cannot mix BigInt and other types"），要求插件版本需大于 `1.0.14` 且需要进行适当的类型转换。

### 2. 运行与集成风险
*   **记忆污染机制失效**：尽管有噪声过滤，但如果 `auto-capture`（自动捕获）或者 `jsonl-distill`（会话蒸馏）的 prompt 出现偏差，依然可能存入大量垃圾记忆导致 LanceDB 查询降级。
*   **隐私与安全**：Scope 隔离机制依赖于配置和调用的规范，若默认权限配置不当（例如全部走 global），可能会导致 Agent 泄露不同用户的私密会话信息。
*   **热更新缓存陷阱**：直接修改 `.ts` 文件后重启可能会由于 `jiti` 缓存未清空导致旧代码继续运行，引起隐蔽 bug。

## 四、 关键问题

1.  **架构兼容性**：项目如何在现有仅支持 Gemini/Ollama 的离线或混合 Embedding 环境下，保证 Vector + BM25 和 Rerank 的平滑运行？（如：不使用 Jina Rerank 时如何无缝降级或替换为本地轻量级重排方案）
2.  **融合打分策略验证**：RRF 融合 (Vector 权重 + BM25 权重) 与之后的多阶段调整（时间衰减、长度归一化）如何避免导致高相关性的短记忆被意外过滤（`hardMinScore` 配置）？
3.  **内省（Reflection）流**：项目中提供的 JSONL 自动蒸馏和 memoryReflection 是否能够在资源受限的环境下高效运行，是否会带来过多的 Token 消耗？
4.  **迁移与兼容性**：现有的内置 `memory-lancedb` 数据如何确保 100% 安全平滑地迁移到此增强版（即分析 `migrate.ts` 工具的容错性）？
5.  **铁律强制性**：如何确保 Agent 系统配置中正确添加了“AI Agents 铁律”约束以防止由于未清除 `jiti` 缓存造成的错误？