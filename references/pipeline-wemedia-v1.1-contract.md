# 自媒体内容流水线 v1.1 Contract

Source of truth: `PIPELINE_FLOWCHART_V1_1_EMOJI.md`.


## 1.5) 协作材料规则

- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物（报告、审查结论、修复代码、文档交付等）放各自 agent 目录
- 非正式产物（外部 GitHub 项目、本地镜像、共享分析素材、临时脚本、调研素材等）放 `intel/collaboration/`
- `intel/` 继续作为协作层，遵守单写者原则：一个 agent 负责写 / 更新，其他 agent 只读

## 1) 全局状态

```text
ReviseRound = 0
ReviseRound_MAX = 3
HALT_TIMEOUT = 10min
```

## 2) 内容分级

- `S`：简单，直接进入创作快通道
- `M`：标准，必须走 Constitution-First 前置链
- `L`：深度，必须走 Constitution-First 前置链 + GPT 仲裁位

## 3) Step 2 Constitution-First 前置链（M/L）

### 3.1 核心分工
- `Gemini`：内容颗粒度对齐，产出内容宪法
- `Claude Code`：基于内容宪法产出内容策略 / 执行计划
- `Gemini`：复核计划是否偏离原问题
- `GPT`：仅在 L 级 / 高风险 / 明显分歧时做挑刺 / 仲裁

### 3.2 M 级
- `Gemini -> Claude Code -> Gemini`
- Gemini 二次复核输出：`ALIGN | DRIFT | MAJOR_DRIFT`
- `ALIGN` → Step 3
- `DRIFT` → Claude Code 修订 1 次后再复核
- `MAJOR_DRIFT` → 升级 GPT 审核位

### 3.3 L 级
- `Gemini -> Claude Code -> Gemini -> GPT`
- GPT 输出：`GO | REVISE | BLOCK`
- `GO` → Step 3
- `REVISE` → Claude Code 修订 1 次 → Gemini 再复核
- `BLOCK` → HALT / 通知晨星

### 3.4 规则
- 不新增晨星中途确认节点
- Step 2 只升级前置策划层，不替换后续创作 / 审查 / 适配主干

## 4) Step 3 创作产出规范

### `drafts/draft.md`
- 标题
- 平台
- 内容类型
- 正文
- 标签
- 摘要

### `drafts/prompts.md`
- 封面图提示词
- 正文配图提示词（可选）

输入必须包含：
- 选题
- 内容宪法
- 内容计划
- 平台模板
- NotebookLM 知识补充（如有）

## 5) Step 4 审查 Verdict

```json
{
  "verdict": "PUBLISH | REVISE | REJECT",
  "score": 8,
  "quality": {"originality": 8, "readability": 9, "engagement": 7, "seo": 8},
  "compliance": {"pass": true, "issues": []},
  "constitutionAlignment": "ok | drift | major_drift",
  "suggestions": []
}
```

规则：
- `PUBLISH`：score ≥ 8 且合规通过
- `REVISE`：score 5-7 或存在可修复问题
- `REJECT`：score < 5 或存在严重违规

## 6) Step 4.5 修改循环

- Max 3 rounds
- 每轮上下文必须带：原始选题 + 当前草稿 + 审查反馈 + 历史修改记录
- `R3` 仍 `REVISE` → `PUBLISH_WITH_NOTES`
- 任意轮次 `REJECT` → HALT

## 7) Step 5 生图规范（NotebookLM 路线）

**首选：NotebookLM CLI**（全程 CLI，无需浏览器，2048x2048 正方形，中文原生）

```bash
notebooklm use <notebook-id>
notebooklm source add <article.txt>
notebooklm generate infographic \
  --orientation square \
  --style bento-grid \
  --detail detailed \
  --language zh_Hans \
  "<自定义 prompt>"
notebooklm artifact poll <task-id>
notebooklm download infographic <task-id> --artifact <artifact-id> --force
```

- 图片保存路径：`intel/collaboration/media/wemedia/drafts/generated/{A|B|C}/{文章标识}_infographic_sq.jpg`
- 尺寸：2048x2048 原生正方形，无需裁剪
- 语言代码：`zh_Hans`（简体）/ `zh_Hant`（繁体）
- 下载后用 Python PIL 裁剪黑边，JPEG quality=95
- 如 NotebookLM 不可用，降级为 nano-banana

**备选：nano-banana**（Gemini 网页生图，仅降级使用）

## 8) Step 5.5 衍生内容

- `notebooklm` 根据内容特征生成 podcast / mind-map / quiz（infographic 已归 Step 5）
- L 级推荐，M 级可选

## 9) Step 6 多平台适配

输出：
- `platforms/xiaohongshu.md`
- `platforms/douyin.md`
- `platforms/zhihu.md`
- `content-calendar/*`

必须包含：
- 字数 / 标签 / 排版适配
- 发布时间建议

## 10) Step 7 交付与确认

交付摘要必须包含：
- 选题 + 内容级别 + 目标平台
- 内容宪法 / 内容计划摘要
- 审查评分 + 状态
- 各平台版本路径 / 预览
- 配图 / 衍生内容（如有）
- 发布时间建议

安全红线：
- 未经晨星确认，绝不发布到任何外部平台

## 11) 通知合约

- 有消息能力的 agent 应自己向职能群发送开始 / 关键进度 / 完成 / 失败
- `main` 负责监控群终态/异常、最终交付、告警
- 方案类 / 调研类 / 审查类任务完成通知不能只发 `done`，必须附带摘要 / 结论 / 下一步

## 12) 版本原则

- 小更新不升版本号
- 大变动才生成新版本
- 只保留最近两个版本
- 默认入口始终指向最新版本
