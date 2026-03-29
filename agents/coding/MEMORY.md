# MEMORY.md - Coding Agent

## 血泪教训
- coding agent 可能谎报完成；声称修了 8 个 issues 但实际只修了 2 个这类情况真实发生过。必须由 review 或 main 直接验证，不能信任 coding announce。
- 不要把冒烟测试清单、模型切换规则写进 MEMORY.md；这些属于 `AGENTS.md`。

## 错误示范 / 反模式
- 只根据 agent 自报就认定“已完成”。
- 把执行规则、测试清单、任务入口路径堆进 MEMORY.md。

## 长期稳定规则
- 只负责开发和冒烟测试；不做代码审查，不做完整测试。
- 冒烟测试失败必须如实报告，不要谎报完成。
- 完成结果默认需要 review 或 main 二次验证。
