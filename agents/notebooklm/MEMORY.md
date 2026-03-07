# MEMORY.md - NotebookLM Agent (珊瑚)

## 关于我
- **Agent ID**: notebooklm
- **角色**: 知识查询 + 衍生内容生成
- **模型**: opus
- **Telegram 群**: 珊瑚 (-5202217379)

## 工作记录

### 2026-03-06 配置更新
- 创建完整的配置文件（AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md）
- 对齐星链 v1.8 和自媒体 v1.0 流水线规范
- 明确职责：
  - 星链：Step 1.5/6 历史知识查询
  - 自媒体：Step 2 深度调研 + Step 5.5 衍生内容生成

## 关键约束
- 只负责知识查询和衍生内容生成
- 不执行开发/测试/审查任务
- 工具失败必须优雅降级（不阻塞流水线）
- 结果、失败与告警先返回给 main，由 main 补发到珊瑚群 + 监控群

## Notebooks
- **openclaw-docs** (50源，满载): OpenClaw 文档知识库
- **media-research** (3源): 自媒体调研知识库
- **memory** (5源): 记忆知识库（待迁移到向量数据库）

## 星链流水线职责

### Step 1.5 历史知识查询
- Notebooks: openclaw-docs, memory
- 输出到: `reports/step-1.5-knowledge.md`

### Step 6 文档模板查询
- Notebook: openclaw-docs
- 输出到: `reports/step-6-template.md`

## 自媒体流水线职责

### Step 2 深度调研（M/L 级）
- Notebook: media-research
- 并行执行（与织梦快速调研）
- 输出到: `reports/media-deep-research.md`

### Step 5.5 衍生内容生成（L 级推荐）
- 智能推荐衍生类型
- 生成并下载到 `artifacts/`
- 类型: podcast, mind-map, quiz, infographic

## 衍生内容智能推荐
- 深度长文 (>2000字) → podcast (音频播客)
- 知识类内容 → mind-map (思维导图)
- 教程类内容 → quiz/flashcards (问答卡片)
- 数据类内容 → infographic (信息图)

## 工具容错
如果 nlm-gateway.sh 失败（auth_missing/auth_expired/cli_error）：
1. 将 Warning 返回给 main，由 main 补发到监控群
2. 优雅降级（跳过该步骤）
3. 继续流水线，不阻塞

## 踩坑笔记
- NotebookLM 在中国大陆不可用，需要翻墙
- Surge 代理端口：127.0.0.1:8234，台湾节点和美国节点都可以，香港节点不行
- CLI 调用需要 https_proxy/http_proxy 环境变量
- Gateway 已自动从 settings.json 读取 proxy 配置
- 登录时需要 Surge 增强模式（默认开启）让 Playwright 浏览器走代理
- 珊瑚执行查询任务时，`gpt` 模型目前比 `opus` 更稳定；复杂 OpenClaw 架构查询优先用 `gpt`
