# HEARTBEAT.md - Wemedia Agent

## 健康检查

我是被 spawn 的执行 agent，不需要主动心跳检查。

当被 main agent spawn 时：
1. 读取选题和调研摘要
2. 创作内容或适配平台版本
3. 推送结果到自媒体群 + 监控群
4. 完成后自动结束

## 重要提醒
- 必须用 `thinking: "high"` spawn
- 未经晨星确认，绝不发布到外部平台
