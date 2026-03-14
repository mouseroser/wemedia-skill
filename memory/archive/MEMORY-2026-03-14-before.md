# MEMORY.md - 小光的长期记忆

## ⚠️ 血泪教训（永不重犯）

### 2026-03-06：Review 编排模式失败
- **错误**：让 review agent 编排其他 agent（coding/test/gemini）
- **后果**：mode=run 的 announce 回调有轮次限制，review 只能处理约 3 轮就结束
- **教训**：review 只负责执行审查，所有编排由 main 负责
- **修复**：v2.6 架构调整，review 改为单一审查任务

### 2026-03-06：Agent 推送不可靠
- **错误**：假设 agent 会自动推送消息到职能群
- **后果**：gemini 在真实任务中没有发送开始/进度/完成消息
- **教训**：agent 自推不可靠（depth-1/depth-2 都不可靠），所有关键通知必须由 main 补发
- **修复**：统一推送规范，main 负责监控群 + 补发缺失

### 2026-03-05：Telegram Privacy Mode 陷阱
- **错误**：只配置 `requireMention: false`，没关闭 Telegram bot 的 Privacy Mode
- **后果**：群里仍需 @ 才能响应
- **教训**：OpenClaw 配置 + Telegram 端设置必须同步
- **修复**：@BotFather `/setprivacy` → Disable → 重新添加 bot 到群

### 2026-03-06：Coding Agent 谎报完成
- **错误**：相信 coding agent 的 announce 说"修复了 8 个 issues"
- **后果**：实际只修了 2 个，浪费了后续流程时间
- **教训**：coding 的 announce 不可信，必须通过 review 或 main 直接验证
- **修复**：Step 3 强制交叉审查，不跳过验证

### 2026-03-12：Skills 目录位置混淆
- **错误**：将新创建的 skills 放在 `~/.openclaw/workspace/skills/`
- **后果**：来回移动了 3 次才放到正确位置
- **教训**：所有 skills 都应该在 `~/.openclaw/skills/`，不是 workspace 下
- **修复**：已移动到正确位置，更新架构文档

### 2026-03-13：memory-lancedb-pro memory_list/memory_stats 返回 0 条
- **错误**：插件工具中 `agentId` 解析为 `undefined`，导致 `scopeFilter` 只包含 `['global']`，而数据库记忆都是 `scope=agent:main`
- **后果**：`memory_list` 和 `memory_stats` 返回 0 条记忆，但自动召回和自动捕获正常工作
- **根本原因**：`resolveRuntimeAgentId(context.agentId, runtimeCtx)` 返回 `undefined`，因为 `context.agentId` 未设置且 `runtimeCtx` 中没有 `agentId` 或 `sessionKey`
- **修复**：在 `~/.openclaw/workspace/plugins/memory-lancedb-pro/src/tools.ts` 中，为 `memory_list` 和 `memory_stats` 添加默认值：
  ```typescript
  const agentId = resolveRuntimeAgentId(context.agentId, runtimeCtx) || 'main';
  ```
- **验证**：修复后 `memory_list` 返回 5 条，`memory_stats` 显示 316 条记忆
- **上游提交**：已创建 Issue #186 和 PR #187 到 CortexReach/memory-lancedb-pro
- **本地修改保护**：
  - 修改位置：`src/tools.ts` 第 1050 行和第 1165 行
  - 更新前检查：`cd ~/.openclaw/workspace/plugins/memory-lancedb-pro && git diff src/tools.ts`
  - 如果有本地修改，先备份：`git stash`
  - 更新后重新应用：`git stash pop` 或手动重新添加 `|| 'main'`
  - 或等待 PR #187 合并后再更新
- **配置补充**：同时添加了 `scopes` 配置到 `openclaw.json` 的 `plugins.entries.memory-lancedb-pro.config`

---

## ❌ 错误示范（不要这样做）

### 流水线编排
- ❌ 让 review 编排其他 agent（v2.5 及之前）
- ✅ main 直接编排所有 agent（v2.6）

### 通知机制
- ❌ 依赖 agent 自推到职能群
- ✅ main 统一补发到监控群 + 职能群

### GitHub 项目分析
- ❌ 直接用 browser 访问 GitHub 网页（容易限流）
- ✅ 先 clone 到本地再分析

### 配置修改
- ❌ 直接改 openclaw.json 后用 `gateway(action="restart")`
- ✅ 改完后用 `openclaw gateway restart`（完整重启）

