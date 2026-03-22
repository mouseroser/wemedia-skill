# MEMORY.md - 小光的长期记忆

> 精简版 (2026-03-22)。完整历史备份：`memory/archive/MEMORY-2026-03-14-before.md`
> 踩坑笔记完整版已存入 memory-lancedb-pro 向量数据库，按需召回。

---

## ⚠️ 血泪教训（永不重犯）

1. **Review 不做编排**：review 只负责审查，所有编排由 main 负责。mode=run 的 announce 有轮次限制。
2. **Agent 自推不可靠**：关键通知必须由 main 补发，不能依赖 sub-agent 自推到群。
3. **Coding 结果不可信**：coding 的 announce 不可信，必须通过 review 或 main 直接验证。
4. **memory-lancedb-pro 升级回归**：升级会覆盖本地补丁（`resolveRuntimeAgentId(...) || 'main'`），每次升级后必须检查 `memory_stats`/`memory_list` 是否正常。修复后需完整 `openclaw gateway restart`。
5. **AI 生成的脚本必须当场验证**：先 `openclaw <cmd> --help` 确认子命令存在，不要盲目信任 agent 生成的 CLI 命令。
6. **Cron isolated session 不查记忆**：prompt 里写死的路径必须经过验证；需要调用 memory 工具的任务不写 shell 脚本，用 agentTurn 直接调工具。
7. **三件套记录缺一不可**：完成重要工作后必须同时更新 (1) memory/YYYY-MM-DD.md (2) memory_store (3) .learnings/ERRORS.md（如有错误），不需要晨星提醒。

---

## ❌ 错误示范 → 正确做法

