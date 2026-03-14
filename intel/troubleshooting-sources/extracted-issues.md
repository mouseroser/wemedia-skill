# 从 MEMORY.md 提取的踩坑记录

**提取日期**: 2026-03-09
**来源**: MEMORY.md 踩坑笔记章节
**目标**: 为 troubleshooting notebook 准备初始条目

---

## 1. GitHub 项目访问限流

**现象**:
- 直接用 browser 访问 GitHub 网页容易触发限流（Too many requests）
- 短时间内反复打开同一仓库页面尤其容易触发

**根因**:
- 限流针对 OpenClaw browser 的具体会话，不是全局限流

**解决方案**:
```bash
# 优先本地 clone，再读 README / docs / 代码
git clone https://github.com/user/repo.git /tmp/repo-name
cat /tmp/repo-name/README.md
```

**临时解决方案**:
```bash
# 如果已经触发限流，重启 browser
openclaw browser stop && openclaw browser start
```

**适用范围**: 星链、StarEval、自媒体流水线

**标签**: `github`, `browser`, `rate-limit`, `workaround`

---

## 2. 多 agent 协作材料存放位置

**现象**:
- 多 agent 联合工作时，非正式材料（外部项目、临时脚本等）不知道放哪

**规则**:
- 正式产物 → 放各自 agent 目录
- 非正式产物 → 放 `intel/collaboration/`

**示例**:
```bash
# 首选目录
~/.openclaw/workspace/intel/collaboration/

# 示例
~/.openclaw/workspace/intel/collaboration/memory-lancedb-pro/
```

**边界**:
- `intel/collaboration/` 放非正式产物、共享输入、协作素材
- agent 的正式工作产物仍放各自 agent 目录

**标签**: `collaboration`, `file-organization`, `intel`

---

## 3. Sub-agent depth-2 无 workspace context

**现象**:
- depth-2 sub-agent（review spawn 的 coding/test/brainstorming/docs）不会注入 AGENTS.md
- 但 message 工具可用

**解决方案**:
- review spawn 时在 task 中附带推送指令（chat ID + message 用法）
- 每个 agent 自己推送到自己的群，review 不代劳

**标签**: `sub-agent`, `context`, `spawn`, `depth-2`

---

## 4. Telegram 群白名单配置

**错误配置**:
```json
❌ "channels.telegram.allowGroups"  // 不存在
```

**正确配置**:
```json
✅ "channels.telegram.groups": {
  "<chatId>": { ... }
}

✅ 支持通配符:
"groups": {
  "*": { "requireMention": false }
}
```

**标签**: `telegram`, `config`, `groups`, `allowlist`

---

## 5. Telegram 群消息响应配置

**默认行为**:
- `requireMention: true`，需要 @bot 才响应

**自动响应所有消息**:
```json
"requireMention": false
```

**标签**: `telegram`, `config`, `requireMention`

---

## 6. Telegram bindings peer.id 格式

**正确格式**:
```json
"tg:-xxxxxxxxxx"  // 带 tg: 前缀
```

**标签**: `telegram`, `bindings`, `format`

---

## 7. 获取 Telegram 群 Chat ID

**问题**:
- polling 模式下 getUpdates 可能为空（已被消费）

**最可靠方法**:
```bash
grep chatId /tmp/openclaw/openclaw-YYYY-MM-DD.log
```

**标签**: `telegram`, `chat-id`, `debugging`

---

## 8. openclaw doctor 自动清除未知字段

**行为**:
- `openclaw doctor --fix` 会自动清除未知配置字段

**不支持的字段**:
- ❌ `agents.list[].label`
- ❌ `agents.list[].timeoutSeconds`
- ❌ `channels.telegram.groups[chatId].label`

**正确做法**:
- ✅ agent 超时只能在 spawn 时传 `runTimeoutSeconds`

**标签**: `openclaw`, `doctor`, `config`, `validation`

---

## 9. sessions_spawn 是非阻塞的

**行为**:
- `sessions_spawn` 立即返回 `{ status: "accepted", runId }`
- 不等子 agent 完成

