# 小红书发布版 — Claude HUD（B标）

**发布状态**: ✅ 晨星已确认
**选题级别**: S级
**创作时间**: 2026-03-22
**确认时间**: 09:51
**预计发布时间**: 即时发布

---

## 标题

HUD装完，Agent不再盲跑

---

## 正文

你有没有遇到过这种感觉：

把任务丢给 Claude Code，然后就……什么都不知道。
是在思考？还是在读文件？有没有跑偏？
光标一直在闪，但你完全不知道它在干嘛。

这种"黑盒感"是 Coding Agent 最大的痛点之一。

---

**Claude HUD 就是为了解决这个问题。**

它是一个 Claude Code 插件，在你的终端底部固定显示一条状态栏，实时告诉你：

```
[Opus | Max] │ my-project git:(main*) Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25%
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2
◐ explore [haiku]: Finding auth code (2m 15s)
▸ Fix authentication bug (2/5)
```

具体能看到什么：
• **Context 健康度**：进度条绿→黄→红，快满了一眼看出来
• **Tool 活动**：Claude 在读哪个文件、在 grep 什么、在改什么
• **Agent 状态**：哪个 subagent 在跑，在做什么事，跑了多久
• **Todo 进度**：任务完成了几个（实时更新）
• **Token 速度**：`out: 42.1 tok/s`，感受模型在不在线

300ms 刷新一次，数据来自原生 API，不是估算。

---

**3步装好：**

```
/plugin marketplace add jarrodwatts/claude-hud
/plugin install claude-hud
/claude-hud:setup
```

然后重启 Claude Code，就出现了。
想精调布局和颜色，跑 `/claude-hud:configure`。

---

**说说我自己的体验（对比视角）：**

我在用 OpenClaw 跑多 Agent 流水线——也会看子 Agent 的 session 状态。
本质上是同一个问题：我不知道 Agent 在干嘛，心里没底。

Claude HUD 解决的是"单会话内"的实时透视。
OpenClaw 的 session 监控解决的是"跨 session / 跨设备"的状态追踪（手机上也能看）。

两者互补，不冲突。

如果你在用 Claude Code，Claude HUD 值得装。
它把黑盒变成透明舱，心理安全感直接拉满。

---

10.5k stars，Mar 20 还在持续更新，社区很活跃。
GitHub: github.com/jarrodwatts/claude-hud

---

#Claude #AI编程 #CodingAgent #开发工具 #效率工具 #Claude Code

---

## 配图清单

1. 封面：Claude HUD 状态栏界面（深色终端风格）
2. 对比图：黑盒等待 vs HUD 透明监控
3. 功能展示：5个核心功能信息图
4. OpenClaw vs Claude HUD 互补说明图

---

## 发布后跟踪

- 发布后24小时内记录：阅读量、点赞、收藏、评论
- 目标：收藏率 > 点赞率（小红书价值内容核心指标）
