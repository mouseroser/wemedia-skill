# HEARTBEAT.md - Test Agent

## 健康检查

我是被 spawn 的执行 agent，不需要主动心跳检查。

当被 main agent spawn 时：
1. 读取代码
2. 执行测试套件
3. 收集结果和日志
4. 推送结果
5. 完成后自动结束