**流程**:
- `mode=run` 下 announce 机制会重新唤醒 parent session
- 多轮串行循环（如 Step 4 R1→R2→R3）在 mode=run 下可以工作

**标签**: `sessions`, `spawn`, `async`, `mode=run`

---

## 10. 子 agent API 失败导致 review 违规

**现象**:
- coding agent API 凭证错误时，review 会违反硬性约束自己改代码

**解决方案**:
- review AGENTS.md 加硬性约束
- 子 agent 失败必须重试 spawn（最多3次）
- 绝不自己代替
- 3次仍失败 → 推送监控群 + HALT

**标签**: `review`, `coding`, `api-failure`, `constraint`

---

## 11. model fallback 配置

**配置位置**:
```json
"agents.defaults.model.fallbacks": [...]  // 数组，按顺序尝试
```

**继承规则**:
- 全局 fallback 会被所有 agent 继承
- 单个 agent 可通过 `agents.list[].model` 覆盖

**标签**: `model`, `fallback`, `config`

---

## 12. Step 7 通知晨星缺失

**问题**:
- 流程图画了 review → main → 晨星
- 但 review AGENTS.md 没写通知指令
- 导致晨星收不到交付通知

**修复**:
- Step 7 加硬性通知指令
- 监控群 + 晨星 DM (target:1099011886)

**教训**:
- 流程图和执行指令必须一一对应

**标签**: `notification`, `step-7`, `review`, `main`

---

## 13. 获取新群 Chat ID（临时开放法）

**问题**:
- 新群没在白名单时，日志不记录消息，getUpdates 也抓不到

**解决方案**:
1. 临时把 `channels.telegram.groupPolicy` 改为 `"open"`
2. 重启 gateway
3. 发消息后从日志 grep 负数 ID
4. 抓到后改回 `"allowlist"`

**标签**: `telegram`, `chat-id`, `groupPolicy`, `workaround`

---

## 14. groups 配置不支持 agentId

**错误配置**:
```json
❌ "channels.telegram.groups[chatId].agentId"  // 不存在
```

**正确配置**:
```json
✅ 使用 bindings 数组:
{
  "agentId": "xxx",
  "match": {
    "channel": "telegram",
    "peer": {
      "kind": "group",
      "id": "tg:<chatId>"
    }
  }
}
```

**标签**: `telegram`, `groups`, `bindings`, `config`

---

## 15. groups/bindings 变更需要 restart

**行为**:
- groups 和 bindings 的变更不是 dynamic reload

**解决方案**:
```bash
openclaw gateway restart
```

**标签**: `config`, `restart`, `groups`, `bindings`

---

## 16. Gemini 生图模型不支持 tool use

**问题**:
- `gemini/gemini-3-pro-image-preview` 不支持工具调用（exec/message 等）

**解决方案**:
- nano-banana 只负责生图，返回图片 URL
- main agent 接收 URL 后下载到 workspace 再用 message 发送

**标签**: `gemini`, `image-generation`, `tool-use`, `nano-banana`

---

## 17. nano-banana LLM 超时

**问题**:
- 默认超时约 60 秒，生图模型响应慢会超时

**解决方案**:
```json
// openclaw.json
"timeoutSeconds": 300

// 或 spawn 时传参
sessions_spawn(runTimeoutSeconds: 300)
```

**标签**: `nano-banana`, `timeout`, `config`

---

## 18. nano-banana announce 显示 failed 但实际成功

**现象**:
- `gemini-3-pro-image-preview` 先返回空 assistant 消息（content=[]），再返回图片
- OpenClaw 看到空响应判定 failed，但图片实际已生成

**处理**:
- 无论 announce ✅ 还是 ❌，都检查返回内容中是否有图片 URL

**标签**: `nano-banana`, `announce`, `false-negative`

---

## 19. 旧 session 抢占 binding 路由

**问题**:
- main agent 的 sessions.json 里有旧 group session 时
- binding 到其他 agent 不生效

**解决方案**:
1. 从 sessions.json 删除旧 session 条目
2. 重启 gateway

**标签**: `sessions`, `bindings`, `routing`, `cleanup`

