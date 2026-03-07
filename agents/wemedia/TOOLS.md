# TOOLS.md - Wemedia Agent

## 内容创作工具
- 文案编辑
- 平台模板
- 内容排期

## 平台模板
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

## 工作目录结构
```
~/.openclaw/workspace/agents/wemedia/
├── drafts/              # 内容草稿
│   ├── draft.md        # 文案正文
│   └── prompts.md      # 配图提示词
├── platforms/           # 各平台版本
│   ├── xiaohongshu.md
│   ├── douyin.md
│   └── zhihu.md
└── content-calendar/    # 内容排期
    └── YYYY-MM.md
```

## 输入来源
- 选题：main agent 传入
- 调研摘要：
  - 织梦快速调研：`~/.openclaw/workspace/agents/gemini/reports/media-research.md`
  - 珊瑚深度调研：`~/.openclaw/workspace/agents/notebooklm/reports/media-deep-research.md`
- 审查反馈：`~/.openclaw/workspace/agents/gemini/reports/content-review.json`

## Spawn 参数
- **thinking: "high"** (必须)
- main agent spawn 时必须设置此参数

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
