# memory-lancedb-pro 增强型长期记忆插件 - 交付文档

**项目代号**: memory-lancedb-pro  
**任务级别**: S 级（标准报告）  
**交付日期**: 2026-03-07  
**文档版本**: v1.0

---

## 一、执行摘要

### 1.1 项目概述

`memory-lancedb-pro` 是为 OpenClaw 开发的增强型长期记忆插件，旨在解决内置基础插件 (`memory-lancedb`) 检索能力薄弱、缺乏作用域隔离和治理工具的问题。

### 1.2 核心价值

| 能力 | 描述 |
|------|------|
| **混合检索** | Vector + BM25 双路召回，RRF 融合策略 |
| **智能重排** | Cross-Encoder 重排，支持 Jina/SiliconFlow/Ollama |
| **多阶段打分** | 6 层打分流水线（近期提升、重要性权重、长度归一化、时间衰减、MMR 多样性、硬性过滤） |
| **作用域隔离** | global / agent / project / user / custom 多层级隔离 |
| **自适应检索** | 自动跳过寒暄/命令，智能识别记忆相关查询 |
| **噪声过滤** | 过滤拒绝回复、元提问、HEARTBEAT 等垃圾数据 |
| **会话内省** | 支持 sessionMemory 和 memoryReflection |
| **自进化机制** | 自动提取知识到 LEARNINGS.md / ERRORS.md |

### 1.3 部署建议

- **推荐配置**: Gemini Embedding + Ollama 本地 Rerank
- **部署时间**: 30-60 分钟（含测试验证）
- **前置条件**: Node.js >= 18, OpenClaw Gateway, Gemini API Key 或 Ollama

---

## 二、技术方案

### 2.1 核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                    memory-lancedb-pro                        │
├─────────────────────────────────────────────────────────────┤
│  Auto-Capture          │  Auto-Recall                       │
│  ─────────────         │  ─────────────                     │
│  agent_end hook        │  before_agent_start hook           │
│  ↓                     │  ↓                                  │
│  噪声过滤 → 重要性判断  │  查询 → 自适应检索判断              │
│  ↓                     │  ↓                                  │
│  混合存储              │  混合检索 → Rerank → 多阶段打分    │
│  (Vector + BM25)       │  ↓                                  │
│  ↓                     │  返回 Top-K 记忆                    │
│  Markdown 镜像         │                                     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 关键技术点

#### 混合检索 (Vector + BM25)
- **Vector 检索**: LanceDB ANN 向量索引，支持 HNSW 近似最近邻
- **BM25 检索**: LanceDB FTS 全文索引，关键词匹配
- **RRF 融合**: `score = Σ(1/(k+rank))`，k=60 默认

#### Cross-Encoder 重排
- 支持 Jina / SiliconFlow / Pinecone API
- 5s 超时保护 + 自动降级到 cosine 排序
- 推荐本地 Ollama 部署 `bge-reranker-v2-m3`

#### 多阶段打分流水线
1. **近期提升**: `exp(-ageDays / halfLife) * weight`
2. **重要性权重**: `score *= (0.7 + 0.3 * importance)`
3. **长度归一化**: `score *= 1 / (1 + 0.5 * log2(len/anchor))`
4. **时间衰减**: `score *= 0.5 + 0.5 * exp(-ageDays / halfLife)`
5. **MMR 多样性**: cosine > 0.85 → 降权 50%
6. **硬性过滤**: score < threshold → 丢弃

### 2.3 与内置版本对比

| 功能 | memory-lancedb | memory-lancedb-pro |
|------|----------------|-------------------|
| BM25 全文检索 | ❌ | ✅ |
| Cross-Encoder 重排 | ❌ | ✅ |
| 多阶段打分 | ❌ | ✅ (6 层) |
| 作用域隔离 | ❌ | ✅ |
| 噪声过滤 | ❌ | ✅ |
| 自适应检索 | ❌ | ✅ |
| CLI 管理工具 | ❌ | ✅ |
| 会话内省 | ❌ | ✅ |

---

