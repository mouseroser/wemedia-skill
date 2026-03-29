# TOOLS.md - Test Agent

## 测试工具
- 测试框架：根据项目配置
- 覆盖率工具：根据项目需求
- 性能测试：根据需要

## 测试类型
- **Step 5**: 完整测试套件
- **TF-1/TF-2**: 重跑失败的测试
- **TF-3**: 全量回归测试

## 测试报告格式
```
PASS/FAIL
- Total: X tests
- Passed: Y
- Failed: Z
- Duration: Xs

Failed tests:
- test_name: error message
  Stack trace: ...
```

## 工作目录
- 测试产出：`~/.openclaw/workspace/agents/test/`
- 读取代码：`~/.openclaw/workspace/agents/coding/`

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
