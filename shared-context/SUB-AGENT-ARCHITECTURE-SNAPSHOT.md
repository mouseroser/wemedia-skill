# SUB-AGENT-ARCHITECTURE-SNAPSHOT.md

> 更新：2026-03-28 21:05 Asia/Shanghai
> 口径：当前 sub-agent 顶层实际结构快照（收口后）。

## 总结

- sub-agent 默认不再单独维护 `USER.md`；服务对象信息收敛到 `AGENTS.md` 的“服务对象”段。
- 当前最小可运行骨架不是固定三件套，而是：`SOUL.md` + `IDENTITY.md` + `AGENTS.md` + `memory/`（如有真实价值）。
- `HEARTBEAT.md` / `TOOLS.md` / `MEMORY.md` / `BOOTSTRAP.md` 仍可按真实使用自然长出。
- 多智能体协作产物默认落到 `intel/collaboration/`，不再鼓励写入 agent 私有 `reports/` 作为跨 agent handoff 主链路。
- 职能群通知默认由各 agent 自推（best-effort）；监控群只由 `main` 在终态 / 异常时统一推送。

## 当前各 agent 共同结构特征

### 必有
- `SOUL.md`
- `IDENTITY.md`
- `AGENTS.md`

### 常见按需文件
- `HEARTBEAT.md`
- `TOOLS.md`
- `MEMORY.md`
- `BOOTSTRAP.md`
- `memory/`

### 已撤销的默认要求
- sub-agent 默认独立 `USER.md`
- 私有 `reports/` 作为多 agent 协作主路径
- main 对所有职能群做步骤级补发

## 当前协作主路径

- 星链：`intel/collaboration/starchain/`
- 星鉴：`intel/collaboration/stareval/`
- 自媒体：`intel/collaboration/media/`

## 当前通知主路径

- **职能群**：各 agent best-effort 自推
- **监控群**：`main` 只在终态 / 异常推送
- **晨星 DM**：确认门控、BLOCKED / FAILURE、最终结果、长任务阶段摘要
