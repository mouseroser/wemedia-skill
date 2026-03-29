# TOOLS.md - Monitor Bot

## 监控工具
- 日志分析
- 状态追踪
- 异常检测
- 告警聚合

## 告警格式
```
[P0/P1/P2/P3] 告警标题
- 时间: YYYY-MM-DD HH:MM:SS
- 流水线: 星链/自媒体
- 步骤: Step X
- Agent: agent-id
- 状态: BLOCKED/FAILED/WARNING
- 详情: ...
```

## 异常聚合规则
- 5 分钟窗口内相同异常聚合
- 避免重复告警
- 告警抑制机制

## 工作目录
- 监控日志：`~/.openclaw/workspace/agents/monitor-bot/`
- 读取状态：所有 agent 推送到监控群的消息

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
