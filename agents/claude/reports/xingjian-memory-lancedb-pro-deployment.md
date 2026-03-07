# memory-lancedb-pro 部署方案

## 一、技术分析

### 1.1 核心功能
- **混合检索引擎**: Vector (LanceDB ANN) + BM25 (FTS) 双路召回，RRF 融合策略
- **Cross-Encoder 重排**: 支持 Jina/SiliconFlow/Pinecone API，5s 超时保护 + 降级机制
- **多阶段打分流水线**: 
  - 近期提升 (Recency Boost): exp(-ageDays / halfLife) * weight
  - 重要性权重: score *= (0.7 + 0.3 * importance)
  - 长度归一化: score *= 1 / (1 + 0.5 * log2(len/anchor))
  - 时间衰减: score *= 0.5 + 0.5 * exp(-ageDays / halfLife)
  - MMR 多样性: cosine > 0.85 → 降权
  - 硬性最低分: score < threshold → 丢弃
- **多作用域隔离**: global / agent:<id> / project:<id> / user:<id> / custom:<name>
- **自适应检索**: 跳过寒暄/命令/简单确认，强制检索记忆相关关键词
- **噪声过滤**: 过滤拒绝回复、元提问、HEARTBEAT
- **会话策略**: systemSessionMemory (默认) / memoryReflection / none
- **自进化**: LEARNINGS.md / ERRORS.md / FEATURE_REQUESTS.md 钩子
- **Markdown 镜像**: 双写到 agent workspace memory/YYYY-MM-DD.md
- **Auto-Capture & Auto-Recall**: agent_end 自动提取 + before_agent_start 自动注入

### 1.2 架构依赖
```
核心依赖:
- @lancedb/lancedb >= 0.26.2 (Vector + FTS)
- openai (OpenAI-compatible embedding 抽象)
- @sinclair/typebox (Schema 验证)

外部服务:
- Embedding API: Jina / OpenAI / Gemini / Ollama
- Rerank API: Jina / SiliconFlow / Pinecone (可选)

运行环境:
- Node.js >= 18
- OpenClaw Gateway
- TypeScript 编译环境 (开发时)
```

### 1.3 与内置版本对比优势
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

## 二、环境适配

### 2.1 Gemini Embedding 适配
**现有环境**: 已配置 Gemini API，可用于 Embedding 生成

**配置方案**:
```yaml
# ~/.openclaw/config.yaml
plugins:
  load:
    paths:
      - ~/.openclaw/plugins/memory-lancedb-pro
  slots:
    memory: memory-lancedb-pro

memory-lancedb-pro:
  embedding:
    provider: gemini
    model: text-embedding-004
    apiKey: ${GEMINI_API_KEY}
    baseURL: https://generativelanguage.googleapis.com/v1beta
    dimensions: 768
    taskType: RETRIEVAL_DOCUMENT  # 存储时
  
  # 检索时使用 RETRIEVAL_QUERY
  retrieval:
    taskType: RETRIEVAL_QUERY
```

**关键点**:
- Gemini Embedding API 兼容 OpenAI SDK 格式
- `text-embedding-004` 输出 768 维向量
- 使用 `taskType` 区分存储/检索场景（提升准确率）

### 2.2 Ollama Embedding 适配
**本地部署方案**: 使用 Ollama 运行本地 Embedding 模型

**推荐模型**:
- `nomic-embed-text` (768 维, 8k context)
- `mxbai-embed-large` (1024 维, 512 context)

**配置方案**:
```yaml
memory-lancedb-pro:
  embedding:
    provider: ollama
    model: nomic-embed-text
    baseURL: http://localhost:11434/v1
    dimensions: 768
  
  # Ollama 不需要 apiKey
```

**部署步骤**:
```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 拉取 Embedding 模型
ollama pull nomic-embed-text

# 3. 验证服务
curl http://localhost:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"nomic-embed-text","input":"test"}'
```

### 2.3 Rerank 降级策略
**问题**: 现有环境可能无 Jina/SiliconFlow Rerank API

