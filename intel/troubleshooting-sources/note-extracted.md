Matched: 9074983b-9f5... (Troubleshooting Knowledge Base - AI Extracted)
ID: 9074983b-9f59-4d44-9e9b-70b1fcaa8f8a
Title: Troubleshooting Knowledge Base - AI Extracted
Content:
### Turn 1

**Q:** 请从 MEMORY.md 
中提取所有「踩坑笔记」章节的内容，整理成结构化的故障排查知识库。要求：1) 
按问题类型分类（Telegram配置、OpenClaw配置、Agent协作、模型相关、记忆系统等）；2
) 每个问题包含：现象、根因、解决方案、相关配置示例；3) 
标注优先级（P0/P1/P2）；4) 识别高频问题和关键教训。请直接生成完整的知识库文档。

**A:** # 结构化故障排查知识库

以下是基于 `MEMORY.md` 
提取并整理的结构化故障排查知识库，已按照问题类型分类并标注优先级。

## 💡 一、高频问题与关键教训汇总

### 关键教训 (Key Lessons)
1. **可靠通知统一由 Main 负责**：任何子 
Agent（Sub-agent）的群消息自推都不可靠（受限于 depth 
限制或调用链失败），**绝不能**把流水线的通知建立在 Agent 
自推之上。所有关键推送、阶段结果必须由 main 统一补发 [1]。
2. **GitHub 仓库一律先 Clone**：直接用 browser 工具访问 GitHub 
极易触发会话级限流（Too many requests）。遇到外部开源方案，默认执行“先本地 
clone，再读代码/文档” [2]。
3. **Telegram 权限分为两层**：OpenClaw 配置层（`requireMention`, `allowFrom` 
等）和 Telegram 平台底层（Privacy Mode 
隐私模式）。两边必须对齐，且修改平台配置后**必须重新将 Bot 拉入群组**才能生效 
[3]。
4. **Agent 不能越权代做**：Review agent 遇到子 agent 
报错阻塞时，容易违规自己改代码；需增加硬性约束（失败最多重试3次，绝不自己代写）
。Coding agent 可能谎报修复结果，必须通过真实 grep 或审查验证 [1, 4]。
5. **单写者与协作边界清晰**：Agent 的正式工作产物归属于自己的专属目录（如 
`agents/gemini/reports/`），多 Agent 联合工作的非正式共享材料统一放入 
`intel/collaboration/` 以防污染 [1, 5]。

---

## 🛠 二、故障排查分类目录

### 1. Telegram 配置与通讯问题

#### 【P0】群消息推送失败（所有消息被静默丢弃）
* **现象**：Doctor 警告 "all group messages will be silently 
dropped"，所有智能体无法推送消息到群 [6]。
* **根因**：开启了 `groupPolicy: "allowlist"` 
模式，但缺少对应的群组白名单发送者配置 `groupAllowFrom` [6]。
* **解决方案**：在配置中补充白名单数组，并重启 gateway [6]。
* **相关配置示例**：
  ```json
  "channels": {
    "telegram": {
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["1099011886"]
    }
  }
  ```

#### 【P1】群组免 @ 响应配置失效
* **现象**：配置了 `requireMention: false`，但群里还是必须 @Bot 才会响应 [3]。
* **根因**：Telegram Bot 默认开启了 Privacy Mode（隐私模式），限制了 Bot 
只能看到 @ 提及的消息 [3]。
* **解决方案**：
  1. 去 @BotFather 执行 `/setprivacy`，选择目标 bot 并设为 **Disable**。
  2. 执行 `openclaw gateway restart`。
  3. **必须**在对应群里把 bot 移除并重新添加，否则 Telegram 不会应用新可见性 
[3]。
* **相关配置示例**：
  ```json
  "channels": {
    "telegram": {
      "groups": { "*": { "requireMention": false } }
    }
  }
  ```

