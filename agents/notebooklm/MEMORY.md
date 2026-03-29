# MEMORY.md - NotebookLM Agent (珊瑚)

## 血泪教训
- NotebookLM 在中国大陆不可用，需要稳定代理；Surge 代理端口 `127.0.0.1:8234` 可用，香港节点不行。
- CLI 调用需要 `https_proxy/http_proxy`；登录时需要 Surge 增强模式让 Playwright 浏览器走代理。
- `notebooklm ask -n <notebook-id> "问题"` 才是正确查询方式，不是 `query`。
- `notebooklm generate infographic --orientation square --style bento-grid --detail detailed --language zh_Hans` 可生成 2048x2048 中文信息图，是稳定可复用能力。

## 错误示范 / 反模式
- 把 notebook 列表、流水线职责、工具容错规则、衍生内容推荐写进 MEMORY.md。
- 把 CLI 子命令猜错后不验证就继续扩散到流程里。

## 长期稳定规则
- 复杂 OpenClaw 架构查询目前 `gpt` 比 `opus` 更稳定。
- 小红书配图相关硬规则必须记住：标题 ≤20 字、标签 ≤10、图片必须 1:1 方图、发布前需 content-data 查重。
- Layer 3 fallback 当前稳定做法：直接调 `nlm-gateway.sh query`，timeout 75 秒。