**解决方案 1: 禁用 Rerank**
```yaml
memory-lancedb-pro:
  reranker:
    enabled: false  # 完全禁用，使用 cosine 相似度排序
```

**解决方案 2: 本地 Rerank (推荐)**
```yaml
memory-lancedb-pro:
  reranker:
    provider: ollama
    model: bge-reranker-v2-m3
    baseURL: http://localhost:11434/v1
    timeout: 5000
```

部署本地 Reranker:
```bash
ollama pull bge-reranker-v2-m3
```

**解决方案 3: Gemini 模拟 Rerank**
```yaml
memory-lancedb-pro:
  reranker:
    provider: gemini-rerank  # 自定义 provider
    model: gemini-2.0-flash-exp
    apiKey: ${GEMINI_API_KEY}
    prompt: |
      Rate relevance (0-1) between query and document:
      Query: {query}
      Document: {document}
      Score:
```

## 三、部署步骤

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

# 3. 编译 TypeScript (如果需要)
npm run build

# 4. 验证插件结构
ls -la dist/  # 应包含 index.js, store.js, retriever.js 等
```

### 3.3 配置插件
```bash
# 编辑 OpenClaw 配置
nano ~/.openclaw/config.yaml
```

**最小配置 (Gemini Embedding)**:
```yaml
plugins:
  load:
    paths:
      - ~/.openclaw/plugins/memory-lancedb-pro
  slots:
    memory: memory-lancedb-pro

memory-lancedb-pro:
  # 数据库路径
  dbPath: ~/.openclaw/data/memory-lancedb-pro
  
  # Embedding 配置
  embedding:
    provider: gemini
    model: text-embedding-004
    apiKey: ${GEMINI_API_KEY}
    baseURL: https://generativelanguage.googleapis.com/v1beta
    dimensions: 768
    taskType: RETRIEVAL_DOCUMENT
  
  # 检索配置
  retrieval:
    topK: 10
    vectorWeight: 0.7
    bm25Weight: 0.3
    minScore: 0.3
    taskType: RETRIEVAL_QUERY
  
  # 禁用 Rerank (初期)
  reranker:
    enabled: false
  
  # 会话策略
  sessionStrategy: systemSessionMemory
  
  # 自动召回/捕获
  autoRecall: true
  autoCapture: true
  
  # Markdown 镜像
  mdMirror:
    enabled: true
    dir: ~/.openclaw/workspace/agents/{agentId}/memory
```

### 3.4 迁移现有数据 (可选)
```bash
# 如果之前使用内置 memory-lancedb
cd ~/.openclaw/plugins/memory-lancedb-pro

# 运行迁移工具
node dist/migrate.js \
  --source ~/.openclaw/data/memory-lancedb \
  --target ~/.openclaw/data/memory-lancedb-pro \
  --verify
```

### 3.5 重启 Gateway
```bash
# 重启以加载新插件
openclaw gateway restart

# 检查日志
tail -f ~/.openclaw/logs/gateway.log | grep memory-lancedb-pro
```

## 四、配置建议

### 4.1 打分参数调优
**场景 1: 重视时效性 (日常对话)**
```yaml
memory-lancedb-pro:
  scoring:
    recencyBoost:
      enabled: true
      halfLifeDays: 7      # 7 天半衰期
      weight: 0.3          # 30% 权重
    timeDecay:
      enabled: true
      halfLifeDays: 30     # 30 天衰减
```

**场景 2: 重视准确性 (技术文档)**
```yaml
memory-lancedb-pro:
  scoring:
    recencyBoost:
      enabled: false       # 禁用近期提升
    importanceWeight: 0.5  # 提高重要性权重
    hardMinScore: 0.5      # 提高最低分阈值
```

**场景 3: 平衡模式 (推荐)**
```yaml
memory-lancedb-pro:
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
```

### 4.2 作用域配置
**单 Agent 环境**:
```yaml
memory-lancedb-pro:
  scopes:
    default: [global, agent:claude]