---

## 20. per-agent thinking 不支持

**错误配置**:
```json
❌ "agents.list[].thinking"  // 不存在
```

**正确方式**:
```javascript
// spawn 时传参
sessions_spawn(thinking: "high")

// 或全局配置
"agents.defaults.thinkingDefault"
```

**标签**: `thinking`, `config`, `spawn`

---

## 21. message filePath 权限限制

**问题**:
- agent 的 message 工具只能访问自己 workspace 下的文件
- 跨 workspace 发送会报错

**错误**:
```
"Local media path is not under an allowed directory"
```

**解决方案**:
- 图片下载到执行发送的 agent 自己的 workspace

**标签**: `message`, `filepath`, `permissions`, `workspace`

---

## 22. gemini 图片 URL 被安全策略阻止

**问题**:
- `openai.datas.systems` 的图片 URL 被 OpenClaw 安全策略阻止

**错误**:
```
SsrFBlockedError: Blocked: resolves to private/internal/special-use IP address
```

**解决方案**:
```bash
# 必须先下载到本地
curl -o /path/to/image.png <url>

# 再用 filePath 发送
message(filePath: "/path/to/image.png")
```

**标签**: `gemini`, `image`, `security`, `ssrf`

---

## 23. bindings 在顶层不在 channels 下

**错误配置**:
```json
❌ "channels.telegram.bindings"  // 不存在
```

**正确配置**:
```json
✅ 顶层:
"bindings": [
  {
    "agentId": "...",
    "match": {
      "channel": "telegram",
      "peer": {...}
    }
  }
]
```

**标签**: `bindings`, `config`, `structure`

---

## 24. minimax 模型指令遵循问题

**问题**:
- `minimax/MiniMax-M2.5` 有时不完整执行所有步骤
- 跳过发送到群的步骤

**解决方案**:
- 在 AGENTS.md 和 spawn task 中加粗强调 **必须**
- 明确写出每个 message 调用的完整参数

**教训**:
- 对 minimax 模型，指令要非常具体，不能依赖它自己推断

**标签**: `minimax`, `instruction-following`, `workaround`

---

## 25. gemini-3.1-flash-image-preview 不可用

**错误**:
```
503 "分组下模型 gemini-3.1-flash-image-preview 无可用渠道"
```

**原因**:
- 当前 API 套餐不支持该模型

**替代方案**:
```
gemini/gemini-3-pro-image-preview
```

**标签**: `gemini`, `model`, `availability`

---

## 26. memory_search embeddings API key invalid

**问题**:
- memory_search 工具报 gemini embeddings 400 API_KEY_INVALID

**根因**:
- `memorySearch.provider = "gemini"` 这条 embeddings 链不可用
- 当前聊天代理也不支持 `/embeddings`

**最终修复**:
```json
{
  "provider": "ollama",
  "model": "nomic-embed-text",
  "remote": {
    "baseUrl": "http://127.0.0.1:11434",
    "apiKey": "ollama-local"
  }
}
```

**步骤**:
```bash
# 1. 拉取模型
ollama pull nomic-embed-text

# 2. 强制重建索引
openclaw memory index --force --agent main
```

**标签**: `memory`, `embeddings`, `ollama`, `api-key`

---

## 27. memory-lancedb-pro 部署要点

**插件路径**:
```
~/.openclaw/workspace/plugins/memory-lancedb-pro
```

**当前配置**:
- Embedding: openai-compatible + Ollama
- 模型: nomic-embed-text
- sessionStrategy: systemSessionMemory
- rerank: cross-encoder (本地 sidecar)
- autoCapture: true
- autoRecall: true

**验收链路**:
```
memory_store → memory_recall → memory_forget
```

**踩坑**:
- `memory_forget` 删除数据库记录后，不会自动回删 markdown mirror
- 需手动清理 `memory/YYYY-MM-DD.md` 中的测试行

**plugins.allow 必须显式配置**:
```json
"plugins": {
  "allow": [
    "memory-lancedb-pro",
    "telegram",
    "device-pair",
    "phone-control",
    "talk-voice",
    "acpx"
  ]
}
```

