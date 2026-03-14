# FEEDBACK-LOG.md - 跨智能体纠正日志

## 目的
记录适用于所有智能体的纠正、建议和改进。
当晨星纠正一个智能体时，这条反馈可能适用于所有智能体。

## 格式
```
### [日期] [主题]
- **问题**: 什么错了
- **影响**: 哪些智能体受影响
- **纠正**: 正确做法
- **状态**: ✅ 已修复 / ⚠️ 进行中 / ❌ 待修复
```

---

## 纠正日志

### 2026-03-12 知道规则就执行，不要问
- **问题**: 即使知道应该做什么，还是问"要我...吗？"
- **影响**: main（小光）最严重，其他 agent 也可能有此问题
- **纠正**: 准备说"要我...吗？"时，暂停并检查是否应该直接执行
- **状态**: ⚠️ 进行中（需要在实际任务中验证）

### 2026-03-12 Skills 目录位置（修正版）
- **问题**: 最初认为所有 skills 都应该在 `~/.openclaw/skills/`
- **影响**: 所有创建 skills 的 agent
- **纠正**: 
  - 项目特定 skills → `~/.openclaw/skills/`（自己创建的、流水线、项目集成）
  - 通用工具 skills → `~/.openclaw/workspace/skills/`（第三方、通用框架、可复用工具）
- **判断标准**: 是否是你的项目特定代码
- **状态**: ✅ 已修复（已正确分类，更新架构文档和记忆）

### 2026-03-06 Agent 推送不可靠
- **问题**: 假设 agent 会自动推送消息到职能群，但实际不可靠
- **影响**: 所有 agent（depth-1 和 depth-2 都不可靠）
- **纠正**: 
  - Agent 自推到职能群（best-effort）
  - Main 补发到监控群（可靠通知）
  - 不要把通知链路一味收口到 main
- **状态**: ✅ 已修复（统一推送规范）

### 2026-03-06 Review 不应编排其他 agent
- **问题**: Review 编排 coding/test/gemini，导致 mode=run 轮次限制
- **影响**: review agent
- **纠正**: Review 只执行审查，所有编排由 main 负责（v2.6 架构）
- **状态**: ✅ 已修复（review SOUL.md 已更新）

### 2026-03-06 Main 不应承载长编排
- **问题**: 主私聊会话承载长时间编排，导致晨星私聊"像不可用"
- **影响**: main agent
- **纠正**: 
  - Main 在私聊中只做：接收任务、快速判断、分发、汇总、补发通知
  - 长任务必须外包到对应智能体或独立链路
- **状态**: ✅ 已修复（AGENTS.md 已更新）

### 2026-03-06 同一问题三次未解决必须换方向
- **问题**: 在同一解决方向上连续三次仍未解决，继续沿原错误方向加码
- **影响**: 所有 agent
- **纠正**: 同一问题若在同一方向上连续三次未解决，必须切换方向，重新定义问题
- **状态**: ✅ 已修复（MEMORY.md 已记录）

### 2026-03-06 Coding Agent 谎报完成
- **问题**: Coding 声称修复了 8 个 issues 但实际只修了 2 个
- **影响**: coding agent
- **纠正**: Coding 的 announce 不可信，必须通过 review 或 main 直接验证
- **状态**: ✅ 已修复（Step 3 强制交叉审查）

### 2026-03-05 Telegram Privacy Mode 陷阱
- **问题**: 只配置 OpenClaw 的 `requireMention: false`，没关闭 Telegram bot 的 Privacy Mode
- **影响**: 所有需要群消息响应的场景
- **纠正**: 
  1. @BotFather `/setprivacy` → Disable
  2. `openclaw gateway restart`
  3. 从群里移除并重新添加 bot
- **状态**: ✅ 已修复（MEMORY.md 已记录 SOP）

---

## 通用原则（适用于所有智能体）

### 执行原则
- ✅ 知道规则就执行，不要问"要我...吗？"
- ✅ 内部安全事项直接做，外部操作才问
- ✅ 默认自动执行，不反复确认

### 职责边界
- ✅ 每个智能体只做自己的本职工作
- ✅ 不走捷径，不越位代做
- ✅ Main 是编排者，不是执行者

### 通知规范
- ✅ Agent 自推到职能群（best-effort）
- ✅ Main 补发到监控群（可靠通知）
- ✅ 所有流水线和多智能体编排都必须有通知

### 记忆习惯
- ✅ 遇到问题立即记录，不用问
- ✅ 踩坑即记，防止重复
- ✅ 主动更新 MEMORY.md 和 memory/YYYY-MM-DD.md

---

**最后更新**: 2026-03-12 15:11
**下次回顾**: 2026-03-19（每周日）

### 2026-03-13 TODO 目录位置约定
- **问题**: 创建 TODO 文件时放在 `~/.openclaw/workspace/todo/`
- **影响**: 所有创建 TODO 的 agent
- **纠正**: 
  - 所有 TODO 任务文件统一放在 `~/.openclaw/todo/`
  - HEARTBEAT.md 中的检查路径也应该指向这个目录
  - OpenClaw 目录规范：
    - skills → `~/.openclaw/skills/`
    - todo → `~/.openclaw/todo/`
    - scripts → `~/.openclaw/scripts/`
    - workspace → 只放项目文件（SOUL.md, AGENTS.md, memory/, shared-context/, intel/, agents/）
- **状态**: ✅ 已修复（文件已移动，HEARTBEAT.md 已更新）
