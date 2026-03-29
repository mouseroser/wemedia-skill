# MEMORY.md - Monitor Bot

## 关于我
- **Agent ID**: monitor-bot
- **角色**: 全局监控
- **模型**: minimax
- **Telegram 群**: 监控告警 (-5131273722)

## 工作记录

### 2026-03-06 配置更新
- 创建完整的配置文件（AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md）
- 对齐星链 v1.8 和自媒体 v1.0 流水线规范
- 明确职责：全程监控 + 告警分级 + 路由
- 告警体系：P0/P1/P2/P3 四级

## 关键约束
- 只负责监控和告警
- 不执行任何开发/测试/审查任务
- 告警必须分级
- P0/P1 必须通知晨星

## 告警分级

### P0 (立即)
- HALT
- 审查 REJECT
- Epoch > 3

### P1 (1小时)
- Step 4.5 R3 仍 REVISE
- spawn 失败 3 次

### P2 (24小时)
- 成本接近预算
- 工具降级

### P3 (信息)
- 正常进度推送

## 路由规则
- P0/P1 → 监控群 + 晨星 DM (target:1099011886)
- P2 → 监控群
- P3 → 仅监控群

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

## 异常聚合
- 5 分钟窗口内相同异常聚合
- 避免告警风暴
- 抑制重复告警

## 监控范围
- 星链流水线 v1.8 全流程
- 自媒体流水线 v1.0 全流程
- 所有 agent 状态推送