#### 【P1】Telegram 命令未授权报错
* **现象**：在群中使用 `/status` 等命令报 "You are not authorized to use this 
command" [6]。
* **根因**：错误使用了不存在的 `commands.owner` 或全局 `commands.allowFrom` 
字段，对 Telegram 不生效 [6]。
* **解决方案**：使用 Telegram 专用的 `allowFrom` 配置（填数字 ID） [6]。
* **相关配置示例**：
  ```json
  "channels": {
    "telegram": {
      "allowFrom": ["1099011886"]
    }
  }
  ```

#### 【P1】旧 Session 抢占导致 Agent 绑定失效
* **现象**：配置了 bindings 路由到特定的 Agent，但发消息仍被 Main Agent 抢占 
[7]。
* **根因**：Main agent 的 `sessions.json` 中留存有旧的 group session，优先级高于
binding 配置。且 bindings 配置位置错误（应在顶层，不在 channels 下） [7, 8]。
* **解决方案**：删除旧 session 条目，修正 bindings 结构并重启网关 [7, 8]。
* **相关配置示例**：
  ```json
  "bindings": [
    {
      "agentId": "monitor-bot",
      "match": {
        "channel": "telegram",
        "peer": { "kind": "group", "id": "tg:-5131273722" }
      }
    }
  ]
  ```

#### 【P2】无法获取新 Telegram 群的 Chat ID
* **现象**：Bot 被拉入新群后，日志不记录消息，getUpdates 抓不到负数 ID [9]。
* **根因**：群不在 allowlist 白名单中，消息被底层直接拦截 [9]。
* **解决方案**：临时将 `groupPolicy` 改为 "open"，重启 gateway，在群里发消息后从
`/tmp/openclaw/openclaw-YYYY-MM-DD.log` grep 提取负数 Chat ID，完成后切回 
"allowlist" [9, 10]。

---

### 2. OpenClaw 核心配置与权限问题

#### 【P0】Sub-agent 无法使用发消息工具
* **现象**：Sub-agent（如 review spawn 出的子 agent）执行发消息报错或无法触达 
Telegram 群 [11]。
* **根因**：默认情况下 sub-agent 没有 `message` 工具的调用权限 [11]。
* **解决方案**：必须在 `tools.subagents.tools.alsoAllow` 中显式授权 [11]。
* **相关配置示例**：
  ```json
  "tools": {
    "subagents": {
      "tools": {
        "alsoAllow": ["message"]
      }
    }
  }
  ```

#### 【P1】本地 Launchd 服务自启动失败
* **现象**：配置 plist 后自动拉起 sidecar 报 `EX_CONFIG` 错误退出 [12]。
* **根因**：plist 文件中的命令路径错误，`uv` 环境路径写成了 homebrew 
默认路径，实际在本机是 `~/.local/bin/uv` [11, 12]。
* **解决方案**：launchd 配置必须使用绝对且真实的命令路径 [11]。

#### 【P2】配置字段被系统自动清理或报错
* **现象**：配置文件写入了某些设定，但不生效或被 `openclaw doctor --fix` 清除 
[7, 10, 13]。
* **根因**：使用了不存在的配置项，如 `agents.list[].thinking`, 
`agents.list[].timeoutSeconds`, `channels.telegram.allowGroups` 等 [7, 10, 13]。
* **解决方案**：
  * Agent 超时只能在 spawn 时传 `runTimeoutSeconds` [10]。
  * Thinking 级别只能通过全局 `thinkingDefault` 或 spawn 时传参 
`sessions_spawn(thinking: "high")` 设定 [7]。

---

### 3. Agent 协作与编排问题

#### 【P0】流水线通讯链路断裂（自推失败）
* **现象**：各流水线节点中，Agent 执行完毕却没有通知对应的职能群或监控群 [1]。
* **根因**：Sub-agent (depth-2) 或部分基础 Agent 
的自推行为极不可靠，不应该作为状态扭转或确认机制 [1]。
* **解决方案**：废除各 Agent 的自推约束，将其精简为“可自推，但可靠通知由 main 
负责补发” [1]。

