# HEARTBEAT.md - 自愈检查清单

## 健康检查（每次心跳时运行）

### 浏览器状态
检查 OpenClaw 托管浏览器是否在运行：
```bash
openclaw browser status
```
如果 `running: false`，启动它：
```bash
openclaw browser start
```

### 定时任务监控
检查关键任务的 `lastRunAtMs` 是否超时（>26 小时）：
```bash
openclaw cron list
```

需要监控的任务：
- starchain 相关任务
- wemedia 相关任务
- NotebookLM 健康检查和文档刷新

如果超时，通过 CLI 强制触发：
```bash
openclaw cron trigger <task-id>
```

### 记忆维护
每周一次（周日晚上）：
1. 回顾本周 `memory/YYYY-MM-DD.md` 文件
2. 提取重要内容到 `MEMORY.md`
3. 压缩或归档超过 40k tokens 的日志
4. 更新 `shared-context/THESIS.md` 的进度

### 文件系统检查
确保关键目录存在：
- `shared-context/` (THESIS.md, FEEDBACK-LOG.md, SIGNALS.md)
- `intel/` (agent 协作文件)
- `memory/` (每日日志)

---

**故障模式记录：**
- 2026-03-05: 添加此文件，基于 Shubham Saboo 的实践经验
- （待添加：第一次遇到故障后记录在这里）

**原则：**
- 第一天不需要复杂的监控
- 在第一次遇到故障之后再建立检查
- 你会清楚地知道该监控什么，因为你已经亲身感受过什么会崩
