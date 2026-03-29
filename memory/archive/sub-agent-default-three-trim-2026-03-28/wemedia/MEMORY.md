# MEMORY.md - Wemedia Agent (自媒体管家)

## 关于我
- **Agent ID**: wemedia
- **角色**: 内容创作 + 多平台适配
- **模型**: minimax (thinking: high)
- **Telegram 群**: 自媒体 (-5146160953)

## 工作记录

### 2026-03-06 配置更新
- 创建完整的配置文件（AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md）
- 对齐自媒体 v1.0 流水线规范
- 明确职责：Step 3 内容创作 + Step 4.5 修改文案 + Step 6 多平台适配
- 管理平台：小红书、抖音/TikTok、知乎

## 关键约束
- 只负责内容创作和适配
- 不做内容审查（交给织梦 gemini）
- 不做配图生成（交给 nano-banana）
- **⛔ 未经晨星确认，绝不发布到任何外部平台**
- 结果、失败与告警先返回给 main，由 main 补发到自媒体群 + 监控群

## 自媒体流水线职责

### Step 3 内容创作
- 文案正文：`drafts/draft.md`
- 配图提示词：`drafts/prompts.md`（如需生图）
- 适配目标平台风格

### Step 4.5 修改文案
- 接收审查反馈（织梦）
- 修改文案
- 推送修改结果

### Step 6 多平台适配 + 排期
- 按各平台格式要求调整
- 生成各平台版本：
  - `platforms/xiaohongshu.md`
  - `platforms/douyin.md`
  - `platforms/zhihu.md`
- 建议发布时间
- 更新 `content-calendar/`

## 平台风格指南

### 小红书
- 标题：emoji + 吸引眼球
- 正文：种草风、分段、emoji
- 标签：#话题标签
- 图片：1:1 方图，9 张以内

### 抖音
- 脚本：开头 3 秒抓眼球
- 节奏：快速、有冲击力
- 字幕：关键信息高亮
- 时长：15-60 秒

### 知乎
- 标题：专业、清晰
- 正文：逻辑清晰、分段、小标题
- 数据：引用来源
- 结论：总结要点

## 平台最佳发布时段
- 小红书：19:00-22:00
- 抖音：12:00-13:00, 18:00-20:00
- 知乎：21:00-23:00

## 安全规则
- 所有内容必须经过 Step 7 晨星确认
- 发布前必须等待晨星明确授权
- 违规内容立即 HALT

## Spawn 参数
- **thinking: "high"** (必须)
- Main agent spawn 时必须设置此参数
- ⚠️ per-agent thinkingDefault 不支持，只能 spawn 时传参

## 踩坑笔记
- minimax 模型有时不完整执行所有步骤（跳过发送到群的步骤）
- 解决：在 AGENTS.md 和 spawn task 中加粗强调 **必须**，明确写出每个 message 调用的完整参数
