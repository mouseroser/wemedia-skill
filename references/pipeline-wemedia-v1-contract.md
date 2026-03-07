# 自媒体内容流水线 v1.0 Contract

> DEPRECATED: 此文件已被 `pipeline-wemedia-v1.1-contract.md` 取代，不再作为默认执行入口；仅保留作回看/回滚参考。

Source of truth: `SKILL.md`

## 1) 全局状态

```text
ReviseRound = 0
ReviseRound_MAX = 3
HALT_TIMEOUT = 10min
```

## 2) 内容分级

| 级别 | 说明 | 通道 |
|------|------|------|
| S（简单） | 单平台短文案/转发评论 | 快速通道（跳过 Step 2/4） |
| M（标准） | 单平台原创图文/回答 | 标准通道 |
| L（深度） | 多平台联动/系列/深度长文 | 完整通道 |

## 3) 平台配置

| 平台 | 风格 | 字数限制 | 特殊要求 |
|------|------|----------|----------|
| 小红书 | 种草风、口语化、emoji 丰富 | 标题 20 字、正文 1000 字内 | 标签 10-15 个、封面图必须 |
| 抖音 | 短视频脚本、hook 开头、节奏紧凑 | 脚本 300 字内 | 前 3 秒 hook、BGM 建议 |
| 知乎 | 专业深度、数据引用、逻辑清晰 | 无硬性限制 | 引用来源、专业术语 |

## 4) Step 3 创作产出规范

### draft.md 结构
```markdown
# [标题]

## 平台：[目标平台]
## 类型：[图文/视频脚本/问答]

---

[正文内容]

---

## 标签
#标签1 #标签2 ...

## 摘要
[一句话摘要，用于平台简介/描述]
```

### prompts.md 结构（如需配图）
```markdown
# 配图提示词

## 封面图
[英文提示词，描述风格/构图/色调]

## 配图 1
[英文提示词]

## 配图 2（可选）
[英文提示词]
```

## 5) Step 4 审查 Verdict

```json
{
  "verdict": "PUBLISH | REVISE | REJECT",
  "score": 8,
  "quality": {
    "originality": 8,
    "readability": 9,
    "engagement": 7,
    "seo": 8
  },
  "compliance": {
    "pass": true,
    "issues": []
  },
  "suggestions": [
    "建议优化标题，增加数字吸引力",
    "第三段可以加入具体案例"
  ]
}
```

### Verdict 判定规则
- score ≥ 8 且 compliance.pass = true → PUBLISH
- score 5-7 或 compliance 有可修复问题 → REVISE
- score < 5 或 compliance 有严重违规 → REJECT

## 6) Step 4.5 修改循环

- Max 3 rounds
- 每轮携带 context：原始选题 + 当前草稿 + 审查反馈 + 前轮修改记录
- R3 仍 REVISE → 降级 PUBLISH_WITH_NOTES（标记需晨星重点审阅）
- 任何轮次 REJECT → HALT

## 7) Step 5 生图规范

- nano-banana 只接受英文提示词
- spawn 参数：`runTimeoutSeconds: 300`
- 图片下载到 wemedia workspace：`~/.openclaw/workspace-wemedia/`
- 发送到自媒体群 + 生图群
- nano-banana 返回可能显示 failed 但图片实际生成（检查返回内容中的 URL）

## 8) Step 6 多平台适配

每个目标平台生成独立版本文件：
- `platforms/xiaohongshu-[date]-[slug].md`
- `platforms/douyin-[date]-[slug].md`
- `platforms/zhihu-[date]-[slug].md`

适配要点：
- 字数裁剪/扩展至平台要求
- 标签格式适配（小红书 # / 知乎话题标签）
- 排版适配（小红书 emoji 分段 / 知乎 markdown）

排期更新：
- 写入 `content-calendar/YYYY-MM.md`
- 格式：`| 日期 | 平台 | 标题 | 状态 | 链接 |`

## 9) Step 7 交付 + 确认门控

交付摘要必须包含：
- 选题 + 内容类型 + 级别（S/M/L）
- 目标平台列表
- 审查评分 + 状态（normal / publish_with_notes）
- 各平台版本文件路径
- 配图文件路径（如有）
- 建议发布时间

⛔ 安全红线：
- 未经晨星确认，绝不发布到任何外部平台
- 晨星确认方式：在 Telegram 中回复"确认发布"或类似肯定表达
- 晨星可以要求修改后再确认

## 10) 告警规则

| 触发 | 级别 | 目标 |
|------|------|------|
| Step 4 REJECT | 🚨 | 自媒体群 + 监控群 + 晨星 |
| Step 4.5 R3 降级 | ⚠️ | 自媒体群 + 监控群 |
| 任何步骤超时 | ⚠️ | 监控群 + 晨星 |
| nano-banana 生图失败 | ⚠️ | 监控群 |
| HALT | 🚨 | 监控群 + 晨星 |
