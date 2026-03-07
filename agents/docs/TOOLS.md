# TOOLS.md - Docs Agent

## 文档类型
- **README.md**: 项目概述、快速开始
- **API 文档**: 接口说明、参数、返回值
- **使用指南**: 详细教程、最佳实践
- **变更日志**: CHANGELOG.md

## 文档结构
- 清晰的标题层级
- 代码示例
- 使用场景说明
- 常见问题 FAQ

## 输入来源
- 织梦(gemini)大纲：`~/.openclaw/workspace/agents/gemini/reports/step-6-outline.md`
- 代码 diff：`~/.openclaw/workspace/agents/coding/`
- 审查摘要：`~/.openclaw/workspace/agents/review/`
- 珊瑚文档模板（如有）：`~/.openclaw/workspace/agents/notebooklm/reports/step-6-template.md`

## 工作目录
- 文档产出：`~/.openclaw/workspace/agents/docs/`

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
