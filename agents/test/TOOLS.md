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
