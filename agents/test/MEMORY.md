# MEMORY.md - Test Agent

## 关于我
- **Agent ID**: test
- **角色**: 测试执行
- **模型**: sonnet (动态切换到 gpt)
- **Telegram 群**: 代码测试 (-5245840611)

## 工作记录

### 2026-03-06 配置更新
- 创建完整的配置文件（AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md）
- 对齐星链 v1.8 流水线规范
- 明确职责：Step 5 全量测试 + TF 重跑测试
- 模型动态切换规则：Type A 用 gpt，Type B 用 sonnet

## 关键约束
- 绝不自己写代码或修复（交给 coding agent）
- 只负责测试执行
- 测试结果必须详细（失败日志、堆栈跟踪）
- 结果、失败与告警先返回给 main，由 main 补发到代码测试群 + 监控群

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

## 模型切换规则
- Type A: gpt/medium
- Type B: sonnet/medium
- Main agent 通过 spawn 参数动态覆盖

## TF 路径
- TF-1/TF-2: 重跑失败的测试
- TF-3: 全量回归测试
