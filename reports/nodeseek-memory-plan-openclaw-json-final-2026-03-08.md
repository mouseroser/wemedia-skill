# NodeSeek 方案本地化落地版 - OpenClaw JSON 架构最终部署方案

## 结论
NodeSeek 这套“三层物理记忆 + 脱水打标 + 时序防僵尸 + 人工审核”的思路，已经可以和你当前这台机器的 OpenClaw 架构对齐，而且大部分核心能力已经落地。

**当前这台机器的最终落地形态应定义为：**
- **Tier-0 权威热区**：`SOUL.md` / `IDENTITY.md` / `USER.md` / `MEMORY.md`
- **Tier-1 深度长期记忆**：`memory-lancedb-pro`（LanceDB Pro）
- **Tier-2 日志与暂存层**：`memory/YYYY-MM-DD.md`
- **治理层**：原子记忆补强 + 观察期检查单 + 回滚手册 + 人工修订

这不是纸面方案，而是已经能在当前 `openclaw.json` 上直接运行的版本。

## 一、把 NodeSeek 原方案翻译成你当前机器的架构

### 1.1 Tier-0：权威热区（Absolute Override）
NodeSeek 原文强调：身份、用户、长期记忆要成为“启动必读、不可跳过”的唯一真相来源。

落到你当前机器上，对应的是：
- `~/.openclaw/workspace/SOUL.md`
- `~/.openclaw/workspace/IDENTITY.md`
- `~/.openclaw/workspace/USER.md`
- `~/.openclaw/workspace/MEMORY.md`

而且你的 main agent 启动规则本来就已经这么设计了：
- 先读 `SOUL.md`
- 再读 `USER.md`
- 再读当天/昨天 `memory/*.md`
- 主私聊再读 `MEMORY.md`

**结论**：Tier-0 在你机器上已经存在，不需要重建，只需要继续保持“数据库记忆不得覆盖 Tier-0 文件记忆”的原则。

### 1.2 Tier-1：深度长期记忆层
NodeSeek 原方案的核心是：
- LanceDB Pro 向量数据库
- Embedding
- Hybrid Retrieval
- Rerank
- 噪声过滤
- Auto Recall

你当前机器的对应实现是：
- 运行时插件：`memory-lancedb-pro`
- 数据库路径：`~/.openclaw/memory/lancedb-pro`
- 向量模型：`nomic-embed-text`
- Embedding 通路：本地 Ollama 的 OpenAI-compatible 端点
- 检索模式：`hybrid`
- 当前状态：已启用并接管运行时 memory slot

### 1.3 Tier-2：日常流水账 / 暂存层
NodeSeek 把 `memory/YYYY-MM-DD.md` 定义为“原始对话缓存 + 等待脱水整理”的海马体层。

你当前机器上，这层已经天然存在：
- `~/.openclaw/workspace/memory/YYYY-MM-DD.md`

而且当前插件也开了 `mdMirror`，会把记忆镜像写回 Markdown。

**结论**：Tier-2 也已经存在，不需要额外另起一套系统。

## 二、当前机器的最终部署形态

## 2.1 当前已生效配置
配置文件：`/Users/lucifinil_chen/.openclaw/openclaw.json`

当前 `memory-lancedb-pro` 生效配置是：

```json
{
  "plugins": {
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "embedding": {
            "provider": "openai-compatible",
            "apiKey": "ollama-local",
            "model": "nomic-embed-text",
            "baseURL": "http://127.0.0.1:11434/v1",
            "dimensions": 768
          },
          "dbPath": "~/.openclaw/memory/lancedb-pro",
          "enableManagementTools": true,
          "sessionStrategy": "systemSessionMemory",
          "autoCapture": true,
          "autoRecall": true,
          "autoRecallMinLength": 8,
          "captureAssistant": true,
          "retrieval": {
            "rerank": "none"
          },
          "mdMirror": {
            "enabled": true,
            "dir": "memory-md"
          }
        }
      }
    },
    "slots": {
      "memory": "memory-lancedb-pro"
    }
  }
}
```

## 2.2 当前状态
按当前实机状态，已经达到：
- `Memory: enabled (plugin memory-lancedb-pro)`
- `memory-lancedb-pro` 正常加载
- `memory_store / memory_recall / memory_forget / memory_update / memory_stats / memory_list` 可用
- 插件 CLI `openclaw memory-pro` 可用
- 当前库状态：
  - `Total memories: 79`
  - `Retrieval mode: hybrid`
  - `Scope: agent:main`

## 三、对 NodeSeek 方案的本地化改写

### 3.1 你当前机器的“最终版三层记忆架构”