## 三、部署指南

### 3.1 前置检查

```bash
# 1. 检查 Node.js 版本
node --version  # >= 18

# 2. 检查 OpenClaw Gateway 状态
openclaw gateway status

# 3. 检查 Embedding 服务可用性
# Gemini:
curl -H "x-goog-api-key: $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1beta/models

# Ollama:
curl http://localhost:11434/api/tags
```

### 3.2 安装插件

```bash
# 1. 克隆仓库
cd ~/.openclaw/plugins
git clone https://github.com/win4r/memory-lancedb-pro.git

# 2. 安装依赖
cd memory-lancedb-pro
npm install

# 3. 验证插件结构
ls -la dist/
```

### 3.3 配置插件

**最小配置 (Gemini Embedding)**:
```yaml
plugins:
  load:
    paths:
      - ~/.openclaw/plugins/memory-lancedb-pro
  slots:
    memory: memory-lancedb-pro

memory-lancedb-pro:
  dbPath: ~/.openclaw/data/memory-lancedb-pro
  
  embedding:
    provider: gemini
    model: text-embedding-004
    apiKey: ${GEMINI_API_KEY}
    baseURL: https://generativelanguage.googleapis.com/v1beta
    dimensions: 768
    taskType: RETRIEVAL_DOCUMENT
  
  retrieval:
    topK: 10
    vectorWeight: 0.7
    bm25Weight: 0.3
    minScore: 0.3
    taskType: RETRIEVAL_QUERY
  
  reranker:
    enabled: false  # 初期禁用，测试稳定后启用
  
  sessionStrategy: systemSessionMemory
  autoRecall: true
  autoCapture: true
  
  mdMirror:
    enabled: true
    dir: ~/.openclaw/workspace/agents/{agentId}/memory
```

### 3.4 推荐配置 (Gemini + Ollama Rerank)

```yaml
memory-lancedb-pro:
  embedding:
    provider: gemini
    model: text-embedding-004
    apiKey: ${GEMINI_API_KEY}
    dimensions: 768
  
  reranker:
    provider: ollama
    model: bge-reranker-v2-m3
    baseURL: http://localhost:11434/v1
  
  retrieval:
    topK: 10
    vectorWeight: 0.7
    bm25Weight: 0.3
    minScore: 0.3
  
  scoring:
    recencyBoost:
      enabled: true
      halfLifeDays: 14
      weight: 0.2
    importanceWeight: 0.3
    lengthNormalization:
      enabled: true
      anchorLength: 200
    mmrDiversity:
      enabled: true
      threshold: 0.85
      penalty: 0.5
    hardMinScore: 0.3
  
  scopes:
    defaultAccess: [global, agent:self]
  
  autoRecall: true
  autoCapture: true
  mdMirror:
    enabled: true
```

### 3.5 重启服务

```bash
# 重启 Gateway
openclaw gateway restart

# 检查日志
tail -f ~/.openclaw/logs/gateway.log | grep memory-lancedb-pro
```

---

## 四、风险管理

### 4.1 API 依赖与延迟

**风险**: Rerank API 超时导致检索失败

**应对方案**:
1. **启用降级机制**: 自动降级到 cosine 排序
2. **配置超时保护**: `timeout: 3000ms`, `retries: 1`
3. **本地部署 Rerank**: 使用 Ollama 部署 `bge-reranker-v2-m3`

```yaml
reranker:
  provider: ollama
  model: bge-reranker-v2-m3
  baseURL: http://localhost:11434/v1
  timeout: 5000
  fallback: cosine
```

### 4.2 LanceDB BigInt 错误

**风险**: LanceDB 0.26+ 版本 BigInt 类型转换错误

**应对方案**:
1. 确保插件版本 > 1.0.14
2. 手动强制转换: `timestamp: Number(timestamp)`

### 4.3 记忆污染

**风险**: Auto-Capture 存入垃圾数据

**应对方案**:
1. **启用噪声过滤**:
```yaml
noiseFilter:
  enabled: true
  patterns:
    - "^I don't have"
    - "^I cannot"
    - "^HEARTBEAT"
    - "^/[a-z]+"
```