```

**多 Agent 环境**:
```yaml
memory-lancedb-pro:
  scopes:
    # 每个 Agent 独立作用域
    agent:claude:
      access: [global, agent:claude, project:starchain]
    agent:gemini:
      access: [global, agent:gemini, project:starchain]
    agent:main:
      access: [global, agent:main, user:1099011886]
```

**项目隔离**:
```yaml
memory-lancedb-pro:
  scopes:
    project:starchain:
      agents: [claude, gemini, main]
      isolation: strict  # 严格隔离，不访问 global
```

### 4.3 性能优化
**高并发场景**:
```yaml
memory-lancedb-pro:
  retrieval:
    topK: 5              # 减少召回数量
    vectorWeight: 0.8    # 提高向量权重 (更快)
    bm25Weight: 0.2      # 降低 BM25 权重
  
  reranker:
    enabled: false       # 禁用 Rerank (节省延迟)
  
  adaptiveRetrieval:
    minQueryLength: 20   # 提高触发阈值
```

**低资源环境**:
```yaml
memory-lancedb-pro:
  embedding:
    provider: ollama
    model: nomic-embed-text  # 轻量级模型
  
  retrieval:
    topK: 3
  
  autoCapture: false     # 禁用自动捕获
  memoryReflection:
    enabled: false       # 禁用内省
```

## 五、风险应对

### 5.1 API 依赖与延迟
**风险**: Rerank API 超时导致检索失败

**应对方案**:
1. **启用降级机制** (已内置):
   ```typescript
   // retriever.ts 自动降级到 cosine 排序
   if (rerankerTimeout || rerankerError) {
     fallbackToCosineRerank();
   }
   ```

2. **配置超时保护**:
   ```yaml
   memory-lancedb-pro:
     reranker:
       timeout: 3000      # 3s 超时
       retries: 1         # 重试 1 次
       fallback: cosine   # 降级策略
   ```

3. **监控告警**:
   ```yaml
   memory-lancedb-pro:
     monitoring:
       rerankerFailureThreshold: 0.1  # 10% 失败率告警
       notifyChannel: -5131273722     # 监控群
   ```

### 5.2 LanceDB BigInt 错误
**风险**: LanceDB 0.26+ 版本 BigInt 类型转换错误

**应对方案**:
1. **确保插件版本 > 1.0.14**:
   ```bash
   cd ~/.openclaw/plugins/memory-lancedb-pro
   git pull origin main
   npm install
   ```

2. **手动修复 (如果需要)**:
   ```typescript
   // store.ts
   const timestamp = Date.now();
   const record = {
     ...data,
     timestamp: Number(timestamp),  // 强制转换为 Number
     createdAt: Number(timestamp)
   };
   ```

### 5.3 记忆污染
**风险**: Auto-Capture 存入垃圾数据

**应对方案**:
1. **启用噪声过滤**:
   ```yaml
   memory-lancedb-pro:
     noiseFilter:
       enabled: true
       patterns:
         - "^I don't have"
         - "^I cannot"
         - "^HEARTBEAT"
         - "^/[a-z]+"  # 过滤命令
   ```

2. **调整 Auto-Capture 阈值**:
   ```yaml
   memory-lancedb-pro:
     autoCapture:
       minImportance: 0.5     # 只捕获重要度 >= 0.5 的记忆
       maxPerTurn: 2          # 每轮最多 2 条
       categories: [preference, fact, decision]  # 限制类别
   ```

3. **定期清理**:
   ```bash
   # 删除低分记忆
   openclaw memory-lancedb-pro clean --min-score 0.3 --dry-run
   openclaw memory-lancedb-pro clean --min-score 0.3
   
   # 删除过期记忆
   openclaw memory-lancedb-pro clean --older-than 90d
   ```

### 5.4 作用域泄露
**风险**: 配置不当导致跨 Agent 记忆泄露

**应对方案**:
1. **默认隔离配置**:
   ```yaml
   memory-lancedb-pro:
     scopes:
       defaultAccess: [agent:self]  # 默认只访问自己的作用域
       globalAccess: explicit       # global 需显式授权
   ```

2. **审计日志**:
   ```yaml
   memory-lancedb-pro:
     audit:
       enabled: true
       logPath: ~/.openclaw/logs/memory-audit.log
       logCrossScope: true  # 记录跨作用域访问
   ```

3. **定期检查**:
   ```bash
   # 检查作用域配置
   openclaw memory-lancedb-pro scopes list
   
   # 检查跨作用域访问
   grep "cross-scope" ~/.openclaw/logs/memory-audit.log
   ```

### 5.5 热更新缓存陷阱
**风险**: 修改 .ts 文件后 jiti 缓存未清空

**应对方案**:
1. **强制清除缓存**:
   ```bash
   # 删除 jiti 缓存
   rm -rf ~/.openclaw/cache/jiti
   
   # 重启 Gateway
   openclaw gateway restart
   ```

2. **开发模式配置**:
   ```yaml
   # ~/.openclaw/config.yaml
   plugins:
     development:
       clearCacheOnRestart: true
       watchFiles: true
   ```

3. **AI Agents 铁律** (添加到 System Prompt):
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

## 六、测试验证

### 6.1 基础功能测试
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

# 4. 验证结果
# 应返回刚才存储的记忆，且 score > 0.5
```

