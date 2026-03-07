# OpenClaw 主智能体三层架构总览

**作者**: main (小光)
**时间**: 2026-03-06

---

## 0 层：OpenClaw 内核层（Engine Layer）

> 这层是 OpenClaw 自己的运行时状态，不属于流水线文件架构的一部分。

**位置**: `~/.openclaw/`

- `openclaw.json` / `openclaw.json.bak*` - 全局配置
- `logs/` - 网关运行日志
- `agents/main/` - main agent 的 runtime 状态
  - `agent/models.json` - 内部模型配置
  - `agent/auth-profiles.json` - 鉴权配置（可能含敏感信息）
  - `sessions/*.jsonl*` - 会话日志、reset/lock 标记
- 其他系统目录：`browser/`, `canvas/`, `cron/`, `devices/`, `skills/` 等

**特性**:
- 由 OpenClaw 守护进程自动读写
- 包含敏感信息（token、认证、内部状态）
- 不参与 NotebookLM / 向量化 / 知识库
- 不属于“主智能体的工作目录”，只在调试/排障时查看

---

## 1 层：Main Agent 工作区（Workspace Layer）

> 这里才是“主智能体的小宇宙”：人格、记忆、流水线、报告、协作。

**位置**: `~/.openclaw/workspace/`

### 1.1 身份层（Identity Layer）

- `SOUL.md` - 主智能体的灵魂、核心原则
- `IDENTITY.md` - 名称、emoji、人格描述
- `USER.md` - 关于晨星（称呼、时区、流水线确认规则）
- `AGENTS.md` - main 的角色：星链 v1.8 + 自媒体 v1.0 编排中心

### 1.2 操作层（Operations Layer）

- `HEARTBEAT.md` - 自愈检查清单（浏览器、cron、记忆维护等）
- `TOOLS.md` - 本地工具/设备的说明
- `reports/` - 报告与分析
  - `2026-03-06-verification-report.md` - 智能体配置完整性验证报告
  - `agent-directory-structure.md` - 各智能体目录结构规范
  - `architecture-overview.md` - 本文件
- `scripts/` - 可执行脚本
  - `compress-memory.sh` - 记忆压缩脚本

### 1.3 知识层（Knowledge Layer）

- `MEMORY.md` - 主智能体长期记忆（关键决策/踩坑/约定）
- `memory/YYYY-MM-DD.md` - 每日工作日志
  - 例如：`memory/2026-03-06.md`
- `shared-context/` - 跨 agent 共享上下文
  - `THESIS.md`, `FEEDBACK-LOG.md`, `SIGNALS.md`
- `intel/` - agent 协作层（单写者原则）
  - `DAILY-INTEL.md` 等协作文件
  - `collaboration/` - 多 agent 联合工作的非正式材料（外部项目、本地镜像、共享分析素材等）

### 1.4 子智能体根目录

- `agents/{agent-id}/` - 子智能体工作区根目录
  - 每个子智能体内部再使用“三层文件架构 + 专属产物目录”（见下一节）

**关键点**:
- `workspace/` 是 main 的“家”，用于定义人格、记忆和所有流水线文件
- 架构和文档、报告、脚本，全部集中在这一棵树下
- 可以安全地纳入版本控制 / NotebookLM / 日后迁移

---

## 2 层：子智能体工作区（Sub-Agent Layer）

> 每个子智能体都有自己的 mini workspace，结构类似 main，但只包含与自己相关的内容。

**位置**: `~/.openclaw/workspace/agents/{agent-id}/`

### 2.1 通用配置文件集（8 件套）

每个子智能体都有完整的配置文件集：

- `AGENTS.md` - 职责与工作流程（对齐星链 v1.8 / 自媒体 v1.0）
- `SOUL.md` - 核心身份和原则
- `USER.md` - 关于晨星（最少版本）
- `IDENTITY.md` - 名称和 emoji
- `TOOLS.md` - 工具与目录说明
- `HEARTBEAT.md` - 健康检查
- `MEMORY.md` - 该智能体自己的工作记录与踩坑
- `BOOTSTRAP.md` - 首次启动指引（读完可删）

### 2.2 专属产物目录

按照角色，为每个子智能体设计了专属目录，例如：

