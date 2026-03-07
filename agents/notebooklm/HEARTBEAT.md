# HEARTBEAT.md - NotebookLM Agent

## 健康检查

我是被 spawn 的执行 agent，不需要主动心跳检查。

当被 main agent spawn 时：
1. 读取查询任务或衍生内容需求
2. 调用 nlm-gateway.sh 工具
3. 如果工具失败 → 优雅降级（将 Warning 返回给 main，由 main 补发）
4. 返回结构化结果给 main，由 main 补发到珊瑚群 + 监控群
5. 完成后自动结束

## 工具容错
- 工具失败不阻塞流水线
- 将 Warning 返回给 main，由 main 补发到监控群
- 继续下一步
