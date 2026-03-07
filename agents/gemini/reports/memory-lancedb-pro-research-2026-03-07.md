# 调研报告：memory-lancedb-pro 落地与集成计划

**日期**: 2026-03-07
**任务**: StarChain 研究阶段 - `memory-lancedb-pro` 插件评估与 OpenClaw 引入计划
**评审对象**: `https://github.com/win4r/memory-lancedb-pro.git`

---

## 1. 核心结论
`memory-lancedb-pro` 能够完美填补当前 OpenClaw 纯文件记忆（`MEMORY.md` 等）在**语义检索**和**模糊匹配**上的短板。它原生支持任意兼容 OpenAI API 规范的 Embedding 服务，完美契合我们对 Gemini 和 Ollama 的诉求。

由于其具备长文本自动分块（Long-Context Chunking）和混合检索（Vector + BM25）能力，推荐将其作为**辅助性检索中枢**引入，但**不立刻替代现有的本地文件记忆层**。

## 2. Gemini 与 Ollama 兼容性评估

仓库源码（`src/embedder.ts`）与文档均明确证实：
- **Gemini**: 完美支持。只需将 `baseURL` 指向 `https://generativelanguage.googleapis.com/v1beta/openai/`，模型指定为 `gemini-embedding-001`，其维度自适应为 `3072`。
- **Ollama**: 完美支持。将 `baseURL` 设为 `http://localhost:11434/v1`。**关键限制**：对于本地模型（如 `nomic-embed-text`），必须显式在配置中覆盖 `embedding.dimensions`（如 768），否则会导致维度不匹配的插入错误。

## 3. 渐进式部署计划 (Phased Rollout)

为了严格遵守“保留本地文件记忆作为 Truth Layer”的约束，制定以下三阶段落地计划：

### 阶段一：影子模式 (Shadow Mode) - 纯后台索引
**目标**：无损接入，仅验证 Embedding 流程和向量化存储的稳定性。
- **配置策略**：
  - `autoCapture: false`（关闭对话实时捕获）
  - `autoRecall: false`（关闭自动回忆介入）
  - `sessionStrategy: "none"`（避免干扰现有会话机制）
- **实施动作**：
  - 接入 Ollama 提供本地极速 Embedding（免费且无网络 IO 延迟），或者使用 Gemini Embedding。
  - 使用自带的 CLI 工具或脚本，将现存的 `MEMORY.md` 及 `memory/YYYY-MM-DD.md` 异步批量灌入 LanceDB Pro。
  - 在 Agent 中仅暴露 `memory_search` 供手动调用测试。

### 阶段二：只读外脑 (Read-Only Augmentation)
**目标**：将混合检索能力赋予 Agent，提升长线任务（如 StarChain 跨 Epoch 回溯）的上下文获取能力。
- **配置策略**：
  - `autoRecall: true`（开启自动回忆）
  - `autoRecallMinLength: 20`（调高触发阈值，仅针对复杂指令触发）
  - 引入项目提供的 `new-session-distill` (Gemini Map-Reduce 提取 Worker)，将历史 Session 日志在**后台**由系统进程提炼后注入 LanceDB。
- **实施动作**：
  - 核心状态与 Truth Layer 依然完全依赖 `MEMORY.md`，LanceDB Pro 作为“经验检索库”存在，由 Gemini Worker 定期写入总结。

### 阶段三：混合双轨 (Hybrid Dual-Track)
**目标**：平滑整合双形态记忆。
- **配置策略**：
  - 允许 Agent 调用 `memory_store`（写入 LanceDB）。
  - （可选）开启 `autoCapture: true`。
- **实施动作**：
  - 文件侧：`MEMORY.md` 继续作为**强规则、刚性身份和核心宪法**载体。
  - 数据库侧：`memory-lancedb-pro` 作为**经验片段、历史踩坑记录、零碎知识点**的载体。
  - 启用配置中的 `enableManagementTools: true` 开启 `memory_list` 和治理节点，控制数据库膨胀。

## 4. 推荐配置基线 (Baseline Configuration)

在 `openclaw.plugin.json` 中的推荐 Override 配置：

```json
{
  "plugins": {
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "embedding": {
            "provider": "openai-compatible",
            "model": "nomic-embed-text",
            "baseURL": "http://127.0.0.1:11434/v1",
            "dimensions": 768, 
            "chunking": true
          },
          "sessionStrategy": "none",
          "autoCapture": false,
          "autoRecall": false,
          "enableManagementTools": false
        }
      }
    }
  }
}
```
*(注：如果使用 Gemini，将 baseURL 和 model 替换为对应值，省略 dimensions 即可)*

## 5. 潜在风险与假设
1. **Reranker 依赖**：文档提及 Jina Cross-Encoder Rerank。如果默认强依赖外部 Reranker，在国内网络下可能存在延迟或需额外配置。需要确认其是否可以回退为纯 BM25/Vector RRF 融合分数（代码阅读推断是支持可选的）。
2. **Chunking 消耗**：长文本 `chunking` 功能默认开启，如使用计费 API 会导致 Token 飙升；结合 Ollama 本地模型则无此风险，但需监控本地显存压力。
3. **一致性漂移**：后期若开放 `memory_store` 给 Agent，可能会与 `MEMORY.md` 产生事实冲突。由于检索是基于语义的，Agent 可能会被检索出的过期碎片误导。因此，保留 `MEMORY.md` 永远处于 prompt 最高优先级（系统提示层）是必须的。