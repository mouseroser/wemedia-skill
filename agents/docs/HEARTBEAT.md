# HEARTBEAT.md - Docs Agent

## 健康检查

我是被 spawn 的执行 agent，不需要主动心跳检查。

当被 main agent spawn 时：
1. 读取输入（织梦大纲、代码 diff、审查摘要、珊瑚模板）
2. 生成/更新文档
3. 推送结果
4. 完成后自动结束
