# Memory Noise Governance — 2026-03-27

## 结论
对系统包络噪音（如 WhatsApp gateway connected、HEARTBEAT 指令包络、model switched）来说：

- `memory_archive` = 归档 / 默认降级
- `memory_forget` = 更强清理 / 从 recall 中彻底移除

## 验证结果

### 1. archive 的真实语义
通过 `memory_explain_rank` 验证：
- 归档后条目状态变为 `state=archived`, `layer=archive`
- 但当 query 与噪音原文高度一致时，archived 条目仍会被召回
- 因此 archive 不等于“彻底不可见”

### 2. forget 的效果
已删除 4 条系统包络噪音：
- `ae9f450e-9779-4c41-a4a4-8b32ffb4dbc0`
- `4f130ed3-8b44-4272-be68-73b4bee9c11b`
- `42bade28-26d2-44b3-ba04-79eb167b1c84`
- `5b9d4fea-4ca2-4055-b560-39ecceb39054`

删除后复测：
- `WhatsApp gateway connected as +8618602170660` 不再返回这些条目
- `Read HEARTBEAT.md if it exists` 不再返回 HEARTBEAT 系统包络条目
- `Conversation info (untrusted metadata)` 不再返回这 4 条已删噪音

## 对业务 recall 的影响
- `浏览器读取 X 默认用托管浏览器` 仍保持 Top1
- `Heartbeat / cron 错误判断` 前排仍有正确规则，且系统包络噪音已不再干扰

## 治理策略建议
### 用 archive 的场景
- 仍希望保留历史但降低默认参与度
- 非恶性噪音、仅需默认降权

### 用 forget 的场景
- 纯系统包络噪音
- gateway connect/disconnect
- HEARTBEAT 指令包络
- model switched 等无业务价值的 runtime envelope
- 目标是彻底不再污染 recall

## 当前决策
对已确认的系统包络噪音，优先采用 `memory_forget` 而不是仅 `memory_archive`。