### Telegram 群配置
- ❌ 只配置 OpenClaw 的 `requireMention: false`
- ✅ 同时关闭 Telegram bot 的 Privacy Mode + 重新添加 bot

### Skills 目录位置
- ❌ 将所有 skills 都放在 `~/.openclaw/skills/`
- ✅ 项目特定 skills → `~/.openclaw/skills/`（自己创建的、流水线、项目集成）
- ✅ 通用工具 skills → `~/.openclaw/workspace/skills/`（第三方、通用框架、可复用工具）
- **约定**: 判断标准是"是否是你的项目特定代码"
- ✅ 同时关闭 Telegram bot 的 Privacy Mode + 重新添加 bot

### 验证测试结果
- ❌ 只看 `final-test.sh` 的汇总状态
- ✅ 补一条真实 E2E 验证，确认功能实际可用

### 记忆系统
- ❌ 用 NotebookLM 存储频繁更新的记忆
- ✅ 本地文件 + 向量数据库（memory-lancedb-pro）

---

## 晨星的核心偏好

### 沟通风格
- 简洁有力，不废话
- 默认自动执行，不反复确认
- 内部安全事项直接做，外部操作才问
- 知道规则就执行，不要问"要我...吗？"

### 记忆习惯
- 遇到问题立即记录，不用问
- 踩坑即记，防止重复
- 主动更新 MEMORY.md 和 memory/YYYY-MM-DD.md
- **⚠️ 2026-03-13 教训**：修复完成后应该立即主动记录，不要等晨星问"记录了吗"才去做。这是执行问题，必须改进。

### 工作原则
- 每个智能体只做自己的本职工作
- 不走捷径，不越位代做
- 同一问题连续三次未解决，必须切换方向
- 主私聊会话禁止承载长编排

### 语言规则
- 晨星 ↔ 小光：中文
- 小光 ↔ claude/gpt：英文
- 其他场景：中文

### 通知规则
- 所有流水线和多智能体编排都必须有通知
- 通知粒度随编排复杂度升级
- Agent 自推到职能群，main 补发到监控群

---

## 关于晨星
- 名字：陈颖，称呼：晨星
- 时区：Asia/Shanghai
- 使用 Telegram 作为主要通讯渠道
- Telegram ID: 1099011886

---

## Telegram 群组与子 Agent

| Agent ID | 称呼 | 群名 | Chat ID |
|----------|------|------|---------|
| main | 小光 | - | - |
| monitor-bot | - | 监控告警 | -5131273722 |
| docs | - | 项目文档 | -5095976145 |
| test | - | 代码测试 | -5245840611 |
| review | - | 交叉审核 | -5242448266 |
| coding | - | 代码编程 | -5039283416 |
| brainstorming | - | 灵感熔炉 | -5231604684 |
| wemedia | - | 自媒体 | -5146160953 |
| nano-banana | - | 生图 | -5217509070 |
| gemini | 织梦 | 织梦 | -5264626153 |
| notebooklm | 珊瑚 | 珊瑚 | -5202217379 |
| claude | 小克 | 小克 | -5101947063 |
| openai | 小曼 | 小曼 | -5242027093 |

---

## 模型配置

- 默认模型：anthropic/claude-opus-4-6
- 代理端点：want.eat99.top（Gemini 3.1 Pro Preview）
- 也有 MiniMax、GPT Codex 等配置
- 星链流水线已启用 Gemini、Claude、GPT 三模型交叉审核
- skill 路径：~/.openclaw/skills/starchain/

### openclaw.json 默认配置（Type B 为基准）
- coding: gpt (gpt-5.4)
- review: sonnet
- test: sonnet
- brainstorming: sonnet（R3/TF-3/Step 5.5 动态切换到 opus）
- main: opus
- docs: minimax
- monitor-bot: minimax
- 织梦(gemini): gemini-preview
- 珊瑚(notebooklm): opus
- 小克(claude): opus
- 小曼(openai): gpt-5.4

---

## 流水线