- `brainstorming/`：`specs/`, `reports/`, `archives/`
- `coding/`：`code/`, `patches/`, `logs/`, `archives/`
- `review/`：`reviews/`, `verdicts/`, `reports/`, `archives/`
- `test/`：`test-results/`, `logs/`, `reports/`, `archives/`
- `docs/`：`docs/`, `drafts/`, `archives/`
- `gemini/`：`reports/`, `analysis/`, `archives/`
- `notebooklm/`：`reports/`, `artifacts/`, `queries/`, `archives/`
- `wemedia/`：`drafts/`, `platforms/`, `content-calendar/`, `analytics/`, `archives/`
- `monitor-bot/`：`alerts/`, `logs/`, `reports/`, `archives/`
- `nano-banana/`：`images/`, `prompts/`, `archives/`

详见：`reports/agent-directory-structure.md`

---

## 为什么 agents/main 不能并入 workspace？

**短答案**：因为它属于“内核层”，不是“工作区层”。

- `~/.openclaw/agents/main/` 是 OpenClaw 自己的运行状态：
  - 含 session 日志、认证配置、内部模型配置
  - 由网关自动读写，可能包含敏感信息
  - 升级/实现细节可能变化
- `~/.openclaw/workspace/` 是 main 的“公开世界”：
  - 人格、记忆、流水线产物、报告、脚本
  - 用于协作、调试、版本管理、外部工具集成

如果把 `agents/main` 并入 `workspace`：

- **职责混乱**：引擎状态 vs. 流水线文件混在一起
- **安全风险**：认证配置/session 原始日志更容易被同步/分享出去
- **维护困难**：OpenClaw 内核升级时，很难保证与自定义目录调整完全兼容

因此：

> - 主智能体的“人格 + 记忆 + 产物”全部在 `workspace/` 下；
> - OpenClaw 的runtime状态留在 `agents/main/`；
> - 二者通过配置和工具交互，而不是通过合并目录。

---

## 心智模型总结

可以用三层来记：

1. **内核层（Engine Layer）** — `~/.openclaw/`
   - OpenClaw 自己的世界（配置、日志、sessions、agents/main）
2. **主智能体工作区（Main Workspace Layer）** — `~/.openclaw/workspace/`
   - 小光的世界：人格、记忆、流水线、报告、脚本、shared-context、intel
   - `intel/collaboration/` 专门用于多 agent 共读的外部 GitHub 项目与共享分析材料
3. **子智能体工作区（Sub-Agent Layer）** — `~/.openclaw/workspace/agents/{id}/`
   - 各职能 agent 的世界：各自的配置 + 工作产物

文件系统就是集成层，所有流水线、记忆和协作都在这三层之间通过文件来完成。

---

_后续如有架构调整或新增流水线，记得更新本文件。_

---

## 运行时目录约定（针对未来新智能体）

为避免再次混淆，引入硬性约束：

1. **Engine runtime 统一放在根级 `agents/{id}/` 下**  
   - 路径示例：`~/.openclaw/agents/main/{agent,sessions}`、`~/.openclaw/agents/gemini/{agent,sessions}`  
   - 内容包含：`models.json`、`auth-profiles.json`、`sessions.jsonl` 等运行时状态。

2. **Workspace 只存放“人格 + 记忆 + 产物”**  
   - 路径示例：`~/.openclaw/workspace/agents/gemini/`  
   - 内容仅限：`AGENTS/SOUL/USER/IDENTITY/TOOLS/HEARTBEAT/MEMORY/BOOTSTRAP` 和各类工作产物目录（`specs/`, `code/`, `reports/` 等）。

3. **发现 runtime 目录出现在 workspace 下时的处理流程**  
   - 立即将 `agent/`、`sessions/` 从 `~/.openclaw/workspace/agents/{id}/` 移动到 `~/.openclaw/agents/{id}/`。  
   - 在对应 agent 的 `TOOLS.md` 中保持提示：这些目录属于 OpenClaw 内核 runtime，不参与流水线，请勿修改。

4. **新建智能体时的操作规范**  
   - 只需要在 `openclaw.json` 中为该智能体设置 `workspace: "~/.openclaw/workspace/agents/{id}"`。  
   - 不手动创建 `agent/`、`sessions/`；运行时需要时，OpenClaw 会在 `~/.openclaw/agents/{id}/` 自动创建。
