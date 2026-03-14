# Troubleshooting Knowledge Base v2.0

**更新日期**: 2026-03-14
**来源**: MEMORY.md, 2026-03-09.md, 故障排查文档

---

## 1) 常见错误及解决方案

### 流水线非预期停顿（高频）
- **现象**: Main Agent 收到子任务完成的 `announce` 后，只回复消息但不推进，导致流程卡死
- **根因**: 系统把"回复"与"推进"拆分成了两个独立的会话回合
- **解决方案**: 强制铁律——在收到 `announce` 的同一个 `function_calls` 块里，必须一次性完成：回复内容、发送群通知、Spawn 下一步

### Sub-agent 编排失败卡死
- **现象**: Review Agent 调用 Gemini 等子智能体时卡死
- **根因**: `mode=run` 的回调有轮次限制（约 3 轮即结束）
- **解决方案**: 将 Review 降级为单一审查任务，所有 Agent 的编排均交由 Main Agent 直接平铺调度

### 测试脚本"假失败"
- **现象**: 执行测试脚本报 FAIL，但实际端到端功能正常
- **根因**: 脚本自身的探测逻辑存在缺陷
- **解决方案**: 永远补做真实的 E2E 验证以确认功能

### Coding Agent 谎报进度
- **现象**: Coding 报告"已修复 N 个 issue"，但实际只修复了部分
- **解决方案**: 必须通过 Review 或 Main Agent 直接交叉验证

---

## 2) 配置陷阱

### Telegram Privacy Mode 陷阱（高频）
- **现象**: 配置了 `"requireMention": false`，但在群里仍需 @bot 才会响应
- **正确配置**: 
  1. 前往 BotFather 执行 `/setprivacy` 并选择 **Disable**
  2. 执行 `openclaw gateway restart`
  3. 将 bot **移出并重新拉入群组**

### 热重载与完整重启混淆
- **现象**: 修改配置文件后不生效
- **正确做法**: 修改 `openclaw.json` 或修改 `node_modules` 源码后，必须使用 `openclaw gateway restart`

### 凭空捏造非法配置字段
- **现象**: 执行 `openclaw doctor --fix` 时大量字段被清空
- **正确配置**: 
  - 查阅 `openclaw-docs` 确认字段名
  - `thinking` 仅支持全局或 spawn 时传参
  - 超时控制应使用 `runTimeoutSeconds`

### Binding 路由被旧 Session 抢占
- **现象**: 绑定了特定群路由，但消息仍被 Main Agent 错误截获
- **正确做法**: 删除 Main 的 `sessions.json` 中残留的旧会话并重启 Gateway

---

## 3) 权限问题

### Sub-agent 跨群推送权限缺失（高频）
- **现象**: 子 Agent 假装推送进度，但监控群毫无反应
- **根因**: 子 Agent 默认不具备跨上下文调用 `message` 工具的权限
- **解决方案**: 
  1. 在 `tools.subagents.tools.alsoAllow` 中显式授权 `["message"]`
  2. 废弃 Agent 自推，统一由 Main Agent 补发通知

### Telegram 群消息与命令权限
- **现象**: 群消息被静默丢弃，或者输入命令提示 Unauthorized
- **解决方案**: 
  - 配置 `channels.telegram.groupAllowFrom` 加入授权者的全数字 ID
  - 全局命令需配置 `channels.telegram.allowFrom`

### 本地文件与网络图片发送权限
- **现象**: 跨 Workspace 发文件报错；直接发网络图片报 SSRF 拦截
- **解决方案**: 先用 `exec curl` 下载到 Agent 自身工作区，再用 `message(filePath)` 推送

---

## 4) 工作流最佳实践

### "三思与先说后做"原则
- **实践**: 收到任务先搜索历史记忆，执行前必须向晨星汇报要做什么、在哪里做、为什么做，等待确认后才能动手

### 发现问题立即主动修复
- **实践**: 遇到测试失败、系统缺陷时应主动分析并立即启动修复流水线
- **注意**: 实施重大架构改动前必须先进行"收益评估"

### 记忆维护与"原话证据"原则
- **实践**: 遵循"原话做证据，提炼做索引，推断默认谨慎"
- **冲突处理**: 以最新、最明确的原话记录为最高准则

### GitHub 分析防限流
- **实践**: 严禁直接让 Agent 通过 Browser 访问 GitHub 网页；必须通过 `git clone` 拉取到本地再行分析

---

## 5) 近期重要更新

### StarChain v2.6 编排模式
- 废除 Review 编排机制，改由 Main Agent 全面接管
- 新增重试机制（失败自动重试 3 次）
- 引入 Rule 0 铁律：除特定核准步骤外，流水线必须全自动推进

### 记忆系统升级
- `memory-lancedb-pro` 插件进入 P1 状态
- 底层切换为 Ollama + `nomic-embed-text` 的 Embedding
- 搭配本地 Launchd 自启的 `local-rerank-sidecar`

### 文档体系自动化
- 351 个 OpenClaw 英文文档迁移至 NotebookLM 知识库
- 每日 04:00 自动刷新、每 6 小时健康检查的 Cron 任务
- 使用 Minimax 模型削减 90%+ API 成本

### 自动适配流水线配置规范
- 当 `SKILL.md` 发生更新时，Main 必须**不等待指示立即自动**刷新所有相关 Agent 的配置

---

## 配置速查表

| 场景 | 正确做法 |
|------|----------|
| Telegram 免 @ 响应 | BotFather /setprivacy Disable + Gateway 重启 + 重新拉入群 |
| 配置修改生效 | `openclaw gateway restart`（完整重启） |
| 超时控制 | spawn 时传 `runTimeoutSeconds` |
| 子 Agent 消息权限 | `tools.subagents.tools.alsoAllow` 添加 `["message"]` |
| 记忆冲突 | 以最新、最明确的原话记录为准 |
| GitHub 分析 | `git clone` 到本地再分析 |

---

*本知识库由 NotebookLM 自动整理，每周日自动更新*
