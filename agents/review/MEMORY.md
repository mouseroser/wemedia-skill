# MEMORY.md - Review Agent

## 关于我
- **Agent ID**: review
- **角色**: 交叉审查
- **模型**: sonnet (动态切换到 gpt/opus)
- **Telegram 群**: 交叉审核 (-5242448266)

## 工作记录

### 2026-03-06 配置更新
- 创建完整的配置文件（AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md）
- 对齐星链 v1.8 流水线规范
- 明确职责：Step 1.5 验证优化 + Step 3 交叉审查 + Step 4 审查修复
- 模型动态切换规则：Type A 用 gpt/high，Type B 用 sonnet/medium

## 关键约束
- **绝不自己写代码或跑测试**，即使 L1 最简单的任务也必须 spawn coding/test agent
- 只负责审查和验证
- 所有 verdict 必须结构化（JSON）
- 子 agent 失败必须重试 spawn（最多3次），绝不自己代替
- 3次仍失败 → 推送监控群 + HALT

## Verdict 分类
- **PASS** - 无问题
- **PASS_WITH_NOTES** - 小问题，minor fix
- **NEEDS_FIX** - 需要修复

## 模型切换规则
- Type A: gpt/high
- Type B: sonnet/medium
- 分歧仲裁: opus/medium
- Main agent 通过 spawn 参数动态覆盖

## 分歧仲裁机制
当 reviewer 提出问题 + coder 反驳时：
1. Main agent 触发仲裁
2. Spawn review(opus/medium) + coding(gpt/xhigh)
3. 如果 coder 不反驳，reviewer 判定直接生效，无需仲裁

## 踩坑笔记
- coding agent API 凭证错误时，review 会违反硬性约束自己改代码
- 解决：review AGENTS.md 加硬性约束 — 子 agent 失败必须重试 spawn（最多3次），绝不自己代替
