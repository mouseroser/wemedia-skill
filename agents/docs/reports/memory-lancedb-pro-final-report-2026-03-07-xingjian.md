# memory-lancedb-pro Final Report

**Xingjian Pipeline Step 6 - Final Delivery**  
**Date**: 2026-03-07  
**Output Path**: `reports/memory-lancedb-pro-final-report-2026-03-07-xingjian.md`

---

## 1. Title

**memory-lancedb-pro Integration Assessment: Hybrid Retrieval as Auxiliary Layer**

---

## 2. CoreConclusion

`memory-lancedb-pro` 是一个功能强大的混合检索插件（Vector + BM25 + Cross-Encoder Rerank），可作为 OpenClaw 的高性能二级辅助索引。**推荐渐进集成**，但必须严格保持 `MEMORY.md` + `memory/YYYY-MM-DD.md` 为唯一 truth layer。

**关键结论**:
- ✅ Gemini/Ollama embedding 兼容性已验证
- ✅ 混合检索能力可提升记忆召回精度
- ⚠️ 必须禁用 autoRecall、mdMirror、selfImprovement 等隐式行为
- ⚠️ 状态不一致和 context pollution 是核心风险，需通过配置基线严格管控

---

## 3. RecommendedArchitecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenClaw Gateway                           │
├─────────────────────────────────────────────────────────────────┤
│  Local File Memory (Truth Layer)                                │
│  ┌─────────────────┐  ┌─────────────────────┐                  │
│  │   MEMORY.md     │  │ memory/YYYY-MM-DD.md│  ← 权威 truth   │
│  └─────────────────┘  └─────────────────────┘                    │
├─────────────────────────────────────────────────────────────────┤
│  memory-lancedb-pro (Auxiliary Layer)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Vector      │  │    BM25      │  │ Cross-Encoder│          │
│  │  Search      │→ │  Keyword     │→ │   Rerank     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│  Embedding Providers                                             │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │   Gemini     │  │    Ollama    │  ← 本地开发/备选           │
│  │ (primary)    │  │  (fallback)  │                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

**核心设计原则**:
- Truth Layer 不变: 本地 markdown 文件保持唯一权威
- Auxiliary 定位: LanceDB 仅作为高性能二级检索索引
- Explicit over Implicit: 禁用 autoRecall，要求 agent 显式调用检索工具

---

## 4. PhasePlanSummary

| Phase | Duration | Focus | Exit Criteria |
|-------|----------|-------|---------------|
| **Phase 0** | 1-2 周 | 基础设施准备 | 测试 namespace 可用，embedding 端点可响应 |
| **Phase 1** | 2-3 周 | 受控试点 | 检索质量达标，无状态不一致 |
| **Phase 2** | 持续 | 生产渐进 | Phase 1 稳定运行 2 周无重大问题 |

---

## 5. EnableNow

| Feature | Rationale |
|---------|-----------|
| `memory_store` | 基础存储能力，与本地文件互补 |
| `memory_recall` | 显式检索，agent 主动触发，无副作用 |
| `memory_update` | 更新已有记忆条目 |
| `memory_forget` | 删除特定记忆 |
| Hybrid retrieval (Vector + BM25) | 核心价值，keyword + semantic 混合检索 |
| Cross-encoder rerank | 提升检索精度 |
| Multi-scope isolation | 支持 agent 级别隔离 |
| Gemini embedding (OpenAI-compatible) | 已验证可用 |
| Ollama (fallback) | 本地开发/离线备选 |

---

## 6. DeferNow

| Feature | Rationale | Recommendation |
|---------|-----------|----------------|
| `autoRecall` | 自动注入可能导致 context pollution，失控 | 永远禁用 |
| `mdMirror` | 与本地 MEMORY.md 冲突，破坏 truth layer | 永久禁用 |
| `sessionStrategy: mdMirror` | 同上 | 禁用 |
| `selfImprovement` hooks | 隐式行为，难以预测 | 禁用 |
| External reranker API | 引入额外依赖和延迟 | 使用内置 rerank 或 defer |

---

## 7. Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R1 | **Context Pollution**: 过度检索导致无关信息淹没关键上下文 | High | 禁用 autoRecall，限制 topK，手动审查 |
| R2 | **State Desync**: LanceDB 与本地文件不一致导致信息冲突 | High | 禁用 mdMirror，仅将 LanceDB 作为辅助索引 |
| R3 | **Complexity Overhead**: 多阶段检索引入延迟和配置复杂度 | Medium | 逐步启用各阶段，提供 fallback 降级 |
| R4 | **Implicit Behaviors**: 隐藏的 hooks/auto 行为导致不可预测 | Medium | 显式禁用 selfImprovement |
| R5 | **Token Exhaustion**: 过度检索填充 context window | Medium | 设置 strict topK 上限，监控 token 使用 |

**回滚触发条件**:
- LanceDB 与本地文件状态不一致持续 > 24h
- 检索延迟 P99 > 5s
- Context pollution 导致 agent hallucination
- 插件崩溃或 Gateway 不稳定

---

## 8. RecommendedNextAction

1. **立即启动 Phase 0**: 确认 Gateway 环境可访问 Gemini embedding 端点
2. **创建测试 namespace**: 使用 `memory-lancedb-pro` 隔离测试环境
3. **应用 ConfigBaseline**: 按报告第 5 节配置部署，禁止所有 defer 项
4. **试点范围**: 先从 `agent:review` 和 `agent:gemini` 开始

---

## 9. ReportPath

- **Final Report**: `reports/memory-lancedb-pro-final-report-2026-03-07-xingjian.md`
- **Constitution**: `agents/gemini/reports/memory-lancedb-pro-research-2026-03-07-xingjian.md`
- **Implementation Plan**: `agents/review/reports/memory-lancedb-pro-implementation-plan-2026-03-07-xingjian.md`
- **Consistency Review**: `agents/gemini/reports/memory-lancedb-pro-consistency-review-2026-03-07-xingjian.md`

---

*星鉴流水线 Step 6 交付完成*  
*Docs Agent | 2026-03-07*
