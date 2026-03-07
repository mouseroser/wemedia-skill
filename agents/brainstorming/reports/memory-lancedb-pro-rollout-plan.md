# Memory-LanceDB-Pro 最终落地方案

## 一、适配性评估

### 我们为什么适合用这个项目

1. **现有痛点精准匹配**
   - 当前 `MEMORY.md` 已有膨胀趋势，未来会烧 token、检索效率低
   - `memory_search` 工具已配置但不可用（404 embeddings 错误），说明向量检索需求已存在
   - 10 个子智能体协作场景下，记忆隔离和跨 scope 检索是刚需

2. **技术栈兼容**
   - 已有 LanceDB 基础设施（内置 memory-lancedb）
   - 已有 Gemini/Ollama 双路线，可灵活选择 embedding provider
   - 已有文件记忆三层架构（IDENTITY/USER/MEMORY），可平滑扩展为四层

3. **团队偏好一致**
   - NodeSeek 方案强调"可控性 > 自动化"，与晨星"重要决定需确认"的风格一致
   - 脱水打标法、Supersede 机制、人工审核闭环都符合星链流水线的门控理念

### 我们为什么需要谨慎

1. **复杂度增加**
   - 引入 embedding API 依赖（Gemini/Ollama）
   - 引入 rerank 依赖（Jina/SiliconFlow）
   - Gateway service 环境变量继承问题需要解决

2. **现有系统未完全失效**
   - 当前三层文件记忆（IDENTITY/USER/MEMORY）仍可用
   - 问题是"未来会膨胀"，不是"现在已崩溃"
   - 可以先修复 `memory_search` 配置，再决定是否升级

3. **噪音风险**
   - autoRecall 可能把无关记忆注入 context
   - autoCapture 可能把错误事实写入数据库
   - 需要严格的审核机制

---

## 二、推荐首发路线

### 选择：Gemini（优先）

**理由：**
1. **已验证可用**：织梦(gemini) agent 已稳定运行，Gemini API 连通性无问题
2. **成本可控**：Gemini embedding 免费额度充足，适合初期验证
3. **延迟可接受**：云端 API 延迟 < 500ms，对记忆检索场景足够
4. **无需本地部署**：避免 Ollama 本地模型管理和资源占用

**Ollama 作为备选：**
- Phase 2 引入，用于离线场景或成本优化
- 需要先验证 Ollama embedding 模型质量（如 `nomic-embed-text`）
- 需要评估本地资源占用（M3 MacBook Pro 内存/CPU）

---

## 三、分阶段实施路径

### Phase 0：环境修复与验证（P0，1-2 天）

**目标：** 修复现有 `memory_search` 配置，验证 embedding 能力

**任务：**
1. 排查 `404 Cannot POST /codex/embeddings` 错误
2. 配置 Gemini embedding provider（`GEMINI_API_KEY` 环境变量）
3. 验证内置 `memory-lancedb` 的 `memory_search` 工具可用
4. 测试基础向量检索功能

**启用功能：**
- 内置 `memory-lancedb` 的基础向量检索

**禁用功能：**
- BM25 全文检索
- Hybrid fusion
- Rerank
- autoRecall/autoCapture

**验收门槛：**
- `memory_search` 工具可正常返回结果
- 检索延迟 < 1s
- 无 404/500 错误

**回滚方案：**
- 保持现有 `MEMORY.md` 文件记忆，不做任何迁移

---

### Phase 1：引入 memory-lancedb-pro 基础能力（P0，3-5 天）

**目标：** 替换内置 memory-lancedb，启用 BM25 + Hybrid 检索

**任务：**
1. Clone `memory-lancedb-pro` 到 `~/.openclaw/workspace/plugins/memory-lancedb-pro`
2. 配置 `openclaw.config.json`：
   ```json
   {
     "plugins": {
       "memory-lancedb-pro": {
         "enabled": true,
         "config": {
           "embeddingProvider": "gemini",
           "autoRecall": false,
           "autoCapture": false,
           "hybridSearch": true,
           "rerankProvider": null
         }
       }
     }
   }
   ```
3. 迁移现有 `MEMORY.md` 到 LanceDB（使用 `migrate.ts`）
4. 测试 Vector + BM25 混合检索
5. 验证 scope 隔离（`global` / `agent:<id>`）