2. **调整捕获阈值**:
```yaml
autoCapture:
  minImportance: 0.5
  maxPerTurn: 2
  categories: [preference, fact, decision]
```

3. **定期清理**:
```bash
openclaw memory-lancedb-pro clean --min-score 0.3 --dry-run
openclaw memory-lancedb-pro clean --older-than 90d
```

### 4.4 作用域泄露

**风险**: 配置不当导致跨 Agent 记忆泄露

**应对方案**:
1. **默认隔离配置**:
```yaml
scopes:
  defaultAccess: [agent:self]
  globalAccess: explicit
```

2. **启用审计日志**:
```yaml
audit:
  enabled: true
  logPath: ~/.openclaw/logs/memory-audit.log
  logCrossScope: true
```

### 4.5 热更新缓存陷阱

**风险**: 修改 .ts 文件后 jiti 缓存未清空

**应对方案**:

**AI Agents 铁律** (添加到 System Prompt):
```markdown
## AI Agents 铁律

1. 修改 TypeScript 插件代码后，必须执行:
   ```bash
   rm -rf ~/.openclaw/cache/jiti
   openclaw gateway restart
   ```

2. 验证修改生效:
   ```bash
   openclaw memory-lancedb-pro version
   tail -f ~/.openclaw/logs/gateway.log | grep memory-lancedb-pro
   ```
```

---

## 五、测试验证

### 5.1 基础功能测试

```bash
# 1. 检查插件加载
openclaw gateway status | grep memory-lancedb-pro

# 2. 存储测试
openclaw memory-lancedb-pro store \
  --text "晨星喜欢使用 Gemini 和 Ollama 进行本地部署" \
  --scope agent:claude \
  --importance 0.8

# 3. 检索测试
openclaw memory-lancedb-pro recall \
  --query "晨星的部署偏好" \
  --scope agent:claude \
  --top-k 3
```

### 5.2 混合检索测试

```bash
# 存储测试数据
openclaw memory-lancedb-pro store --text "OpenClaw 是一个 AI Agent 框架"
openclaw memory-lancedb-pro store --text "LanceDB 是向量数据库"
openclaw memory-lancedb-pro store --text "Gemini 支持 Embedding API"

# Vector 检索 (语义相似)
openclaw memory-lancedb-pro recall --query "AI 框架" --vector-only

# BM25 检索 (关键词匹配)
openclaw memory-lancedb-pro recall --query "LanceDB" --bm25-only

# 混合检索
openclaw memory-lancedb-pro recall --query "向量数据库框架" --hybrid
```

### 5.3 作用域隔离测试

```bash
# 存储到不同作用域
openclaw memory-lancedb-pro store --text "Claude 专用记忆" --scope agent:claude
openclaw memory-lancedb-pro store --text "Gemini 专用记忆" --scope agent:gemini
openclaw memory-lancedb-pro store --text "全局共享记忆" --scope global

# 验证隔离 (Claude 应看不到 Gemini 的记忆)
openclaw memory-lancedb-pro recall --query "专用记忆" --scope agent:claude
```

### 5.4 性能测试

```bash
# 批量存储
for i in {1..100}; do
  openclaw memory-lancedb-pro store --text "测试记忆 $i" --scope agent:claude
done

# 检索延迟测试
time openclaw memory-lancedb-pro recall --query "测试记忆" --top-k 10

# 预期: < 500ms (无 Rerank) / < 2s (有 Rerank)

# 统计信息
openclaw memory-lancedb-pro stats
```

### 5.5 集成测试

```bash
# 完整对话流程
openclaw agent --local --agent claude << 'EOF'
你好，我是晨星。我喜欢使用 Gemini 和 Ollama 进行本地部署。
EOF

sleep 3  # 等待 Auto-Capture

openclaw agent --local --agent claude << 'EOF'
你还记得我的部署偏好吗？
EOF

# 验证响应应包含 "Gemini"、"Ollama"、"本地部署"
```

