# memory-lancedb-pro 插件研究报告

## 项目摘要
**memory-lancedb-pro** 是一个 OpenClaw 增强型长期记忆插件，作为内置 `memory-lancedb` 的上位替代，引入了混合检索（向量 + BM25）、跨编码器重排序（Rerank）、多层隔离（Scope）和多种智能衰减机制。它的核心目标是提供高信噪比的长程知识留存及回忆，降低无用对话污染，并增强跨多 Agent 项目的记忆管理与分配能力。当前版本为 `1.0.32`。

## 可用能力清单
1. **混合检索引擎**: 并行支持 Vector 语义搜索和 LanceDB 内置的 BM25 FTS 倒排搜索，经过调优的 RRF 融合。
2. **多阶段重排与衰减**:
   - Cross-encoder Rerank (默认支持 jina, siliconflow, voyage, pinecone)。
   - 基于时间衰减 (Time Decay) 和时效性加成 (Recency Boost)。
   - 基于长度的归一化 (Length Norm) 和重要性加权。
3. **多作用域 (Scope) 隔离**: 允许划分 `global`、`agent:<id>`、`user:<id>` 等，防止异构环境下的记忆污染。
4. **智能降噪**: `Auto-Capture`（自动捕获）与 `Auto-Recall`（自动回忆），内置过滤闲聊、Meta 问题和拒绝回复等机制；支持按字数跳过不需要记忆检索的查询（中文字数门槛特调为 6 字）。
5. **记忆强化**: 支持按照“手动召回”频次延长 Time Decay 的 Half-Life（默认系数 0.5）。
6. **Markdown 镜像留存**: 支持把 LanceDB 的条目双写一份为 Markdown。
7. **自动化与管理能力**: 附带一套 CLI 工具（查看、批量删除、备份导入导出等），以及推荐外置的 Session JSONL 异步蒸馏管线（`examples/new-session-distill`）。

## Embedding 接入建议
插件兼容任意 OpenAI API 协议的 Embeddings 接口（支持轮询池 `apiKey` 数组）。配置项归集于 `plugins.entries.memory-lancedb-pro.config.embedding`。

### Gemini 接入建议
Gemini 的 Embedding API（如 `gemini-embedding-001` 或 `text-embedding-004`）具有较大的维度（如 3072）和优秀的跨语种泛化能力。
**配置示例**:
```json
"embedding": {
  "apiKey": "${GEMINI_API_KEY}",
  "model": "text-embedding-004",
  "baseURL": "https://generativelanguage.googleapis.com/v1beta/openai/",
  "dimensions": 768, 
  "chunking": true
}
```
*注：Gemini 允许在生成端或 API 侧降维（例如 768），建议按需在 `dimensions` 中指定。*

### Ollama 接入建议
适合对本地算力和数据隐私敏感的节点。推荐使用轻量的专用文本 Embedding 模型，如 `nomic-embed-text`（维度 768）或 `mxbai-embed-large`。
**配置示例**:
```json
"embedding": {
  "apiKey": "dummy",
  "model": "nomic-embed-text",
  "baseURL": "http://localhost:11434/v1",
  "dimensions": 768,
  "chunking": true
}
```

## 不建议立即启用的功能
1. **Session Memory 聚合入库 (`sessionMemory.enabled: true`)**:
   - 理由：会将多轮的会话内容暴力塞入 LanceDB，造成关键词检索污染和 Token 消耗。
   - 替代：建议维持默认的 `false`，改用官方文档提供的通过 webhook/cron + `jsonl_distill` 等异步**外挂蒸馏**方式进行提纯后入库。
2. **Auto-Recall (`autoRecall: true`)**:
   - 理由：在当前的 OpenClaw 配置中，默认将 `<relevant-memories>` 隐性塞入 prompt 容易引起模型原样“吐出”提示词（暴露记忆机制）。若未在 `system prompt` 配合严苛的隐蔽输出要求，建议暂时关闭，依赖手动 Tool (`memory_recall`) 或者将其作为幕后节点的静默工具。
3. **Markdown Mirroring (`mdMirror.enabled: true`)**:
   - 理由：如果主节点（真相层）依然强依赖文件系统的文本库（如我们当前的做法），开启这个选项会导致“真相层”产生严重的分叉（LanceDB 里的修改不会反向映射到原有知识库 Markdown，反而会另写一套文件），增加双写冲突的治理负担。

## 对当前体系的适配建议（初稿）
1. **缓解 Embedding / Provider 链路不稳定的风险**:
   - 当前网络环境或多 Provider 切换时，容易遇到超时。可利用该插件的 `embedding.apiKey` 数组轮询特性（虽然主要防限流，也可兜底容灾）。
   - 若外网 Embedding 不稳，可优先在 Node 层走内网穿透直连局域网的 Ollama 作为 Embedding 基座（BM25 作为无模型本地召回本身已经能兜底约 40% 的确定性命中）。
2. **处理“文件记忆与向量记忆双重存在”冲突**:
   - **核心痛点**：当前环境以“文件”作为真相层（Truth Layer），而此插件建立了一套独立的 Vector 真相层。
   - **应对策略**：将 `memory-lancedb-pro` 的定位由“唯一真相”降级为**“索引加速器”与“经验法则库（Principle Layer）”**。
   - **落地建议**：
     - Scope 层面约束：将“硬事实”存入工作区共享文件；将“模型避坑指南、沟通偏好、易错命令”等高频小粒度知识通过此插件写入 `scope=global` 的 LanceDB。
     - 开发阶段限制使用该插件保存大量的业务 Spec 或代码结构，而仅用于保存：`"不要把文件写在 XXX 目录"` 这种教训。
3. **部署方式注意**:
   - 在我们的环境中，不要使用相对路径引用，推荐直接克隆至 workspace 的 `plugins/memory-lancedb-pro` 目录并采用绝对路径进行挂载以防止 JITI 缓存和 CWD 导致找不到模块的问题。
   - 配置改动或底层 `.ts` 更新时，**务必执行** `rm -rf /tmp/jiti/` 否则重启 OpenClaw 后依然加载陈旧代码。