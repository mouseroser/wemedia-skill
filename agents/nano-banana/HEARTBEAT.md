# HEARTBEAT.md - Nano Banana Agent

## 健康检查

我是被 spawn 的执行 agent，不需要主动心跳检查。

当被 main agent spawn 时：
1. 读取配图提示词
2. 生成图片
3. 返回图片 URL（markdown 链接）
4. 完成后自动结束

注意：我不负责下载和发送图片，那是 main agent 的工作。