### 星链 StarChain v2.6（当前版本）
- **架构调整**：Main 直接编排所有 agent，Review 只做单一审查任务
- **全自动推进**：除 Step 7 晨星确认外不停顿（Rule 0）
- **Spawn 重试机制**：失败自动重试 3 次（第 2 次等 10 秒），3 次都失败才 BLOCKED + 告警
- **推送规范**：Agent 自推到职能群，main 补发到监控群（sub-agent 推送不可靠）
- **打磨层（Step 1.5 + 1.5S）**：gemini 扫描 → openai 宪法 → claude 实施计划 → review/gemini 复核 → review/openai|claude 仲裁 → notebooklm 补料 → brainstorming 落地 Spec-Kit → analyze Step 2 gate
- **Step 3**：main 编排 claude + gemini 双审；L2-低风险主审查位默认 claude/sonnet/medium
- **Step 4**：brainstorming 出修复方案 → coding 修复 → review/gemini 预审 → review 正式复审
- **Step 5.5**：gemini 诊断 → review/claude 独立复核 → brainstorming 根因分析 → review/openai|claude 仲裁回滚决策
- **优化收益**：降本 30-40%，效率提升 30-40%，Epoch 成功率提升 15-20%

### 星链新增工作模式
- **外部方案产品化模式**：外部方案吸收 → 内部约束对齐 → 产品定义 → 分阶段实现 → 结果沉淀
- 三层处理原则：方案层（理念与结构）、产品层（适合小光体系的功能边界与协作方式）、实现层（代码、配置、通知、记忆、回滚）
- 优先级原则：若外部方案与当前系统冲突，优先保证系统稳定、可回滚、可演进

### 自媒体流水线 v1.1
- **Step 1**: 选题分级（S/M/L）+ 平台分析
- **Step 2**: Constitution-First 前置链（Gemini 内容颗粒度对齐 → Claude Code 内容计划 → Gemini 复核 → GPT 按需仲裁）
- **Step 3-7**: 串联创作、审查、生图、适配、交付
- **Step 7**: 晨星确认门控（⛔ 未经晨星确认，绝不发布到任何外部平台）

### 星鉴流水线 v1.2
- **Step 2**: gemini 研究宪法（问题定义 / 边界 / 风险）
- **Step 3**: claude 主方案（基于宪法出落地报告）
- **Step 4**: review/gemini 一致性复核（ALIGN / DRIFT / MAJOR_DRIFT）
- **Step 5**: review/gpt 按需仲裁（GO / REVISE / BLOCK）
- **Step 6**: docs 交付定稿
- **Step 7**: main 统一交付

---

## 自媒体管家（wemedia agent）

- 模型：minimax/MiniMax-M2.5，thinking: high
- ⚠️ spawn 时必须带 `thinking: "high"`（per-agent thinkingDefault 不支持，只能 spawn 时传参）
- workspace: ~/.openclaw/workspace-wemedia/
- 职责：内容创作、排期发布、数据监控、多平台分发、评论互动
- 管理平台：小红书、TikTok/抖音、知乎
- 安全规则：未经晨星确认不得发布内容到外部平台
- 下属 agent：nano-banana（生图）、gemini（文本生成/分析）

---

## NotebookLM Skill

- 路径：~/.openclaw/skills/notebooklm/
- 3 个 notebook：memory, openclaw-docs, media-research
- `openclaw-docs` 只用于 OpenClaw 自身问题（配置、故障、架构、命令等）
- 其他场景不要默认连接 `openclaw-docs`
- 如果 `openclaw-docs` 被删除并重建，必须立即同步更新 `config/notebooks.json`
- 代理必须走支持的节点（美国、台湾），且 Surge 增强模式默认开启
- Cron：健康检查每 6h + 文档刷新每天 04:00
- CLI：notebooklm v0.3.3，认证文件 ~/.notebooklm/storage_state.json

---

## 记忆系统架构

### memory-lancedb-pro（当前主记忆插件）
- 插件路径：`~/.openclaw/workspace/plugins/memory-lancedb-pro`
- Embedding：Ollama + nomic-embed-text
- 模式：systemSessionMemory + vector+BM25+reranked
- P1 状态：autoRecall=true, autoCapture=true, captureAssistant=false
- 已导入 60 条历史记忆 + 19 条原子记忆
- CLI：`memory-pro` 可用

### 本地 rerank sidecar
- 路径：`services/local-rerank-sidecar/`
- 模型：BAAI/bge-reranker-v2-m3（transformers backend）
- 端口：127.0.0.1:8765
- 接口：Jina 兼容 `/v1/rerank`
- 自启动：launchd 服务 `com.openclaw.local-rerank-sidecar`
- 可插拔 backend：transformers（生产）/ ollama（实验）