### 5.6 降级机制测试

```bash
# 模拟 Rerank 失败
# 配置错误 API Key 后重启

openclaw memory-lancedb-pro recall --query "测试" --top-k 5

# 检查日志
tail -f ~/.openclaw/logs/gateway.log | grep reranker
# 应看到 "reranker failed, fallback to cosine"
```

---

## 六、运维建议

### 6.1 日常维护

```bash
# 每周
openclaw memory-lancedb-pro stats
openclaw memory-lancedb-pro clean --min-score 0.2 --dry-run

# 每月
openclaw memory-lancedb-pro export --output ~/backups/memory-$(date +%Y%m).jsonl
openclaw memory-lancedb-pro clean --older-than 90d
```

### 6.2 监控指标

```yaml
monitoring:
  metrics:
    - retrieval_latency_p95
    - reranker_failure_rate
    - auto_capture_rate
    - scope_isolation_violations
  alerting:
    channels: [-5131273722]
    thresholds:
      retrieval_latency_p95: 2000  # ms
      reranker_failure_rate: 0.1   # 10%
```

### 6.3 故障排查

```bash
# 检查插件状态
openclaw gateway status | grep memory

# 检查日志
tail -f ~/.openclaw/logs/gateway.log | grep -E "memory|error"

# 重建索引
openclaw memory-lancedb-pro reindex --verify

# 验证配置
openclaw memory-lancedb-pro config validate
```

---

## 七、附录

### 7.1 参考资料

- LanceDB 官方文档: https://lancedb.github.io/lancedb/
- OpenClaw Plugin API: https://docs.openclaw.dev/plugins
- Jina Rerank API: https://jina.ai/rerank
- Ollama Embedding 模型: https://ollama.com/library

### 7.2 常见问题

**Q1: 检索结果不准确怎么办？**
- 调整 `vectorWeight` / `bm25Weight` 比例
- 启用 Rerank 提升准确率
- 提高 `hardMinScore` 阈值过滤低分结果

**Q2: 存储速度慢怎么办？**
- 降低 `autoCapture` 频率
- 批量存储使用 `batch-store` 命令
- 检查 Embedding API 延迟

**Q3: 内存占用过高怎么办？**
- 降低 `topK` 值
- 禁用 `memoryReflection`
- 使用轻量级 Embedding 模型

**Q4: 如何迁移现有数据？**
```bash
node dist/migrate.js \
  --source ~/.openclaw/data/memory-lancedb \
  --target ~/.openclaw/data/memory-lancedb-pro \
  --verify
```

### 7.3 配置参数速查

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `topK` | 10 | 召回数量 |
| `vectorWeight` | 0.7 | 向量检索权重 |
| `bm25Weight` | 0.3 | BM25 权重 |
| `minScore` | 0.3 | 最低分阈值 |
| `recencyBoost.halfLifeDays` | 14 | 时间半衰期 |
| `mmrDiversity.threshold` | 0.85 | MMR 相似度阈值 |

---

## 八、交付检查清单

- [x] 前置检查: Node.js, OpenClaw Gateway, Embedding 服务
- [x] 安装插件: git clone + npm install
- [x] 配置文件: ~/.openclaw/config.yaml
- [x] 重启服务: openclaw gateway restart
- [x] 功能测试: store + recall + 作用域隔离
- [x] 性能测试: 批量存储 + 检索延迟
- [x] 降级测试: Rerank 失败场景
- [x] 集成测试: Auto-Capture + Auto-Recall

**部署完成标志**:
- Gateway 日志显示 "memory-lancedb-pro loaded successfully"
- `openclaw memory-lancedb-pro stats` 返回正常统计信息
- 集成测试中 Auto-Recall 能正确召回之前的记忆
- Markdown 镜像文件正常生成

---

**文档信息**:
- 来源: 星鉴流水线 v1.2
- 生成: docs agent (minimax)
- 前置输入:
  - gemini 研究宪法
  - claude 主方案
  - review 一致性复核 (ALIGN)
