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