| 错误 | 正确 |
|------|------|
| 让 review 编排其他 agent | main 直接编排所有 agent |
| 依赖 agent 自推到群 | main 统一补发到监控群 |
| browser 访问 GitHub | 先 `git clone` 到本地 |
| 改配置后 gateway reload | 必须 `openclaw gateway restart` |
| 只配 OpenClaw requireMention | 同时关 Telegram Privacy Mode |
| skills 放 workspace 下 | 放 `~/.openclaw/skills/` |
| TODO 放 workspace 下 | 放 `~/.openclaw/todo/` |
| 说"要我...吗？" | 知道规则就直接执行 |
| 发现问题先报告等指令 | 发现问题立即修复再报告 |
| 用 openai SDK 当 HTTP 客户端 | 用原生 fetch 调本地 Ollama |
| minimax 跑复杂 cron 任务 | minimax 只跑脚本型，复杂判断用 Sonnet/Opus |
| 修改 plugins/*.ts 后直接重启 | 先 `rm -rf /tmp/jiti/` 再重启 |

---

## 晨星的核心偏好

- **沟通**：简洁有力，默认执行不反复确认
- **记录**：遇到问题/修复后立即主动记录
- **原则**：每个 agent 只做本职、不走捷径、同一问题连续三次未解决必须切换方向
- **语言**：晨星↔小光中文，对外协作按仓库语境定
- **通知**：所有流水线必须有通知，Agent 自推职能群 + main 补发监控群

---

## 关于晨星

- 陈颖，时区 Asia/Shanghai，Telegram ID: 1099011886

---

## Telegram 群组

| Agent | 称呼 | Chat ID |
|-------|------|---------|
| main | 小光 | DM |
| monitor-bot | - | -5131273722 |
| docs | - | -5095976145 |
| test | - | -5245840611 |
| review | - | -5242448266 |
| coding | - | -5039283416 |
| brainstorming | - | -5231604684 |
| wemedia | - | -5146160953 |
| nanobanana | - | -5217509070 |
| gemini | 织梦 | -5264626153 |
| notebooklm | 珊瑚 | -5202217379 |
| claude | 小克 | -5101947063 |
| openai | 小曼 | -5242027093 |

---

## 模型配置

- 默认：anthropic/claude-opus-4-6
- coding: gpt-5.4 | review/test/brainstorming: sonnet | docs/monitor-bot: minimax
- 织梦: gemini-preview | 珊瑚: opus | 小克: opus | 小曼: gpt-5.4

---

## 流水线概要

### 星链 v2.8
- Main 直接编排，Review 只做审查
- 全自动推进（Rule 0），除 Step 7 晨星确认外不停顿
- 打磨层（Step 1.5）：NotebookLM(1.5B)→OpenAI(1.5C)→Claude(1.5D)→Gemini(1.5E) 证据驱动
- Brainstorming 动态模型：L1/L2 用 sonnet，L3 用 opus，关键决策始终 opus
- Spawn 失败自动重试 3 次

### 自媒体 v1.1
- 选题分级(S/M/L) → Constitution-First → 创作 → 审查 → 生图 → 适配 → 交付
- ⛔ Step 7：未经晨星确认绝不发布

### 星鉴 v1.2
- gemini 研究宪法 → claude 主方案 → review/gemini 复核 → review/gpt 仲裁 → docs 交付

---

## 记忆系统

- **Layer 1**：MEMORY.md + memory/*.md（文件）
- **Layer 2**：memory-lancedb-pro@1.1.0-beta.8 + Ollama bge-m3 + 本地 rerank(bge-reranker-v2-m3:8765)
  - autoRecall=true, autoCapture=true, captureAssistant=true
  - Smart Extraction: openai/gpt-oss-120b（提取→去重→合并，3次LLM调用）
  - Embedding: bge-m3（本地 Ollama，1024维向量，2026-03-15 从 nomic-embed-text 切换）
  - Rerank: bge-reranker-v2-m3（本地 Python sidecar:8765，MPS加速）
- **Layer 3**：NotebookLM（memory-archive + openclaw-docs + troubleshooting）
  - layer3Fallback 配置在 openclaw.json，升级后易丢失
  - 专用 runtime worktree: `~/.openclaw/runtime-plugins/memory-lancedb-pro`
- **防护**：post-upgrade-guard.sh 每6小时 + 心跳检查，自动修复 layer3Fallback 配置丢失
- **最终架构决策**：L2 快速召回 → L3 深度推理，builtin memorySearch 不再作为第二召回层（P2.3 已关闭）
- **维护**：每日日志加载今天+昨天，压缩阈值 40k tokens，周日 04:00 压缩 + 22:00 MEMORY.md 维护

---

## Workspace 架构

- Main: `~/.openclaw/workspace/`
- Sub-agents: `~/.openclaw/workspace/agents/{agent-id}/`
- Skills: `~/.openclaw/skills/`（不是 workspace 下）
- TODO: `~/.openclaw/todo/`（不是 workspace 下）
- Scripts: `~/.openclaw/scripts/`
- 路径索引: `shared-context/PATHS.md`（所有核心路径汇总）
- Cron 总表: `shared-context/CRON-MATRIX.md`
- 协作产物: `workspace/intel/collaboration/`

---

## 核心规则

1. **流水线更新自动应用**：看到流水线更新立即更新所有相关 agent 配置，不等提醒
2. **插件更新先分析再更新**：查 CHANGELOG → 评估影响 → 制定计划 → 确认后更新
3. **OpenClaw 新版本联动**：晨星说"有新版本"→ 立即更新 openclaw-docs 笔记
4. **优化前先评估收益**：不为"看起来更好"而改动，必须有明确使用场景
5. **使用 Skill 必须完整执行**：阅读所有要求、列出所有文件、逐个更新验证
6. **约定变更后全量迁移**：修改架构/目录约定后，必须同步检查所有引用方并一次性全部迁移

---

## 上游 PR 跟进

- **PR #210** (fix/skip-claude-review-on-fork-prs): ✅ 已合并 (2026-03-15)
- **PR #206** (feat/layer3-notebooklm-fallback): CLEAN + MERGEABLE，等待 maintainer 审批（checks: version-sync ✅, cli-smoke ✅, claude-review 按 fork PR 规则跳过）
- Cron `check-memory-lancedb-pr-status` 每天 09:00 自动检查状态

---

## 本周重大事件（2026-03-16 ~ 2026-03-22）

### 自媒体 NotebookLM 信息图路线探索成功（03-22）
- NotebookLM CLI 原生支持 `generate infographic`，`--orientation square` 输出 2048x2048 正方形
- 命令：`notebooklm generate infographic --orientation square --style bento-grid --detail detailed --language zh_Hans "<prompt>"`
- 全程 CLI，无需浏览器，绕过 Gemini 下载不落盘问题
- 语言代码：`zh_Hans`（简体）/ `zh_Hant`（繁体）
- 路径约定：`agents/wemedia/drafts/generated/{A|B|C}/{文章标识}_infographic_sq.jpg`
- 流水线已更新：Step 5 从 nanobanana 改为 NotebookLM，nanobanana 降为备选

### 自媒体三篇小红书配图更新（03-21/22）
- A 篇（OpenCode 三强格局）：封面 + 信息图 v2 + 三栏对比
- B 篇（Claude HUD）：信息图 + 功能展示
- C 篇（Agent安全下篇）：信息图 v2 + 三层框架

### 自媒体 24/7 运营系统 v1 方案确立（03-18）
- 基于 Shubham Saboo X 文章的四层升级方案
- 角色映射：main=总编排, gemini=快速研究, notebooklm=深度研究, wemedia=创作

### Layer 3 NotebookLM fallback 稳定化（03-16/17）
- 根因：Ollama API IPv4/IPv6 混合 + `--session-id` 不稳定
- 修复：`nlm-gateway.sh` 改用 `nlm-ask` 内部函数绕过 session 问题
- 验证：链路已通，剩余 45s 偶发超时非 session lock

### 黄仁勋 GTC 选题（03-19）
- 成功完成系列内容生产
