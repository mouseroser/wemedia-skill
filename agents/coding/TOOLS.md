# TOOLS.md - Coding Agent

## 开发工具
- 编程语言：根据项目需求
- 测试框架：根据项目配置
- 代码格式化：根据项目规范

## 冒烟测试清单
参考星链流水线 `references/smoke-test-checklist.md`：
- 核心路径测试
- 边界条件检查
- 依赖验证

## 工作目录
- 代码产出：`~/.openclaw/workspace/agents/coding/`
- 读取任务：`~/.openclaw/workspace/agents/brainstorming/specs/{feature}/tasks.md`

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
