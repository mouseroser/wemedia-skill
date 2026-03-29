# Memory Optimization Phase 2 — 2026-03-26

## Scope
执行 Phase 2A + Phase 2B：
- Phase 2A：补分层健康检查短句、巩固高频新规则
- Phase 2B：建立“新规则自动原子化”固定动作，开始清理系统包络噪音

## 本轮已执行

### Phase 2A
已补入 Layer 2 的短句型原子记忆：
- cron timeout 不等于 memory 故障，先看执行链路
- network connection error 优先判断为执行链路或模型连接波动，不直接判断 memory failure
- 判断 memory 是否真的坏了时，先分层：文件层、检索层、rerank 层、cron/模型调用层
- 浏览器读取 X 的当前有效口径：默认用 OpenClaw 托管浏览器；不要用本地浏览器或 profile=user

### Phase 2B
已固化的动作口径：
- 新规则 / 新偏好 / 新 workaround / 新边界，一律补短句型原子记忆
- 优先写成“问句能直接打中”的句式，而不是长段抽象说明
- 优先处理：用户偏好、系统规则、工具坑、外部研究资产定位

## 当前结果

### 已改善
- 新近规则 recall 提升明显
- 统计学表述约束已可 Top1 命中
- Berryxia 外部研究资产定位已可 Top1 命中
- 文件路径坑、buttons=[] workaround 已进入稳定可召回区间
- 分层健康检查规则已进入可用区（Top3/Top5 可拿到正确依据）

### 仍待继续
- 分层健康检查规则还没稳定到 Top1
- Layer 2 里仍有一部分系统包络/连接状态噪音与查询竞争

## 噪音治理状态
尝试归档以下噪音类记忆：
- WhatsApp gateway connected
- HEARTBEAT 系统包络类条目

结果：archive 调用返回失败，尚未完成自动归档，后续需要单独排查 memory_archive 的可用性或改用其他治理方式。

## 下一步建议
1. 继续补 1-2 条更贴近“Heartbeat / cron 错误 / memory 是否坏了”的短句记忆
2. 单独排查 memory_archive 为什么对已定位到的噪音条目归档失败
3. 之后再复跑一次针对性 benchmark，验证分层健康检查规则是否能冲到 Top1/Top2