### 6.2 混合检索测试
```bash
# 存储多条测试数据
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

### 6.3 作用域隔离测试
```bash
# 存储到不同作用域
openclaw memory-lancedb-pro store \
  --text "Claude 专用记忆" \
  --scope agent:claude

openclaw memory-lancedb-pro store \
  --text "Gemini 专用记忆" \
  --scope agent:gemini

openclaw memory-lancedb-pro store \
  --text "全局共享记忆" \
  --scope global

# 验证隔离
openclaw memory-lancedb-pro recall \
  --query "专用记忆" \
  --scope agent:claude
# 应只返回 Claude 和 global 的记忆，不包含 Gemini 的
```

### 6.4 自适应检索测试
```bash
# 应跳过检索的场景
echo "hi" | openclaw agent --local --agent claude
echo "/status" | openclaw agent --local --agent claude
echo "👍" | openclaw agent --local --agent claude

# 应触发检索的场景
echo "你还记得我之前说的部署偏好吗？" | openclaw agent --local --agent claude
echo "上次讨论的 LanceDB 配置是什么？" | openclaw agent --local --agent claude

# 检查日志
tail -f ~/.openclaw/logs/gateway.log | grep "adaptive-retrieval"
# 应看到 "skipped" 和 "triggered" 日志
```

### 6.5 性能测试
```bash
# 批量存储测试
for i in {1..100}; do
  openclaw memory-lancedb-pro store \
    --text "测试记忆 $i: $(date)" \
    --scope agent:claude
done

# 检索性能测试
time openclaw memory-lancedb-pro recall \
  --query "测试记忆" \
  --top-k 10

# 预期: < 500ms (无 Rerank) / < 2s (有 Rerank)

# 统计信息
openclaw memory-lancedb-pro stats
# 应显示: 总记忆数、作用域分布、平均检索时间
```

### 6.6 降级机制测试
```bash
# 模拟 Rerank API 失败
# 方法 1: 配置错误的 API Key
nano ~/.openclaw/config.yaml
# reranker.apiKey: "invalid-key"

openclaw gateway restart

# 检索测试
openclaw memory-lancedb-pro recall --query "测试" --top-k 5

# 检查日志
tail -f ~/.openclaw/logs/gateway.log | grep reranker
# 应看到 "reranker failed, fallback to cosine" 日志

# 方法 2: 禁用 Rerank
nano ~/.openclaw/config.yaml
# reranker.enabled: false

openclaw gateway restart

# 验证检索仍正常工作
openclaw memory-lancedb-pro recall --query "测试" --top-k 5
```

### 6.7 集成测试
```bash
# 完整对话流程测试
openclaw agent --local --agent claude << 'EOF'
你好，我是晨星。我喜欢使用 Gemini 和 Ollama 进行本地部署，不喜欢依赖外部 API。
EOF

