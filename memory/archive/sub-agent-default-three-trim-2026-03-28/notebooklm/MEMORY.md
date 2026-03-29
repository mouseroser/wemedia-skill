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

## 2026-03-09~15 周进展

### Layer 3 NotebookLM Fallback 落地 (3/14-15)
- PR #206 已被 maintainer 关闭（E2E 回归 + memory_recall 契约变更不被接受）
- PR #210 合并（fork PR 跳过 claude-review）
- PR #227 被关闭（测试未接入 npm test，无运行时行为变更）
- 最终本地方案保留，上游方案转为 4H 策略（暂缓执行）
- 最终架构：L2 快速召回 (memory-lancedb-pro hybrid/MMR/rerank) → L3 深度推理 (NotebookLM 自动降级)

### OpenClaw 版本联动规则
- 晨星告知新版本后，必须同步立即更新 openclaw-docs notebook
- 标准动作：确认版本变化 → 触发 `openclaw-docs-update` → 回报结果

## 2026-03-16~22 周进展

### NotebookLM 配图新能力发现 (3/22)
- `notebooklm generate infographic --orientation square --style bento-grid --detail detailed --language zh_Hans`
- 输出 2048x2048 正方形、全中文 bento-grid 风格信息图，效果优秀
- 获取流程：`notebooklm use <notebook>` → `source add <文件>` → `generate infographic` → `artifact poll <id>` → `download infographic <id>`
- **优势**：绕过 Gemini 托管浏览器下载不落盘问题，全自动生成，无需手动操作

### NotebookLM CLI 关键命令
- 正确子命令：`notebooklm ask -n <notebook-id> "问题"`（不是 `query`）
- notebook 操作：`notebooklm use <id>`、`notebooklm source add <file>`
- artifact：`notebooklm generate infographic --orientation square --style bento-grid`
- 语言参数：`zh_Hans`（简体中文），不是 `"Chinese"`

### 自媒体运营系统 24/7 落地 (3/18-21)
- 小红书 方案 C+ 全链路验证完成：CDP 9223（独立 XiaohongshuProfiles Chrome）+ OpenClaw 内置浏览器（X/Twitter）
- NLM media-research notebook 重建（ID: 032a95b5）
- 4 个运营 cron 已配置：xhs-competitor-scan / x-kol-scan / xhs-content-data-sync / nlm-media-source-cleanup
- 本周实际发布：3 篇小红书内容（OpenCode 三强格局 / Claude HUD / Agent 安全下篇）

### 小红书发布踩坑汇总（必须遵守）
1. **标题 ≤ 20 字**（超出被拦截）
2. **话题标签最多 10 个**（超出报错且脚本报 PUBLISHED 但实际未提交）
3. **配图必须 1:1 方图**（1080x1080 或 2048x2048）
4. **禁止截图作配图**：必须下载原图（Gemini 下载到 ~/Downloads/，文件名 Gemini_Generated_Image_*.jpeg）
5. **禁止删到 0 张图**：替换流程必须先上传新图再删旧图
6. **每次操作后检查 toast/error**：`querySelectorAll('.toast, [class*=toast], [class*=notice], [class*=error]')`
7. **发布前用 content-data 检查是否已有同标题笔记**，防止重复发布
8. **\"重新上传\"会弹系统文件选择器**（DOM 外），改用 `browser upload` 直接灌入 `input[type=file]`

### 模型分工硬性规则 (3/20-21 晨星确认)
- 小红书发布 / CDP 自动化 / 多步骤外部操作：**禁用 MiniMax，必须用 Opus 或 Sonnet**
- wemedia 创作环节：**必须用 Sonnet**（MiniMax 会空跑不写文件）
- 操作类任务（浏览器自动化/发布/编辑）：**偏好 GPT**
- 制定计划/编排/策略：可用 Opus，轻量脚本型可用 MiniMax

### Layer 3 稳定化 (3/16-17)
- Layer 3 fallback 从 `openclaw agent --agent notebooklm` 改为直接调 `nlm-gateway.sh query`（绕开 gateway lane lock）
- timeout 从 45 秒调到 **75 秒**（配置 `plugins.entries.memory-lancedb-pro.config.layer3Fallback.timeout`）
- NotebookLM cron 脚本全面修复（5 个脚本都已验证：sync/daily-query/layer3-monthly-archive/update-openclaw-docs/layer3-deep-insights）
- Layer 2 噪音过滤规则加固（屏蔽系统包络 / WhatsApp connect-disconnect / heartbeat ack 等）

### Skills 精修完成 (3/18)
- `notebooklm` skill：gateway-first 路由，精简入口
- `starchain` skill：v2.8 精简入口，删除 launcher 遗产
- `wemedia` skill：对齐运营系统 v1.1，Gemini 搜索优先
- `todo-manager` skill：对齐 control-plane 架构