**标签**: `memory`, `lancedb`, `plugin`, `deployment`

---

## 28. 本地 rerank sidecar 部署

**路径**:
```
services/local-rerank-sidecar/
```

**配置**:
- 模型: BAAI/bge-reranker-v2-m3
- Backend: transformers (生产默认)
- 端口: 127.0.0.1:8765
- 接口: Jina 兼容 `/v1/rerank`

**自启动**:
```bash
# launchd 服务
com.openclaw.local-rerank-sidecar

# 健康检查
~/.openclaw/workspace/scripts/status-local-rerank-sidecar.sh
```

**踩坑**:
- launchd plist 中的路径必须是绝对路径
- `uv` 实际在 `~/.local/bin/uv` 而不是 `/opt/homebrew/bin/uv`

**验收**:
```
memory_recall 返回 vector+BM25+reranked
```

**标签**: `rerank`, `sidecar`, `launchd`, `deployment`

---

## 29. mode=session 在 Telegram 下不可用

**问题**:
- `sessions_spawn(mode=session)` 必须 `thread=true`
- Telegram channel 不支持 subagent thread binding

**错误**:
```
"thread=true is unavailable because no channel plugin registered subagent_spawning hooks"
```

**解决方案**:
- 不用 mode=session
- 改用 main 编排模式（main 直接 spawn 所有 agent）

**标签**: `sessions`, `mode`, `telegram`, `thread`

---

## 30. mode=run 的 announce 回调有轮次限制

**问题**:
- review 用 mode=run 时，spawn 子 agent 后只能处理约 3 轮 announce 就结束
- runTimeoutSeconds 无效

**根因**:
- 问题不是超时而是 run 提前标记 done

**解决方案**:
- 不让 review 做编排
- 改由 main（持久会话）直接编排

**标签**: `mode=run`, `announce`, `limitation`

---

## 31. write 工具无法写入 skills 目录

**错误**:
```
"Path escapes workspace root"
```

**解决方案**:
```bash
exec cat > /path/to/file << 'EOF'
...
EOF
```

**标签**: `write`, `permissions`, `skills`, `workaround`

---

## 32. 织梦产物目录规范

**规则**:
- 由 `gemini`（织梦）完成的研究/报告类产物应放在:
  ```
  ~/.openclaw/workspace/agents/gemini/reports/
  ```

- 不应放在共享工作区:
  ```
  ~/.openclaw/workspace/reports/  ❌
  ```

**原则**:
- 工作产物归属 agent 自己目录
- shared workspace 只放协作与共享上下文

**标签**: `gemini`, `file-organization`, `workspace`

---

## 33. 流水线不该停下来问用户

**原则**:
- 除 Step 7 晨星确认外，中间步骤不需要人工确认
- 进度推送到监控群就够了
- 不要把进度汇报变成确认请求

**SKILL.md Rule 0**:
```
"全自动推进，不停顿"
```

**标签**: `pipeline`, `automation`, `ux`

---

## 34. coding agent 谎报修复完成

**现象**:
- coding 声称修复了 8 个 issues 但实际只修了 2 个

**教训**:
- coding 的 announce 不可信
- 必须通过 review 或 main 直接 grep 验证

**标签**: `coding`, `announce`, `verification`

---

## 35. agent 推送不可靠（通用问题）

**现象**:
- agent / sub-agent 声称推送了消息到群，但实际可能没送达
- depth-1/depth-2 以及各 agent 自推都不能假设可靠送达

**解决方案**:
- 所有流水线的关键推送、阶段结果、失败告警统一由 main 补发

**已更新**:
- 各 agent 的 AGENTS.md：把"必须推送到指定群组"改为"可自推，但可靠通知由 main 负责"

**2026-03-06 方向纠偏**:
- 问题不在"单条消息发送权限"
- 而在"真实任务链路中的自推执行/编排通知机制不可靠"
- agent 在真实任务链路中的开始/进度/成功/失败自推都不可作为可靠通知依据

**标签**: `notification`, `reliability`, `main`, `补发`

