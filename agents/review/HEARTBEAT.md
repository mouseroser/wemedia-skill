# HEARTBEAT.md - Review Agent

## 健康检查

我是被 spawn 的执行 agent，不需要主动心跳检查。

当被 main agent spawn 时：
1. 读取代码和需求
2. 执行结构化审查
3. 产出 verdict JSON
4. 推送结果
5. 完成后自动结束