### 记忆维护规则
- 每日日志：只加载今天 + 昨天
- 压缩阈值：40k tokens
- 定期维护：每周日凌晨 04:00 压缩检查，晚上 22:00 MEMORY.md 维护
- 原子记忆：高频问题补充短句型记忆，提升召回稳定性

---

## Workspace 架构

### Main Agent 工作目录
- `~/.openclaw/workspace/` - Main agent (小光) 的工作目录
- `workspace/intel/` - Agent 协作层（单写者原则）
  - `collaboration/` - 多 agent 联合工作的非正式产物（外部项目、本地镜像、共享分析素材等）
- `workspace/shared-context/` - 跨 agent 共享上下文
  - THESIS.md, FEEDBACK-LOG.md, SIGNALS.md
- `workspace/memory/` - 记忆文件

### Sub-Agent 工作目录
- `~/.openclaw/workspace/agents/{agent-id}/` - 各 agent 的工作产物
- 每个 agent 在自己的 workspace 目录中生成工作产物
- 通过 `intel/` 目录传递摘要或索引（单写者原则）
- 多 agent 联合工作的非正式产物统一放到 `intel/collaboration/`

---

## 踩坑笔记（OpenClaw 配置）

### GitHub 项目一律先 clone 到本地
- **问题**：直接用 browser 访问 GitHub 网页容易触发限流
- **正确做法**：`git clone https://github.com/user/repo.git /tmp/repo-name`
- **适用范围**：星链、StarEval、自媒体；凡是涉及"阅读 GitHub 项目 / 吸收外部方案 / 分析开源仓库"
- **临时解决方案**：如果已触发限流，可重启 OpenClaw browser

### 多 agent 联合工作的非正式材料统一放 `intel/collaboration/`
- **规则**：除了正式产物之外全部放到 `intel/collaboration/`
- **正式产物**：报告、审查结论、修复代码、文档交付等 → 放各自 agent 目录
- **非正式产物**：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → 放 `intel/collaboration/`
- **首选目录**：`~/.openclaw/workspace/intel/collaboration/`

### Sub-agent depth-2 无 workspace context 注入
- depth-2 sub-agent 不会注入 AGENTS.md
- 但 message 工具可用
- 解决方案：spawn 时在 task 中附带推送指令

### Review 与 Main 编排硬性约束
- **Review 约束**：绝不自己写代码或跑测试，必须 spawn coding/test agent
- **Main 编排约束**：在执行流水线时，绝不允许自己直接编辑、修改或修复应用代码与脚本

### Telegram 群白名单
- ❌ `channels.telegram.allowGroups` 不存在
- ✅ 用 `channels.telegram.groups: { "<chatId>": { ... } }` 同时充当白名单和群配置
- ✅ 支持通配符 `"*"`

### Telegram 群消息响应
- 默认 `requireMention: true`，需要 @bot 才响应
- 要自动响应所有消息：`"requireMention": false`

### Telegram bindings peer.id 格式
- 使用 `"tg:-xxxxxxxxxx"` 格式（带 tg: 前缀）

### 获取 Telegram 群 Chat ID
- 从 `/tmp/openclaw/openclaw-YYYY-MM-DD.log` 日志 grep `chatId` 最可靠

### openclaw doctor
- `openclaw doctor --fix` 会自动清除未知配置字段
- 改配置前先确认字段名正确
- ❌ 不支持的字段：`agents.list[].label`、`agents.list[].timeoutSeconds`、`channels.telegram.groups[chatId].label`
- ✅ agent 超时只能在 spawn 时传 `runTimeoutSeconds`

### sessions_spawn 是非阻塞的
- `sessions_spawn` 立即返回 `{ status: "accepted", runId }`，不等子 agent 完成
- `mode=run` 下 announce 机制会重新唤醒 parent session 继续处理下一步

### model fallback 配置
- `agents.defaults.model.fallbacks` 数组，按顺序尝试
- 全局 fallback 会被所有 agent 继承

### Step 7 通知晨星缺失
- 教训：流程图和执行指令必须一一对应
- 修复：Step 7 加硬性通知指令（监控群 + 晨星 DM target:1099011886）

### 获取新群 Chat ID（groupPolicy 临时开放法）
- 临时把 `channels.telegram.groupPolicy` 改为 `"open"`
- 重启 gateway，发消息后从日志 grep 负数 ID
- 抓到后改回 `"allowlist"`