**启用功能：**
- Vector search（Gemini embedding）
- BM25 full-text search
- Hybrid fusion（RRF）
- Multi-scope isolation
- Management CLI（list/search/stats）

**禁用功能：**
- autoRecall（避免噪音注入）
- autoCapture（避免错误写入）
- Rerank（降低复杂度）
- Recency boost / MMR diversity（后续优化）

**验收门槛：**
- 混合检索准确率 > 80%（人工抽样 20 条查询）
- 检索延迟 < 1.5s
- scope 隔离正确（agent 只能访问 global + 自己的 scope）
- 无数据丢失（迁移前后记忆条数一致）

**回滚方案：**
- 禁用 `memory-lancedb-pro` 插件
- 恢复内置 `memory-lancedb`
- 从备份恢复 `MEMORY.md`

---

### Phase 2：引入 Rerank 和自适应检索（P1，5-7 天）

**目标：** 提升检索质量，引入 Jina rerank 和自适应检索

**任务：**
1. 配置 Jina rerank API（或 SiliconFlow）
2. 启用 `rerankProvider: "jina"`
3. 启用 `adaptiveRetrieval: true`
4. 启用 `recencyBoost` 和 `lengthNormalization`
5. 测试 rerank 对检索准确率的提升
6. 优化 rerank 延迟（考虑缓存）

**启用功能：**
- Cross-encoder rerank（Jina）
- Adaptive retrieval
- Recency boost
- Length normalization

**禁用功能：**
- autoRecall（仍需人工触发）
- autoCapture（仍需人工审核）
- MMR diversity（Phase 3 引入）

**验收门槛：**
- 检索准确率 > 90%（人工抽样 20 条查询）
- Rerank 延迟 < 500ms
- 总检索延迟 < 2s
- 无 rerank API 超时或限流错误

**回滚方案：**
- 禁用 `rerankProvider`
- 回退到 Phase 1 配置

---

### Phase 3：引入半自动化记忆管理（P2，7-10 天）

**目标：** 启用 autoCapture，但保留人工审核闭环

**任务：**
1. 设计"记忆提案"工作流：
   - autoCapture 触发后，记忆写入临时 staging 区
   - 每日生成"记忆提案报告"，推送到监控群
   - 晨星审核后，批量写入 Tier-1
2. 实现 Supersede 机制：
   - 写入前检索相似记忆
   - 如果是升级版，标记旧记忆为 `superseded`
3. 实现脱水打标：
   - 自动提取关键事实，打上 `[Fact]` / `[Decision]` / `[Preference]` 标签
4. 测试 autoCapture + 人工审核闭环

**启用功能：**
- autoCapture（写入 staging 区）
- Supersede 机制
- 脱水打标
- 人工审核闭环

**禁用功能：**
- autoRecall（Phase 4 引入）
- 直接写入 Tier-1（需人工审核）

**验收门槛：**
- 每日记忆提案报告准确率 > 85%
- Supersede 机制无误判（旧记忆正确标记）
- 无噪音记忆写入 Tier-1
- 晨星审核通过率 > 80%

**回滚方案：**
- 禁用 autoCapture
- 删除 staging 区记忆
- 恢复手动记忆写入

---

### Phase 4：引入 autoRecall（P2，10-14 天）

**目标：** 启用 autoRecall，但严格控制注入范围

**任务：**
1. 配置 `autoRecall: true`
2. 限制 autoRecall 的 scope：
   - 只召回 `global` + 当前 agent 的 scope
   - 禁止召回其他 agent 的私有记忆
3. 限制 autoRecall 的数量：
   - 最多注入 5 条记忆
   - 总 token 数 < 1000
4. 优化 prompt：
   - 避免模型把 `<relevant-memories>` 原样输出
   - 引导模型"理解记忆但不复述"
5. 测试 autoRecall 对任务完成率的影响

**启用功能：**
- autoRecall（受限范围）
- MMR diversity（避免重复记忆）

**禁用功能：**
- 无限制 autoRecall（避免噪音）

**验收门槛：**
- autoRecall 召回准确率 > 90%
- 无无关记忆注入
- 模型不复述 `<relevant-memories>`
- 任务完成率提升 > 10%

**回滚方案：**
- 禁用 autoRecall
- 回退到 Phase 3 配置

---

### Phase 5：引入 Ollama 备选路线（P2，14-21 天）

**目标：** 验证 Ollama 本地 embedding，作为成本优化方案