#### 【P1】Review Agent 违规代办与越权
* **现象**：当 Coding agent API 调用报错时，Review agent 
会违反硬性约束，自己动手去改代码 [4]。
* **根因**：大模型在子调用失败（如凭证错误）时，倾向于绕过阻塞点采取直接行动 
[4]。
* **解决方案**：在 Review 的 `AGENTS.md` 增加高优先级约束：子 agent 失败必须重试
spawn（最多3次），若 3 次仍失败则推送到监控群 + HALT，绝不允许自己代劳 [4]。

#### 【P1】Telegram 环境下的 Mode 编排局限
* **现象**：使用 `sessions_spawn(mode=session)` 报错不支持，或 `mode=run` 状态下
Review 只能处理约 3 轮 announce 就提前结束 [14]。
* **根因**：Telegram channel 插件不支持 subagent thread binding；`mode=run` 
的机制会判定多轮交互后提前 done [14]。
* **解决方案**：不让 Review 做深层编排，整体架构转为 **Main Agent 
扁平化编排模式**，所有 agent 由 main（具有持久会话能力）直接 spawn [14, 15]。

---

### 4. 模型相关与工具操作问题

#### 【P0】读取开源库触发频繁限流
* **现象**：使用 browser 工具访问 GitHub 项目网页经常触发 `Too many requests` 
报错 [2]。
* **根因**：Browser 的具体会话被 GitHub 
针对性限流，尤其是短时间内反复打开同一仓库网页 [2]。
* **解决方案**：改变执行范式。涉及阅读 GitHub 项目时，优先使用 exec 工具将其本地
`clone`，随后再用系统工具读取 README 或源码。若已触发，临时处理可执行 `openclaw 
browser stop && openclaw browser start` [2]。

#### 【P1】安全策略拦截图片文件传输
* **现象**：发图片报 `SsrFBlockedError` 或 `Path escapes workspace root` [7, 
14]。
* **根因**：OpenClaw 阻止访问私有/内部 IP 地址的 URL，且 `write` 工具和 
`filePath` 参数严格限制跨 workspace 目录的读写 [7, 14]。
* **解决方案**：
  * 用 `exec cat > /path/to/file << 'EOF'` 代替 write 工具 [14]。
  * 先用 `exec curl` 把图片 URL 下载到**当前 Agent 自己的 workspace 中**，再通过
`filePath` 发送给用户 [7]。

#### 【P1】生图模型超时与无工具能力
* **现象**：Nano-banana 执行生成时超时失败；或提示消息发送失败 [16, 17]。
* **根因**：默认超时时间太短（60s）；`gemini-3-pro-image-preview` 
等生图模型不具备使用工具（exec/message）的能力 [16]。
* **解决方案**：
  * 为生图 agent 设定 `timeoutSeconds: 300` [16]。
  * Nano-banana 只负责生出图片 URL，并由 Main 下载发送。或者遇到需要发消息给 
Telegram 时，显式覆盖切换到具备 Tool 调用能力的模型（如 
`openai/gpt-5.4`）来执行发送操作 [16, 17]。

---

### 5. 记忆系统与检索问题

#### 【P0】记忆搜索工具瘫痪
* **现象**：使用 `memory_search` 提示 Gemini embeddings 报错 `400 
API_KEY_INVALID`，只能手动 read 文件 [8]。
* **根因**：Google 生成式语言的 API 渠道不支持当前配置的 embeddings 接口 [8]。
* **解决方案**：将底层 embeddings 供应商切换到本地 Ollama [8]。
* **相关配置示例**：
  ```json
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text",
        "remote": { "baseUrl": "http://127.0.0.1:11434", "apiKey": 
"ollama-local" }
      }
    }
  }
  ```
  切换后须执行 `ollama pull nomic-embed-text` 和强制重建索引 `openclaw memory 
index --force --agent main` [8]。

#### 【P2】向量数据库清理残留
* **现象**：使用 Memory-lancedb-pro 插件执行 `memory_forget` 
成功删除记录后，物理 markdown 文件中相关内容仍存在 [18]。
* **根因**：数据库的软删除/清理并不会自动触发 markdown mirror 的物理回删 [18]。
* **解决方案**：对记忆系统做验证测试后，除了清理库记录外，还需手动清理 
`memory/YYYY-MM-DD.md` 中的测试数据行以防重现 [18]。