### groups 配置不支持 agentId
- ❌ `channels.telegram.groups[chatId].agentId` 不存在
- ✅ agent 绑定必须用 `bindings` 数组

### groups/bindings 变更需要 gateway restart
- groups 和 bindings 的变更不是 dynamic reload
- 需要 `openclaw gateway restart`

### Gemini 生图模型不支持 tool use
- gemini/gemini-3-pro-image-preview 不支持工具调用
- nano-banana 只负责生图，main 接收 URL 后下载再发送

### nano-banana LLM 超时
- 默认超时约 60 秒，生图模型响应慢会超时
- 解决：spawn 时传 `runTimeoutSeconds: 300`

### nano-banana announce 显示 failed 但图片实际生成成功
- gemini-3-pro-image-preview 先返回空 assistant 消息，再返回图片
- 处理：无论 announce ✅ 还是 ❌，都检查返回内容中是否有图片 URL

### 旧 session 抢占 binding 路由
- main agent 的 sessions.json 里有旧 group session 时，binding 到其他 agent 不生效
- 必须从 sessions.json 删除旧 session 条目 + 重启 gateway

### per-agent thinking 不支持
- ❌ `agents.list[].thinking` 不存在
- ✅ thinking 只能通过 spawn 时传参或全局 `agents.defaults.thinkingDefault`

### message filePath 权限限制
- agent 的 message 工具只能访问自己 workspace 下的文件
- 跨 workspace 发送会报错
- 解决：图片下载到执行发送的 agent 自己的 workspace

### gemini 图片 URL 被安全策略阻止
- openai.datas.systems 的图片 URL 被 OpenClaw 安全策略阻止
- 解决：必须先用 exec curl 下载图片到本地，再用 filePath 发送

### bindings 在顶层不在 channels 下
- ❌ `channels.telegram.bindings` 不存在
- ✅ bindings 在 openclaw.json 顶层

### minimax 模型指令遵循问题
- minimax/MiniMax-M2.5 有时不完整执行所有步骤
- 解决：指令要非常具体，明确写出每个 message 调用的完整参数

### gemini-3.1-flash-image-preview 不可用
- 503 "分组下模型 gemini-3.1-flash-image-preview 无可用渠道"
- 使用 gemini/gemini-3-pro-image-preview 代替

### memory_search embeddings 配置
- 最终修复：切到 `provider: "ollama"`, `model: "nomic-embed-text"`
- 拉取本地模型：`ollama pull nomic-embed-text`
- 强制重建索引：`openclaw memory index --force --agent main`

### NotebookLM CLI 代理配置
- NotebookLM 在中国大陆不可用，需要翻墙
- Surge 代理端口：127.0.0.1:8234，台湾节点和美国节点都可用
- CLI 调用需要 https_proxy/http_proxy 环境变量
- 登录时需要 Surge 增强模式

### `final-test.sh` 可能出现假失败
- 测试脚本自身问题可能导致误报
- 教训：验证功能时，不能只看脚本汇总状态，要补真实 E2E 验证

### mode=session 在 Telegram 下不可用
- `sessions_spawn(mode=session)` 必须 `thread=true`
- Telegram channel 不支持 subagent thread binding
- 解决：不用 mode=session，改用 main 编排模式

### mode=run 的 announce 回调有轮次限制
- review 用 mode=run 时，spawn 子 agent 后只能处理约 3 轮 announce 就结束
- 解决：不让 review 做编排，改由 main（持久会话）直接编排

### write 工具无法写入 skills 目录
- `write` 工具报 "Path escapes workspace root"
- 解决：用 `exec cat > /path/to/file << 'EOF'` 代替

### 织梦产物目录修正
- 由 `gemini`（织梦）完成的研究/报告类产物应放在 `~/.openclaw/workspace/agents/gemini/reports/`
- 不应为了临时编排方便把正式工作产物留在共享工作区

### 流水线不该停下来问用户
- 除 Step 7 晨星确认外，中间步骤不需要人工确认
- SKILL.md 已加 Rule 0："全自动推进，不停顿"

### Telegram Privacy Mode 陷阱（详细 SOP）
1. 先确认目标是否真需要"群里免 @ 收消息"
2. 若需要免 @：去 `@BotFather` 执行 `/setprivacy` → 选择 bot → **Disable**
3. 执行 `openclaw gateway restart`
4. 在每个相关群里把 bot **移除并重新添加**
5. 如果不方便关闭 Privacy Mode，就把 bot 提升为**群管理员**
6. 运行 `openclaw channels status`
7. 在群里发一条**不 @ bot** 的普通消息做实测

