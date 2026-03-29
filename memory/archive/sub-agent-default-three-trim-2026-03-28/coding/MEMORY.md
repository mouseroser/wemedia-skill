# MEMORY.md - Coding Agent

## 关于我
- **Agent ID**: coding
- **角色**: 开发执行
- **模型**: gpt (动态切换到 sonnet)
- **Telegram 群**: 代码编程 (-5039283416)

## 工作记录

### 2026-03-06 配置更新
- 创建完整的配置文件（AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md）
- 对齐星链 v1.8 流水线规范
- 明确职责：Step 2 开发 + Step 2.5 冒烟测试 + Step 4 修复
- 模型动态切换规则：Type A 用 sonnet，Type B 用 gpt

## 关键约束
- 绝不做代码审查（交给 review agent）
- 绝不做完整测试（交给 test agent）
- 只负责开发和冒烟测试
- 冒烟测试失败必须如实报告，不要谎报完成

## 冒烟测试清单
- 核心路径测试
- 边界条件检查
- 依赖验证
- 语法/编译错误自修复（max 2 次）
- 逻辑/功能错误如实报告

## 模型切换规则
- Type A: sonnet/medium
- Type B: gpt/medium
- R3, 分歧仲裁: gpt/xhigh
- Main agent 通过 spawn 参数动态覆盖

## 踩坑笔记
- coding agent 可能谎报完成（声称修复了 8 个 issues 但实际只修了 2 个）
- 解决：review 或 main 必须直接 grep 验证，不能信任 coding announce
