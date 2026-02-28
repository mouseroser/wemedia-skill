# 自媒体内容流水线 wemedia-pipeline

基于[星链 StarChain](https://github.com/mouseroser/starchain-pipeline) v1.8 的内容创作流水线，集成 NotebookLM 知识层。

## 流程概览

```
Step 1  选题分级（S/M/L）+ 平台分析
Step 2  gemini 快速调研 + NotebookLM 深度调研（M/L 级）
Step 3  wemedia 内容创作（文案 + 配图提示词）
Step 4  gemini 内容审查（质量/合规/SEO）
  4.5   修改循环（max 3 rounds）
Step 5  nano-banana 配图生成（可选）
Step 5.5 NotebookLM 衍生内容（播客/思维导图/问答/信息图，L 级推荐）
Step 6  wemedia 多平台适配 + 排期
Step 7  晨星确认 → 交付
```

## 内容分级

| 级别 | 说明 | 流程 |
|------|------|------|
| S 简单 | 单平台短文案/转发 | 1→3→5→6→7 |
| M 标准 | 单平台原创图文 | 1→2→3→4→5→6→7 |
| L 深度 | 多平台联动/系列/长文 | 1→2→3→4→5→5.5→6→7 |

## Agent 角色

| Agent | 职责 |
|-------|------|
| main（小光） | 编排中心 + NotebookLM 调度 |
| gemini | 快速调研 + 内容审查 |
| wemedia | 内容创作 + 多平台适配 |
| nano-banana | 配图生成 |
| NotebookLM | 知识层（深度调研 + 衍生内容） |

## 目标平台

- 小红书（种草笔记风格）
- 抖音/TikTok（短视频脚本风格）
- 知乎（专业问答风格）

## NotebookLM 集成

- Step 2：查询 `media-research` notebook 获取历史研究，新领域自动补充深度资料
- Step 5.5：生成衍生内容（音频播客、思维导图、问答卡片、信息图）
- 调研结果自动回写为 notebook 源，知识持续积累

## 安全规则

- ⛔ 未经晨星确认，绝不发布到任何外部平台
- 内容审查 REJECT → HALT，通知晨星
- 所有步骤超时 10 分钟 → HALT

## 依赖

- [星链 StarChain](https://github.com/mouseroser/starchain-pipeline) v1.8 编排框架
- [NotebookLM Skill](~/.openclaw/skills/notebooklm/) 知识层
- OpenClaw agent 生态（wemedia / gemini / nano-banana / monitor-bot）

## 许可

MIT
