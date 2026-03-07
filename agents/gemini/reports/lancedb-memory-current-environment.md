# 当前 OpenClaw 环境约束（给织梦）

- 当前主工作区：`~/.openclaw/workspace/`
- 当前长期记忆仍以本地文件为主：`MEMORY.md` + `memory/YYYY-MM-DD.md`
- 已明确决定：Memory 不使用 NotebookLM；NotebookLM 只用于知识库查询
- `memory_search` 当前不可用，报错指向 embeddings/provider 配置异常（现象：`404 Cannot POST /codex/embeddings`）
- 当前已有 10 个子智能体，消息推送链路已实测可用
- `nano-banana` 发消息不能依赖默认生图模型，需显式覆盖到 `gpt-5.4`
- 偏好：重要决定、偏好、踩坑、解决方案、完成结果要主动记录
- 当前系统已有三层文件记忆意识：`IDENTITY.md` / `USER.md` / `MEMORY.md` + `memory/YYYY-MM-DD.md`
- 当前主要风险不是“完全没记忆”，而是：
  1. 记忆检索工具不可用
  2. 未来 `MEMORY.md` 继续膨胀
  3. 若直接全自动写向量库，可能把噪音和错误事实一起写进去
- 目标不是炫技，而是：可落地、可回滚、逐步迁移，不把现有系统搞脆