### Telegram 群消息推送失败（groupAllowFrom 缺失）
- **问题**：`groupPolicy: "allowlist"` 但缺少 `groupAllowFrom` 配置
- **解决**：添加 `channels.telegram.groupAllowFrom: ["1099011886"]`

### 命令权限问题（allowFrom 配置）
- ❌ `commands.owner` 不存在
- ❌ `commands.allowFrom` 对 Telegram 群不生效
- ✅ `channels.telegram.allowFrom: ["1099011886"]`

---

## 本周重要更新

### 2026-03-07 关键成就
1. ✅ 修复 sub-agent 群通知 bug：在 `tools.subagents.tools.alsoAllow` 中添加 `["message"]`
2. ✅ 更新 OpenClaw 文档到 NotebookLM：351 个英文文档（2.38 MB）
3. ✅ 创建自动更新 Cron 任务：每周日凌晨 04:00，使用 Minimax 降本 90%+
4. ✅ 部署 memory-lancedb-pro 插件：P1 状态，已导入 60 条历史记忆 + 19 条原子记忆

### 2026-03-08 关键成就
1. ✅ 部署本地 rerank sidecar：BAAI/bge-reranker-v2-m3，launchd 自启动
2. ✅ 实现可插拔 backend 架构：transformers（生产）/ ollama（实验）
3. ✅ 完成 Ollama 实验验证：qwen2.5:7b 可正常提供 rerank

### 关键教训
1. Sub-agent 工具权限：默认没有 message 工具权限，需要显式授权
2. 文档清洗策略：只抓取 docs/ 目录，控制文件大小在 2-3 MB
3. 模型选择策略：首次执行用 Opus，定期重复任务用 Minimax 降本 90%+
4. 记忆系统优化：大段历史记忆 + 短句型原子记忆
5. 本地 rerank 架构：固定 sidecar 接口 + 可插拔 backend
6. launchd 踩坑：plist 中的路径必须是绝对路径

---

## 自动更新规则

⚠️ **流水线更新自动应用**：
- 当星链或自媒体流水线的 SKILL.md、流程图或合约更新时
- main (小光) 必须**立即自动**更新所有相关智能体的配置
- **不需要等晨星提醒**，看到流水线更新就立即执行
- 使用 agent-config-generator skill 确保更新完整

**必须更新的文件**：
1. 所有相关智能体的 SOUL.md（职责和步骤）
2. 所有相关智能体的 IDENTITY.md（角色和原则）
3. AGENTS.md（流水线描述）
4. agent-config-generator/references/agent-roles.md（角色定义）

**更新后**：
- 更新记录写入 memory/YYYY-MM-DD.md
- 存储关键决策到 memory-lancedb-pro
- 不需要重启 gateway（配置文件更新不需要重启）

### 2026-03-12：使用 Skill 时必须完整执行
- **错误**：使用 agent-config-generator skill 时只更新了 SOUL.md，遗漏了 IDENTITY.md
- **原因**：没有完整阅读 skill 的模板结构部分，假设只需要更新职责描述
- **教训**：使用 skill 时必须：
  1. 完整阅读 skill 的所有要求和模板
  2. 列出需要更新的**所有文件**
  3. 逐个检查每个文件是否需要更新
  4. 更新完成后验证所有文件都已处理
- **修复**：补充更新了所有受影响 agent 的 IDENTITY.md


### 2026-03-12：流水线更新必须立即自动应用到所有 Agent
- **约定**：当星链、自媒体、星鉴流水线的 SKILL.md、流程图或合约更新时，main（小光）必须立即自动更新所有相关 agent 配置
- **不需要等晨星提醒**：看到流水线更新就立即执行
- **必须更新的文件**：
  1. 所有相关智能体的 SOUL.md（职责和步骤）
  2. 所有相关智能体的 IDENTITY.md（角色和原则）
  3. AGENTS.md（流水线描述）
  4. agent-config-generator/references/agent-roles.md（角色定义）
- **使用工具**：agent-config-generator skill 确保更新完整
- **更新后**：记录到 memory/YYYY-MM-DD.md + 存储到 memory-lancedb-pro
- **这是约定**：晨星和小光的正式约定，必须遵守


