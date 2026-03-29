# TOOLS.md - Review Agent

## 审查工具
- 代码静态分析
- 性能基准对比（参考 `references/performance-baseline.md`）
- 安全性检查
- 依赖分析

## Verdict 格式
```json
{
  "verdict": "PASS | PASS_WITH_NOTES | NEEDS_FIX",
  "score": 85,
  "issues": [
    {
      "severity": "critical | major | minor",
      "category": "logic | performance | security | style",
      "description": "...",
      "location": "file:line",
      "suggestion": "..."
    }
  ]
}
```

## 工作目录
- 审查产出：`~/.openclaw/workspace/agents/review/`
- 读取代码：`~/.openclaw/workspace/agents/coding/`
- 读取需求：`~/.openclaw/workspace/agents/brainstorming/specs/`

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
