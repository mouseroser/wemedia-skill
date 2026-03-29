# TOOLS.md - Local Notes

## Workspace
- **主目录**: `~/.openclaw/workspace/agents/claude/`
- **报告**: `reports/`
- **实验**: `experiments/`
- **记忆**: `memory/`

## Claude API
- 使用 OpenClaw 配置的 Anthropic provider
- 模型：claude-opus-4-6
- Thinking 模式：medium（可动态调整）

## 推送目标
- **职能群**: 小克 (-5101947063)
- **监控群**: 监控告警 (-5131273722)

## 协作文件
- `intel/` - 与其他智能体共享研究成果
- `shared-context/` - 跨智能体知识层

---

根据实际使用添加更多工具和配置笔记。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