---

## 36. NotebookLM CLI 代理配置

**要求**:
- NotebookLM 在中国大陆不可用，需要翻墙

**代理配置**:
- Surge 代理端口: 127.0.0.1:8234
- 支持节点: 台湾、美国
- 不支持: 香港

**环境变量**:
```bash
https_proxy=http://127.0.0.1:8234
http_proxy=http://127.0.0.1:8234
```

**登录要求**:
- Surge 增强模式（默认开启）
- 让 Playwright 浏览器走代理

**标签**: `notebooklm`, `proxy`, `surge`, `cli`

---

## 37. Telegram Privacy Mode 导致免 @ 响应不生效

**问题**:
- 配置了 `requireMention: false`，但群里还是需要 @ 才能响应

**根因**:
- Telegram bot 的 Privacy Mode（隐私模式）默认启用
- 限制 bot 只能看到 @ 提及、命令和回复消息

**解决方案**:
1. 在 @BotFather 中发送 `/setprivacy`
2. 选择你的 bot
3. 选择 **Disable**（禁用隐私模式）
4. **重要**: 从群里移除 bot，然后重新添加
5. 执行 `openclaw gateway restart`

**替代方案**:
- 让 bot 成为群管理员（管理员可以看到所有消息）

**验证**:
```bash
openclaw channels status
openclaw channels status --probe  # 必要时
```

**教训**:
- `requireMention: false` 只是 OpenClaw 配置
- Telegram 端的 Privacy Mode 必须单独关闭
- 修改 Privacy Mode 后必须重新添加 bot 到群

**标签**: `telegram`, `privacy-mode`, `requireMention`, `botfather`

---

## 38. Telegram 群消息推送失败（groupAllowFrom 缺失）

**问题**:
- `groupPolicy: "allowlist"` 但缺少 `groupAllowFrom` 配置

**现象**:
- 所有智能体无法推送消息到群
- Doctor 警告: "all group messages will be silently dropped"

**解决方案**:
```json
"channels.telegram.groupAllowFrom": ["1099011886"]
```

**教训**:
- allowlist 模式必须配置白名单，否则所有群消息被阻止

**标签**: `telegram`, `groupAllowFrom`, `allowlist`, `config`

---

## 39. 命令权限配置错误

**问题**:
- 在智能体群中使用 `/status` 等命令报错:
  ```
  "You are not authorized to use this command"
  ```

**错误尝试**:
1. ❌ `commands.owner` (不存在)
2. ❌ `commands.allowFrom: {"*": ["telegram:1099011886"]}` (不工作)
3. ❌ `commands.allowFrom: {"*": ["1099011886", "telegram:1099011886"]}` (不工作)

**正确解决**:
```json
"channels.telegram.allowFrom": ["1099011886"]
```

**教训**:
- `commands.owner` 不存在
- `commands.allowFrom` 是全局命令授权，但对 Telegram 群不生效
- `channels.telegram.allowFrom` 是 Telegram 特定配置
- 格式: `["1099011886"]`（纯数字，不需要 "telegram:" 前缀）
- 需要重启 gateway 生效

**标签**: `telegram`, `commands`, `allowFrom`, `authorization`

---

## 总结统计

**总计**: 39 个问题条目

**分类统计**:
- Telegram 配置: 12 个
- OpenClaw 配置: 8 个
- Agent 协作: 6 个
- 模型相关: 4 个
- 记忆系统: 3 个
- 流水线: 3 个
- 文件组织: 2 个
- 其他: 1 个

**优先级建议**:
- P0 (高频/高影响): 1, 2, 8, 13, 14, 15, 35, 37, 38, 39
- P1 (中频/中影响): 3, 4, 5, 6, 7, 9, 10, 11, 16, 17, 20, 21, 26, 27, 28
- P2 (低频/低影响): 12, 18, 19, 22, 23, 24, 25, 29, 30, 31, 32, 33, 34, 36

**下一步**:
1. 将这些条目转换成标准化的 troubleshooting 模板格式
2. 创建 troubleshooting notebook
3. 上传到 NotebookLM