```text
┌──────────────────────────────────────────────────────┐
│ Tier-0  权威热区                                     │
│ SOUL.md / IDENTITY.md / USER.md / MEMORY.md          │
│ 启动必读，优先级最高，不被数据库覆盖                 │
└───────────────────────┬──────────────────────────────┘
                        │ 按需召回 / 规则约束
                        ▼
┌──────────────────────────────────────────────────────┐
│ Tier-1  深度长期记忆层                               │
│ memory-lancedb-pro + LanceDB + Ollama embeddings     │
│ autoRecall + autoCapture + hybrid retrieval          │
└───────────────────────┬──────────────────────────────┘
                        │ 镜像 / 人工整理 / 复盘
                        ▼
┌──────────────────────────────────────────────────────┐
│ Tier-2  日志与暂存层                                 │
│ memory/YYYY-MM-DD.md                                 │
│ 原始记录、流水日志、人工脱水前素材                   │
└──────────────────────────────────────────────────────┘
```

### 3.2 “脱水打标”在当前机器上的正确实现
NodeSeek 的“脱水打标”思路，在你这台机器上不应该再另起新系统，而应该对应成：

- **长篇记忆归档**：保留在 `MEMORY.md` / `memory/*.md`
- **数据库长期记忆**：导入 `memory-lancedb-pro`
- **高频问题补强**：用短句型原子记忆补齐聊天态 recall
- **人工修订**：通过 `memory_update` / `memory_forget` / `memory_list` / `memory_stats` 做治理

**这就是你当前已经验证可行的“脱水打标”实现。**

### 3.3 “时序防僵尸”在当前机器上的正确实现
NodeSeek 提到“旧知识、新知识打架”这个问题。

你当前机器上的防僵尸机制，不应该靠重新造轮子，而应该依赖这几层：
- Tier-0 权威文件优先
- `memory_update` 用于修订旧记忆，而不是一味追加
- 原子记忆优先承载高频稳定规则
- 观察期只在真实漏召回时补，不盲目加记忆
- 回滚优先回滚配置，不直接删数据库

### 3.4 “人工审核”在当前机器上的正确实现
NodeSeek 的人工审核思想，在当前机器上应落成：
- `reports/memory-observation-checklist-2026-03-07.md`
- `reports/memory-rollback-runbook-2026-03-07.md`
- `reports/memory-system-status-2026-03-07.md`
- `reports/memory-rollout-changelog-2026-03-07.md`
- `reports/memory-report-index-2026-03-07.md`

**也就是说：人工审核不是嘴上说“以后手工看”，而是已经有了操作文档和回滚路径。**

## 四、哪些地方已经完成，哪些还没做

### 4.1 已完成
- Tier-0 文件层已存在并在 main 启动路径中生效
- Tier-1 LanceDB Pro 插件已部署并接管 memory slot
- Tier-2 每日日志层已存在
- 本地 Ollama embeddings 已接通
- `memory_search` 内置链也已修复
- 历史 `MEMORY.md` 已导入 60 条以上到数据库
- 高频规则/偏好/事实已做三轮原子化补强
- 本地管理工具已启用
- `captureAssistant = true` 已启用
- `autoRecall = true` 已启用
- `autoCapture = true` 已启用
- 观察、回滚、状态、索引文档已齐

### 4.2 还没启用
只剩最后一个大块还没开：
- **P2 rerank**

原因不是没做，而是当前插件 schema 对 rerank 只支持外部 provider：
- `jina`
- `siliconflow`
- `voyage`
- `pinecone`

当前不支持：
- `ollama` 直接作为 rerank provider

因此你现在的状态是：
- **除外部 rerank 外，其他功能已全部启用**

## 五、最终部署建议

### 5.1 最终结论
如果把 NodeSeek 那篇方案改写成“适合你当前机器直接执行”的最终版本，结论就是：

- **不要重新搭一套新记忆系统**
- **直接承认当前这台机器已经落在 NodeSeek 方案的本地化完成态**
- 其中：
  - Tier-0 = 文件权威层
  - Tier-1 = `memory-lancedb-pro`
  - Tier-2 = `memory/YYYY-MM-DD.md`
  - 治理层 = 原子记忆 + 观察清单 + 回滚手册 + 人工修订

### 5.2 当前最推荐的运行姿态
当前建议维持为：
- `memory-lancedb-pro` 持续作为主运行时记忆插件
- 本地 Ollama 继续负责 embeddings
- 保持 `autoRecall = true`
- 保持 `autoCapture = true`
- 保持 `captureAssistant = true`
- 保持 `enableManagementTools = true`
- 保持 `rerank = none`
- 进入自然使用观察期

### 5.3 未来唯一值得推进的大项
如果以后要继续升级，最值得推进的是：
- 补一个外部 rerank provider 的 key
- 再从当前状态升级到真正的 P2 高质量检索模式

这一步之前，不建议再盲目加新层或新机制。

## 六、一句话总结
NodeSeek 那套“三层物理记忆”方案，在你当前这台机器上已经不是待设计状态，而是：

**Tier-0 / Tier-1 / Tier-2 三层都已经落地，当前只差外部 rerank 才算进入真正的 P2 高质量检索阶段。**
