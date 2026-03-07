# memory-lancedb-pro Implementation Plan

**Xingjian Pipeline Step 3**  
**Date**: 2026-03-07  
**Role**: review/opus (主方案)  
**Constitution Source**: Gemini research report

---

## 1. RecommendedArchitecture

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenClaw Gateway                           │
├─────────────────────────────────────────────────────────────────┤
│  Local File Memory (Truth Layer)                                │
│  ┌─────────────────┐  ┌─────────────────────┐                    │
│  │   MEMORY.md     │  │ memory/YYYY-MM-DD.md│  ← 权威 truth     │
│  └─────────────────┘  └─────────────────────┘                    │
├─────────────────────────────────────────────────────────────────┤
│  memory-lancedb-pro (Auxiliary Layer)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Vector      │  │    BM25      │  │ Cross-Encoder│          │
│  │  Search      │→ │  Keyword     │→ │   Rerank     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│  Embedding Providers (抽象层)                                    │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │   Gemini     │  │    Ollama    │  ← 本地开发/备选           │
│  │ (primary)    │  │  (fallback)  │                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 关键设计原则

- **Truth Layer 不变**: `MEMORY.md` + `memory/YYYY-MM-DD.md` 保持为唯一权威数据源
- **Auxiliary 定位**: memory-lancedb-pro 作为高性能二级检索索引，不替代本地文件
- **Explicit over Implicit**: 禁用 autoRecall，要求 agent 显式调用 `memory_recall` 工具

---

## 2. PhasePlan

### Phase 0: 基础设施准备 (1-2 周)

| 任务 | 描述 | 交付物 |
|------|------|--------|
| P0.1 | 环境检查：确认 Gateway 可访问 Gemini/Ollama 端点 | 网络连通性报告 |
| P0.2 | 配置 embedding 端点：Gemini (primary) + Ollama (fallback) | `config.yaml` 片段 |
| P0.3 | 创建隔离的测试 namespace (非生产) | 测试环境就绪 |
| P0.4 | 制定监控指标：检索延迟、命中率、状态一致性 | 监控仪表盘 |

**入口标准**: 测试 namespace 可用，embedding 端点可响应

### Phase 1: 受控试点 (2-3 周)

| 任务 | 描述 | 交付物 |
|------|------|--------|
| P1.1 | 部署 memory-lancedb-pro 到测试 namespace | 插件运行 |
| P1.2 | 配置 `autoRecall: false`，仅启用手动检索 | 安全配置 |
| P1.3 | 验证 hybrid retrieval 效果：Vector + BM25 + Rerank | 检索质量报告 |
| P1.4 | 监控 LanceDB 与本地文件的同步状态 (mdMirror 禁用) | 一致性报告 |
| P1.5 | 小规模 agent 试用 (2-3 个 agent，限定 scope) | 试点反馈 |

**入口标准**: 检索质量达标，无状态不一致

### Phase 2: 生产渐进 (持续)

| 任务 | 描述 | 交付物 |
|------|------|--------|
| P2.1 | 扩展到更多 agent scope | 生产部署 |
| P2.2 | 根据 Phase 1 数据调优权重 (recency boost, time decay) | 优化配置 |
| P2.3 | 启用可选的 autoRecall（仅对经过验证的 agent） | 渐进放开 |
| P2.4 | 建立回滚/降级机制 | 应急预案 |

**入口标准**: Phase 1 稳定运行 2 周无重大问题

---

## 3. EnableNow

以下功能可在部署时立即启用：

| 功能 | 理由 |
|------|------|
| `memory_store` | 基础存储能力，与本地文件互补 |
| `memory_recall` | 显式检索，agent 主动触发，无副作用 |
| `memory_update` | 更新已有记忆条目 |
| `memory_forget` | 删除特定记忆 (需审计日志) |
| Hybrid retrieval (Vector + BM25) | 核心价值，提供 keyword + semantic 混合检索 |
| Cross-encoder rerank | 提升检索精度 |
| Multi-scope isolation | 支持 agent 级别隔离 |
| Gemini embedding (OpenAI-compatible) | 已验证可用 |

---

## 4. DeferNow

以下功能建议推迟或禁用：

| 功能 | 理由 | 建议 |
|------|------|------|
| `autoRecall` | 自动注入可能导致 context pollution，失控 | 永远禁用或仅在 P2.3 试点 |
| `mdMirror` | 与本地 `MEMORY.md` 冲突，破坏 truth layer | 永久禁用 |
| `sessionStrategy: mdMirror` | 同上 | 禁用 |
| `selfImprovement` hooks | 隐式行为，难以预测 | 禁用 |
| External reranker API | 引入额外依赖和延迟 | 使用内置 rerank 或 defer |