# 等待 Auto-Capture 完成 (约 2-3s)
sleep 3

# 新对话测试 Auto-Recall
openclaw agent --local --agent claude << 'EOF'
你还记得我的部署偏好吗？
EOF

# 验证响应
# 应包含 "Gemini"、"Ollama"、"本地部署" 等关键词
# 且在 <relevant-memories> 标签中看到之前的记忆
```

### 6.8 Markdown 镜像验证
```bash
# 检查 Markdown 文件生成
ls -la ~/.openclaw/workspace/agents/claude/memory/

# 应看到 YYYY-MM-DD.md 文件

# 查看内容
cat ~/.openclaw/workspace/agents/claude/memory/$(date +%Y-%m-%d).md

# 应包含今天存储的所有记忆，格式如:
# ## HH:MM:SS - [scope] [importance]
# 记忆内容
# ---
```

## 七、运维建议

### 7.1 日常维护
```bash
# 每周执行
openclaw memory-lancedb-pro stats
openclaw memory-lancedb-pro clean --min-score 0.2 --dry-run

# 每月执行
openclaw memory-lancedb-pro export --output ~/backups/memory-$(date +%Y%m).jsonl
openclaw memory-lancedb-pro clean --older-than 90d
```

### 7.2 监控指标
```yaml
# 添加到监控配置
memory-lancedb-pro:
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

### 7.3 故障排查
```bash
# 检查插件状态
openclaw gateway status | grep memory

# 检查日志
tail -f ~/.openclaw/logs/gateway.log | grep -E "memory|error"

# 检查数据库
ls -lh ~/.openclaw/data/memory-lancedb-pro/

# 重建索引 (如果检索异常)
openclaw memory-lancedb-pro reindex --verify

# 验证配置
openclaw memory-lancedb-pro config validate
```

## 八、总结

### 8.1 部署清单
- [x] 前置检查: Node.js, OpenClaw Gateway, Embedding 服务
- [x] 安装插件: git clone + npm install
- [x] 配置文件: ~/.openclaw/config.yaml
- [x] 迁移数据: migrate.js (可选)
- [x] 重启服务: openclaw gateway restart
- [x] 功能测试: store + recall + 作用域隔离
- [x] 性能测试: 批量存储 + 检索延迟
- [x] 降级测试: Rerank 失败场景
- [x] 集成测试: Auto-Capture + Auto-Recall

### 8.2 关键配置
**推荐配置 (Gemini + 本地 Ollama Rerank)**:
```yaml
plugins:
  slots:
    memory: memory-lancedb-pro

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
  
  scopes:
    defaultAccess: [global, agent:self]
  
  autoRecall: true
  autoCapture: true
  mdMirror:
    enabled: true
```

### 8.3 风险缓解
1. **API 依赖**: 使用 Ollama 本地 Rerank，配置降级机制
2. **LanceDB 错误**: 确保插件版本 > 1.0.14
3. **记忆污染**: 启用噪声过滤 + 调整 Auto-Capture 阈值
4. **作用域泄露**: 默认隔离配置 + 审计日志
5. **缓存陷阱**: 添加 AI Agents 铁律到 System Prompt

### 8.4 后续优化
1. **性能调优**: 根据实际使用情况调整 topK、权重、阈值
2. **作用域策略**: 根据多 Agent 协作需求细化作用域配置
3. **自进化**: 启用 memoryReflection，积累长期知识
4. **监控告警**: 集成到现有监控系统 (监控告警群)

---

**部署完成标志**:
- Gateway 日志显示 "memory-lancedb-pro loaded successfully"
- `openclaw memory-lancedb-pro stats` 返回正常统计信息
- 集成测试中 Auto-Recall 能正确召回之前的记忆
- Markdown 镜像文件正常生成

**预计部署时间**: 30-60 分钟 (含测试验证)
