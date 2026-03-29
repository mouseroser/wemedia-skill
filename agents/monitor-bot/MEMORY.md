# MEMORY.md - Monitor Bot

## 血泪教训
- 告警格式、级别定义、聚合规则属于执行手册，不应塞进 MEMORY.md。

## 错误示范 / 反模式
- 把监控模板、告警 JSON、群路由规则当成长期记忆存储。
- 用 MEMORY.md 替代 AGENTS.md 维护分级策略。

## 长期稳定规则
- MEMORY.md 只保留真正高代价、可复发的监控伤疤。
- 监控格式、分级矩阵、聚合窗口等稳定定义放 AGENTS.md / TOOLS.md。