---

## 5. ConfigBaseline

```yaml
# memory-lancedb-pro baseline config for OpenClaw

plugin: memory-lancedb-pro

# 检索配置
retrieval:
  vector:
    enabled: true
    topK: 10
  bm25:
    enabled: true
    topK: 10
  rerank:
    enabled: true
    model: "cross-encoder/ms-marco-MiniLM-L-6-v2"  # 本地或兼容模型
    topN: 5

# 行为控制 (安全优先)
behavior:
  autoRecall: false          # 禁用自动召回
  mdMirror: false            # 禁用文件镜像
  selfImprovement: false     # 禁用隐式改进
  sessionStrategy: "systemSessionMemory"  # 使用 OpenClaw 内置

# Embedding 提供商
embedding:
  provider: "gemini"         # primary
  apiUrl: "https://generativelanguage.googleapis.com/v1beta/openai/"
  model: "text-embedding-004"
  dimensions: 768
  
  fallback:
    provider: "ollama"
    apiUrl: "http://localhost:11434/v1"
    model: "nomic-embed-text"
    dimensions: 768

# 作用域隔离
scopes:
  - global
  - agent:review
  - agent:coding
  - agent:gemini

# 评分参数 (需调优)
scoring:
  recencyBoost: 1.5
  timeDecay:
    halfLifeDays: 7
  importanceWeight: 0.3
  lengthNormalization: true
```

---

## 6. Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R1 | **Context Pollution**: autoRecall 或过度检索导致无关信息淹没关键上下文 | High | 禁用 autoRecall，限制 topK，手动审查触发频率 |
| R2 | **State Desync**: LanceDB 与本地文件不一致导致信息冲突 | High | 禁用 mdMirror，仅将 LanceDB 作为辅助索引 |
| R3 | **Complexity Overhead**: 多阶段检索引入延迟和配置复杂度 | Medium | 逐步启用各阶段，提供 fallback 降级 |
| R4 | **Implicit Behaviors**: 隐藏的 hooks/auto 行为导致不可预测 | Medium | 显式禁用 selfImprovement 和未知 hooks |
| R5 | **Token Exhaustion**: 过度检索填充 context window | Medium | 设置 strict topK 上限，监控 token 使用 |

---

## 7. RollbackTriggers

以下条件触发回滚：

| Trigger | Condition | Action |
|---------|-----------|--------|
| RT1 | LanceDB 与本地文件状态不一致持续 > 24h | 禁用插件，回退到纯文件检索 |
| RT2 | 检索延迟 P99 > 5s (正常应 < 500ms) | 降级为单一 vector search 或禁用 |
| RT3 | Context pollution 导致 agent hallucination 证据 | 立即禁用 autoRecall，审查配置 |
| RT4 | 插件崩溃或未捕获异常导致 Gateway 不稳定 | 回滚到上一稳定版本 |
| RT5 | 任何安全漏洞或未授权数据访问 | 完全禁用插件 |

---

## 8. Recommendation for Current Environment

### 8.1 立即行动

1. **启动 Phase 0**: 确认 Gateway 环境可访问 Gemini embedding 端点
2. **创建测试 namespace**: 使用 `memory-lancedb-pro` 隔离测试
3. **应用 ConfigBaseline**: 按第 5 节配置部署，禁止所有 defer 项

### 8.2 当前环境适配

- **Embedding**: 优先使用 Gemini (已验证兼容)，Ollama 作为本地开发 fallback
- **模型**: 使用 `text-embedding-004` (768 dim) 或 `nomic-embed-text` (768 dim)
- **Scope**: 先从 `agent:review` 和 `agent:gemini` 开始试点

### 8.3 成功标准 (Phase 1 Exit)

- 检索延迟 < 500ms (P99)
- Hybrid retrieval 命中率 > 80%
- 无状态不一致报告
- Agent 反馈正向

---

## Conclusion

**memory-lancedb-pro** 具备强大的 hybrid 检索能力，适合作为 OpenClaw 的二级辅助索引。其 Gemini/Ollama 嵌入兼容性已通过架构验证。

**推荐策略**: 采用 **Phase 0 → Phase 1 → Phase 2** 渐进部署，以 `MEMORY.md` + daily files 为 truth layer 不可动摇。禁用所有隐式行为 (autoRecall, mdMirror, selfImprovement)，仅启用显式检索工具。

**风险可控**: 通过严格的配置基线和回滚触发器，可有效控制状态不一致和 context pollution 风险。

---

*Report generated by Xingjian Pipeline Step 3*  
*Role: review/opus*  
*Constitution: Gemini research 2026-03-07*
