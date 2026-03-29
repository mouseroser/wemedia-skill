# TOOLS.md - NotebookLM Agent

## Gateway / CLI
- 默认走受管 gateway：`~/.openclaw/skills/notebooklm/scripts/nlm-gateway.sh`
- 直接 CLI 查询用 `notebooklm ask`，不是 `query`
- 常用链路：`use → source add → ask / generate → artifact poll → download`
- infographic 语言参数：`zh_Hans`

## Proxy / Network
- 中国大陆环境下通常需要代理
- Surge 代理：`127.0.0.1:8234`
- 美国 / 台湾节点可用；香港节点不稳定
- 必要时补 `https_proxy` / `http_proxy`

## 常用 notebook / 路径
- `openclaw-docs`
- `media-research`
- 查询结果：`~/.openclaw/workspace/agents/notebooklm/reports/`
- 衍生内容：`~/.openclaw/workspace/agents/notebooklm/artifacts/`

## 失败处理
- gateway / CLI 失败时优先降级，不阻塞主链

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。