**任务：**
1. 部署 Ollama + `nomic-embed-text` 模型
2. 配置 `embeddingProvider: "ollama"`
3. 对比 Gemini vs Ollama 的检索质量
4. 对比延迟和资源占用
5. 决定是否切换到 Ollama

**启用功能：**
- Ollama embedding（备选）

**禁用功能：**
- 无（Gemini 仍可用）

**验收门槛：**
- Ollama 检索准确率 ≥ Gemini 的 95%
- 延迟 < 1s
- 本地资源占用可接受（内存 < 2GB，CPU < 20%）

**回滚方案：**
- 切换回 Gemini embedding

---

## 四、回滚方案总览

### 全局回滚策略

1. **数据备份**
   - 每次迁移前备份 `MEMORY.md` 和 LanceDB 数据库
   - 备份路径：`~/.openclaw/workspace/backups/memory-YYYYMMDD/`

2. **配置回滚**
   - 保留每个 Phase 的配置文件快照
   - 回滚时直接替换 `openclaw.config.json` + `openclaw gateway restart`

3. **数据回滚**
   - Phase 0-1：从备份恢复 `MEMORY.md`
   - Phase 2-5：从备份恢复 LanceDB 数据库

4. **紧急回滚**
   - 如果 memory-lancedb-pro 完全不可用，禁用插件，恢复纯文件记忆

---

## 五、风险与验收门槛

### 关键风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Gemini API 限流/超时 | 检索不可用 | 引入 Ollama 备选路线 |
| autoCapture 写入错误事实 | 污染数据库 | 人工审核闭环 + Supersede 机制 |
| autoRecall 注入噪音 | 降低任务完成率 | 限制召回范围和数量 |
| Rerank API 成本过高 | 预算超支 | 监控成本，必要时禁用 rerank |
| 迁移数据丢失 | 历史记忆丢失 | 每次迁移前备份 |
| Gateway 环境变量问题 | 插件无法启动 | 显式配置 API key 到 config.json |

### 验收门槛总览

| Phase | 核心指标 | 门槛 |
|-------|----------|------|
| Phase 0 | `memory_search` 可用 | 100% 成功率 |
| Phase 1 | 混合检索准确率 | > 80% |
| Phase 2 | Rerank 后准确率 | > 90% |
| Phase 3 | 记忆提案准确率 | > 85% |
| Phase 4 | autoRecall 准确率 | > 90% |
| Phase 5 | Ollama 准确率 | ≥ Gemini 的 95% |

---

## 六、最终建议

### 现在是否该进入实现？

**建议：是，但分阶段推进**

**理由：**
1. **痛点真实存在**：`MEMORY.md` 膨胀趋势明确，`memory_search` 已配置但不可用
2. **技术方案成熟**：memory-lancedb-pro 已有生产案例（NodeSeek 作者实测）
3. **风险可控**：分 5 个 Phase 推进，每个 Phase 都有回滚方案
4. **收益明确**：提升记忆检索质量，支持 10 个子智能体的记忆隔离

**执行建议：**
1. **立即启动 Phase 0**（1-2 天）：修复 `memory_search` 配置，验证 embedding 能力
2. **Phase 0 通过后启动 Phase 1**（3-5 天）：引入 memory-lancedb-pro 基础能力
3. **Phase 1 稳定运行 1 周后，决定是否进入 Phase 2**
4. **Phase 2-5 根据实际效果和成本决定是否推进**

**不建议：**
- 一次性启用所有功能（autoRecall + autoCapture + Rerank）
- 跳过 Phase 0 直接迁移到 memory-lancedb-pro
- 在未验证 Gemini embedding 可用的情况下引入 Ollama

---

## 七、下一步行动

1. **Main agent 确认方案**：晨星审核本方案，决定是否进入 Phase 0
2. **创建 Phase 0 任务清单**：由 brainstorming 产出 Phase 0 的 tasks.md
3. **分配执行 agent**：Phase 0 由 coding agent 执行，review agent 验收
4. **监控群通知**：Phase 0 启动前，推送到监控群告知团队

---

**方案产出时间：** 2026-03-06 23:19 GMT+8  
**产出节点：** Brainstorming Agent (Step 1.5)  
**上游输入：** Gemini 调研报告 + NodeSeek 方案摘要  
**下游交付：** Main agent → 晨星确认 → Phase 0 启动
