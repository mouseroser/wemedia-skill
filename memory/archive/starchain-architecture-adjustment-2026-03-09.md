# 星链架构调整记录

## 日期
2026-03-09

## 问题
星链 v2.5 设计的"Review 作为交叉评审中枢编排 gemini/openai/claude"无法实现。

## 根本原因
OpenClaw 不支持 depth-2 subagent：
- Main spawn review（depth-1）✅
- Review spawn gemini（depth-2）❌

## 决策
放弃 Review 编排模式，改为 Main 直接编排所有 agent。

## 新架构
- Step 1.5A: Main spawn gemini（扫描）
- Step 1.5B: Main spawn openai（宪法）
- Step 1.5C: Main spawn claude（计划）
- Step 1.5D: Main spawn gemini（一致性复核）
- Step 1.5E: Main spawn openai（仲裁，如需要）
- Step 3: Main spawn claude + gemini（双审）
- Step 4: Main spawn gemini（预审）+ review（正式复审）

## 影响
- Review 不再是"编排中枢"，只做单一审查任务
- Main 承担更多编排职责
- 架构更简单、更符合 OpenClaw 限制

## 后续
- 更新星链 SKILL.md
- 更新 Review AGENTS.md
- 记录到 MEMORY.md
