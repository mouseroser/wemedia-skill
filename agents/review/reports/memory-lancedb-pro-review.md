# memory-lancedb-pro 适配审查意见（阻塞版）

## 审查状态
上游研究报告不存在，审查被阻塞。

- 目标文件：`/Users/lucifinil_chen/.openclaw/workspace/agents/gemini/reports/memory-lancedb-pro-research.md`
- 读取尝试：共 3 次（首次读取 + 按要求重试 2 次）
- 结果：均返回 `ENOENT`，当前工作区内无法取得织梦产出的研究报告原文

## 结论
**不建议现在上**。

说明：该结论是**信息阻塞导致的流程性否决**，并非已对 `memory-lancedb-pro` 方案本身完成实质性适配通过/否决判断。在缺失上游研究报告的前提下，无法对方案与当前体系的冲突面做可靠审查，贸然推进风险不可控。

## 首发推荐路线
**暂缓首发，先补齐上游研究报告，再重新进入 Step 1.5 审查。**

在重新审查前，不建议进入实现、集成、灰度或默认启用阶段。

## 主要风险
- **原则风险**：无法确认该方案是否违反“文件记忆是真相层”原则，存在把向量库/检索结果错误抬升为事实来源的风险。
- **链路风险**：无法确认其是否依赖当前不稳定或未定稿的 `embeddings/provider` 链路，可能放大现有兼容性与可维护性问题。
- **能力边界风险**：无法判断 `autoRecall`、`autoCapture`、`sessionMemory`、`rerank` 等功能是否被错误纳入首发范围，导致范围失控。
- **回滚风险**：无法确认是否存在清晰的 feature flag、存储隔离、索引重建与停用路径，回滚点不明。
- **评审失真风险**：在缺少原始研究依据的情况下给出结论，会把 review 退化为猜测，不符合 Step 1.5 的审查职责。

## 必要门槛
以下门槛未满足前，不应放行：

1. **补齐研究输入**：提供可读取的上游研究报告原文。
2. **明确真相层边界**：书面说明文件记忆与向量记忆的主从关系，确保文件层为唯一事实源，向量检索仅作候选召回。
3. **明确 embeddings/provider 路线**：说明首发使用的 embedding 方案、兼容范围、失败降级、切换成本与观测方式。
4. **明确首发裁剪范围**：列出必须暂缓的高风险功能，避免一次性上 `autoRecall / autoCapture / sessionMemory / rerank`。
5. **明确回滚点**：提供禁用开关、索引隔离、数据不反写事实层、可回退到“纯文件记忆”模式的路径。

## 当前无法完成的重点审查项
由于缺失上游报告，以下事项当前**无法形成有效审查结论**：

- 是否与“文件记忆是真相层”的原则冲突
- 是否与当前 embeddings/provider 链路问题冲突
- Gemini / Ollama 兼容 embedding 哪个更适合作为首发方案
- 哪些功能必须暂缓（`autoRecall / autoCapture / sessionMemory / rerank` 等）
- 回滚点是否清晰

## 建议的重新进入条件
当上游报告补齐后，下一轮 Step 1.5 应至少回答：

- 向量库在体系中的定位是否被严格限定为“检索层”，而非“事实层”
- 首发 embedding 是否选用更稳定、依赖更少、可离线/可替换的路线
- 首发是否只保留最小闭环：手动入库、手动检索、只读召回、可完全关闭
- 所有自动化记忆与 rerank 能力是否默认关闭并独立挂开关
- 停用后是否可无损退回“纯文件记忆”工作流

## 结构化 verdict
```json
{
  "verdict": "NEEDS_FIX",
  "score": 20,
  "issues": [
    {
      "severity": "critical",
      "category": "logic",
      "description": "上游研究报告缺失，Step 1.5 无法对 memory-lancedb-pro 做实质性适配审查。",
      "location": "/Users/lucifinil_chen/.openclaw/workspace/agents/gemini/reports/memory-lancedb-pro-research.md",
      "suggestion": "先补齐并提供可读取的研究报告原文，再重新发起 review。"
    },
    {
      "severity": "major",
      "category": "logic",
      "description": "在缺少研究输入的情况下，无法验证该方案是否冲击‘文件记忆是真相层’原则。",
      "location": "review:principle-check",
      "suggestion": "重新评审时必须明确文件层与向量检索层的边界和主从关系。"
    },
    {
      "severity": "major",
      "category": "logic",
      "description": "无法确认 embeddings/provider 依赖、首发 embedding 路线、功能裁剪范围与回滚点。",
      "location": "review:launch-readiness",
      "suggestion": "补齐报告后，逐项补充 provider 兼容性、灰度范围、默认关闭项与回滚机制说明。"
    }
  ]
}
```