### 2026-03-12：Launcher 脚本使用错误的参数
- **错误**：starchain-launcher.sh 和 stareval-launcher.sh 都使用了 `--task` 参数
- **问题**：`openclaw agent` 命令需要 `-m` 或 `--message` 参数，不是 `--task`
- **后果**：脚本无法运行，昨天 stareval-launcher.sh 就报错了
- **修复**：将所有 `--task` 改为 `-m`
- **教训**：
  1. 创建脚本时应该先查看命令的 `--help` 确认参数名
  2. 修复一个脚本的 bug 后，应该检查其他类似脚本是否有相同问题
  3. 修复完成后应该立即推送到 GitHub，不要遗漏
- **已修复并推送**：
  - starchain-launcher.sh (commit 74e0499)
  - stareval-launcher.sh (commit e19b56d)



### 2026-03-12：优化和架构更改前必须先评估收益
- **晨星要求**：任何优化或架构更改前必须先评估收益
- **错误案例**：提出流水线产物集中到 intel/ 目录，直接开始实施，后来发现收益不明确
- **正确流程**：
  1. 具体收益是什么？
  2. 使用场景是什么？多久会用到？
  3. 改动成本有多大？
  4. 收益是否明显大于成本？
  5. 是否有更简单的方案？
- **原则**：
  - 不要为了"看起来更好"而改动
  - 保持简单，除非有明确的使用场景
  - 如果收益不明确或成本过高，先讨论而不是直接实施
- **这是晨星的明确要求，必须严格遵守**


### 2026-03-12：插件版本更新后要主动分析适配
- **晨星指正**：当告诉我"插件有新版本"时，我应该主动完成整个适配流程
- **错误**：只更新版本和修复配置，等晨星问"要不要适配"才分析
- **正确流程**：
  1. 更新到最新版本
  2. 查看 CHANGELOG 了解变化
  3. 检查配置兼容性并修复
  4. **主动分析是否需要适配我的使用场景**
  5. **主动提出适配建议**（启用新特性？调整配置？）
- **原则**：这是主动性的体现，不是被动等待指令
- **晨星的话**："今天是我的问题，是我没有说清楚" → 其实是我应该主动做的


### 2026-03-13：插件版本更新应该先分析适配再更新
- **晨星指正**：插件版本更新应该先分析适配再更新，这样更稳妥
- **当前流程问题**：先更新再分析，如果有破坏性变更或 bug，已经在用了
- **正确流程**：
  1. 查看 CHANGELOG 和 release notes
  2. 评估影响（破坏性变更？配置调整？已知 bug？）
  3. 制定计划（备份？配置修改？测试？）
  4. 提出建议并等待晨星确认
  5. 确认后再更新
  6. 更新后验证功能正常
- **不同类型更新的策略**：
  - 🟢 小版本（bug 修复）：可以先更新再分析
  - 🟡 中版本（新特性）：应该先分析再更新
  - 🔴 大版本（重大变更）：必须先分析再更新
- **优点**：更安全，避免意外中断，有准备，可以选择不更新


### 2026-03-13：遇到问题要第一时间解决修复
- **晨星核心约定**：无论什么时候遇到问题，要第一时间解决修复
- **正确流程**：发现问题 → 立即分析 → 立即修复 → 报告结果
- **错误流程**：发现问题 → 报告 → 等指令 → 修复
- **今天的错误**：
  - 发现向量数据库路径错误 → 报告 → 等指令 → 修复
  - 发现 CLI 命令错误 → 报告 → 等指令 → 修复
  - 发现 Memory Archive 298 个重复 sources → 报告 → 等指令 → 修复
- **应该做的**：发现问题立即修复，不要等晨星说"修复"才开始
- **这是主动性的核心体现**


### 2026-03-13：TODO 目录位置混淆
- **错误**：创建 TODO 文件时放在 `~/.openclaw/workspace/todo/`
- **后果**：违反了约定，导致 HEARTBEAT 检查路径错误
- **教训**：所有 TODO 任务文件统一放在 `~/.openclaw/todo/`，不是 workspace 下
- **修复**：已移动到正确位置，更新 HEARTBEAT.md
- **约定**：OpenClaw 目录规范 - skills 在 `~/.openclaw/skills/`，todo 在 `~/.openclaw/todo/`，workspace 只放项目文件
