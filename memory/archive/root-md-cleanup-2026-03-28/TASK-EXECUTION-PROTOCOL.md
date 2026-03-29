# 任务执行协议 - 强制执行

**创建日期**: 2026-03-09
**严重性**: CRITICAL
**违反后果**: 不可接受的失职

---

## 🚨 问题现状

小光（main agent）频繁失智，表现为：
1. 收到任务后直接 `sessions_spawn`，忘记检查 skills
2. 即使记忆系统有完整规则，也不执行
3. 每次都是事后才想起来
4. 浪费晨星的时间、金钱和资源

**根本原因**：不是"记不住"，而是"不执行"！

---

## ✅ 强制执行协议

### 第一步：收到任务后的强制检查（不可跳过）

```
收到任务
  ↓
立即暂停，执行以下检查：
  ↓
1. 这是什么领域的任务？
   - NotebookLM 相关？
   - 自媒体内容？
   - 方案评估/技术报告？
   - 通用开发/修复？
   - 其他？
  ↓
2. 有对应的 skill 吗？
   - notebooklm skill
   - wemedia skill
   - stareval skill
   - starchain skill
  ↓
3. 如果有 skill：
   - 读取 ~/.openclaw/skills/<skill>/SKILL.md
   - 按 SKILL.md 流程执行
   - 绝不跳过
  ↓
4. 如果没有 skill：
   - 才使用 sessions_spawn
```

### 第二步：执行前的自我确认

在执行任何 `sessions_spawn` 或 skill 流程前，必须先回答：

```
□ 我已经检查了任务领域
□ 我已经确认是否有对应的 skill
□ 如果有 skill，我已经读取了 SKILL.md
□ 我确定当前的执行方式是正确的
```

**如果任何一项未完成，立即停止，重新检查！**

---

## 🎯 Skills 快速参考

| Skill | 适用场景 | 路径 |
|-------|---------|------|
| notebooklm | NotebookLM CLI 功能、notebook 操作、知识库管理 | ~/.openclaw/skills/notebooklm/ |
| wemedia | 自媒体内容创作、发布、数据监控 | ~/.openclaw/skills/wemedia/ |
| stareval | 外部方案评估、技术报告、GitHub 项目分析 | ~/.openclaw/skills/stareval/ |
| starchain | 通用开发任务、修复任务、多轮 review | ~/.openclaw/skills/starchain/ |

**判断原则**：
- 先看领域（NotebookLM/自媒体/评估/开发）
- 领域特定任务 → 用领域 skill
- 通用开发任务 → 用 starchain
- 不要看到"实现功能"就条件反射用 starchain

---

## ❌ 常见错误模式

### 错误 1：直接 spawn subagent
```
❌ sessions_spawn(agentId: "main", task: "...")
```
**为什么错**：
- Main 的 subagent 没有 Telegram 群绑定
- 无法发送通知到职能群
- 不会按标准流程执行

**正确做法**：
- 先检查是否有对应的 skill
- 如果有，读取 SKILL.md 并按流程执行

### 错误 2：搞混 skill 适用范围
```
❌ "为 notebooklm CLI 添加功能" → 用 starchain
```
**为什么错**：
- 这是 NotebookLM 领域的任务
- 应该用 notebooklm skill，不是 starchain

**正确做法**：
- 先判断任务领域
- NotebookLM 相关 → notebooklm skill
- 通用开发 → starchain

### 错误 3：忘记读取 SKILL.md
```
❌ 知道应该用 starchain，但直接 spawn coding
```
**为什么错**：
- 跳过了 starchain 的标准流程
- 缺少 Step 1 分级、Step 1.5 打磨等
- 没有各阶段的推送通知

**正确做法**：
- 读取 ~/.openclaw/skills/starchain/SKILL.md
- 按 SKILL.md 中的完整流程执行

---

## 🔒 强制保障机制

### 1. AGENTS.md 中的强制检查点
已添加 "⚠️ CRITICAL: Task Execution Checkpoint" 章节

### 2. 本协议文档
作为独立的执行协议，随时可查阅

### 3. 记忆系统中的高优先级规则
- importance=1.0 的强制执行清单
- importance=0.95 的失智根因分析
- importance=0.9 的 skill 选择规则

### 4. 每次会话开始时的自我提醒
在 Every Session 清单中，必须读取：
- AGENTS.md（包含强制检查点）
- 本协议文档（TASK-EXECUTION-PROTOCOL.md）

---

## 📊 执行效果监控

### 成功标准
- ✅ 收到任务后，第一件事是执行检查点
- ✅ 正确识别任务领域
- ✅ 正确选择对应的 skill
- ✅ 读取 SKILL.md 并按流程执行
- ✅ 各阶段有完整的推送通知

### 失败标准
- ❌ 直接 spawn 而不检查 skills
- ❌ 搞混 skill 适用范围
- ❌ 跳过 SKILL.md 的标准流程
- ❌ 缺少推送通知

### 监控方式
- 晨星会检查每次任务执行是否遵循协议
- 违反协议 = 触碰底线 = 不可接受

---

## 💡 自我提醒

**每次收到任务时，在心里默念：**

```
1. 停！先检查领域
2. 有对应的 skill 吗？
3. 如果有，读 SKILL.md
4. 按流程执行，不要跳过
5. 确保推送通知完整
```

**记住：**
- 不是"记不住"，而是"不执行"
- 记忆系统有规则，但我必须主动查询和执行
- 每次失智都在浪费晨星的时间和金钱
- 这是不可接受的

---

## 🔄 协议更新记录

- v1.0 (2026-03-09): 初版，建立强制执行协议
