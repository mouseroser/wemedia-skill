# HEARTBEAT.md - Coding Agent

## 健康检查

我是被 spawn 的执行 agent，不需要主动心跳检查。

当被 main agent spawn 时：
1. 读取任务
2. 执行开发
3. 运行冒烟测试
4. 推送结果
5. 完成后自动结束
