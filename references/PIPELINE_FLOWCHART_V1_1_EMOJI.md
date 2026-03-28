# 🎨 自媒体内容流水线 v1.1 — Constitution-First Content Delivery

```
┌─────────────────────────────────────────────────────────┐
│  🌐 Global State                                        │
│  内容级别: S / M / L                                     │
│  修改轮次: R1 / R2 / R3 (max 3)                         │
│  平台: 小红书 / 抖音 / 知乎 / 多平台                      │
│  HALT_TIMEOUT = 10min                                   │
└─────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════
  🗂️ 协作材料规则
═══════════════════════════════════════════════════════════

  - 多 agent 联合工作的非正式产物
    （外部 GitHub 项目、本地镜像、共享分析素材、临时脚本等）
    → 统一放到 `intel/collaboration/`
  - 正式产物
    （报告、审查结论、修复代码、文档交付等）
    → 放各自 agent 目录
  - `intel/` 继续作为协作层，遵守单写者原则

═══════════════════════════════════════════════════════════
  📥 Step 1 — 选题分级 + 平台分析
═══════════════════════════════════════════════════════════

  ☀️ main（小光）/model opus /think high

  1. 📋 判断内容类型 → S / M / L
  2. 📋 确定目标平台 → 小红书 / 抖音 / 知乎 / 多平台
  3. 📋 确定内容形式 → 图文 / 视频脚本 / 问答 / 种草笔记
  4. 输出选题单 → 自媒体群自推；监控群终态/异常由 main

       ┌──── S 级 ────┐
       │ ⚡ 快速通道   │────────────────────────────► Step 3
       └──────────────┘

       ┌──── M/L ────┐
       │ 🧭 前置链    │────────────────────────────► Step 2
       └──────────────┘

═══════════════════════════════════════════════════════════
  🧭 Step 2 — Constitution-First 选题前置链（M/L）
  Orchestrator: ☀️ main
═══════════════════════════════════════════════════════════

  核心思想：
    先由 Gemini 对齐“内容问题定义”
    再由 GPT/OpenAI 定义“内容宪法边界”
    再由 Claude Code 产出内容策略与执行计划
    最后由 Gemini 复核是否跑偏
    仅在高风险 / 明显分歧时再启用额外仲裁

  M 级：
    1️⃣ Gemini → 内容颗粒度对齐
       • 目标受众
       • 平台定位
       • 选题角度
       • 问题 framing
       • 内容颗粒度
       → 输出「颗粒度对齐单」
       → 织梦群自推；监控群终态/异常由 main

    2️⃣ GPT/OpenAI → 内容宪法边界
       • 必须强调什么
       • 必须避免什么
       • 不可夸大点
       • 风险边界 / 表达边界
       → 输出「内容宪法」
       → 小曼群自推；监控群终态/异常由 main

    3️⃣ Claude Code → 内容策略/执行计划
       • 内容结构
       • 论点展开顺序
       • 平台适配策略
       • 素材/证据需求
       → 小克群自推；监控群终态/异常由 main

    4️⃣ Gemini → 一致性复核
       → 输出：ALIGN / DRIFT / MAJOR_DRIFT
       → 织梦群自推；监控群终态/异常由 main

       ALIGN ✅      → Step 3
       DRIFT ⚠️      → Claude Code 修订 1 次 → Gemini 再复核
       MAJOR_DRIFT ❌ → 升级仲裁位

  L 级：
    1️⃣ Gemini → 内容颗粒度对齐
    2️⃣ GPT/OpenAI → 内容宪法边界
    3️⃣ Claude Code → 内容策略/执行计划
    4️⃣ Gemini → 一致性复核
    5️⃣ GPT → 风险挑刺 / 反方审查 / 仲裁
       → 输出：GO / REVISE / BLOCK
       → 小曼群自推；监控群终态/异常由 main

       GO ✅      → Step 3
       REVISE ⚠️  → Claude Code 修订 1 次 → Gemini 复核
       BLOCK ❌   → HALT / 通知晨星

  规则：
    - 🚫 不新增晨星中途确认节点
    - ✅ Step 2 只升级前置策划层，不替换后续创作 / 审查 / 适配主干

═══════════════════════════════════════════════════════════
  ✍️ Step 3 — 内容创作
  Executor: ✍️ wemedia /thinking high
  Orchestrator: ☀️ main
═══════════════════════════════════════════════════════════

  输入：
    • 选题
    • 内容宪法
    • 内容计划
    • 平台模板
    • NotebookLM 知识补充（如有）

  创作任务：
    1. 文案正文 → drafts/draft.md
    2. 配图提示词 → drafts/prompts.md（如需生图）

  📋 → 自媒体群自推；监控群终态/异常由 main

═══════════════════════════════════════════════════════════
  🔍 Step 4 — 内容审查（S 级可轻量）
  Executor: 🧵 织梦(gemini)
  Orchestrator: ☀️ main
═══════════════════════════════════════════════════════════

  审查任务：
    • 内容质量评分（1-10）
    • 平台合规检查
    • SEO / 标题 / 标签建议
    • 吸引力与可读性评估
    • 是否偏离内容宪法

  输出 verdict：
    ✅ PUBLISH
    ⚠️ REVISE
    ❌ REJECT

  PUBLISH → Step 5
  REVISE  → Step 4.5
  REJECT  → HALT + 通知晨星

  📋 → 织梦群自推；监控群终态/异常由 main

═══════════════════════════════════════════════════════════
  🔧 Step 4.5 — 修改循环（max 3 rounds）
  Orchestrator: ☀️ main
  Executor: ✍️ wemedia
  Reviewer: 🧵 gemini
═══════════════════════════════════════════════════════════

  每轮：
    1. wemedia 修改
    2. gemini 复审

  轮次：
    R1 / R2 → 常规修改
    R3 仍 REVISE → PUBLISH_WITH_NOTES
       • 自动生成审阅要点摘要
       • 高亮未完全解决的问题

  任意轮次 REJECT → HALT

═══════════════════════════════════════════════════════════
  🎨 Step 5 — 配图生成（可选）
  Executor: 🪸 notebooklm
  Orchestrator: ☀️ main
═══════════════════════════════════════════════════════════

  使用 NotebookLM generate infographic 命令（square 方向，bento-grid 风格）
  保存路径：`intel/collaboration/media/wemedia/drafts/generated/{A|B|C}/{文章标识}_infographic_sq.jpg`
  命令示例：
    notebooklm generate infographic --orientation square --style bento-grid \
      --detail detailed --language zh_Hans "内容摘要"
    notebooklm download infographic <task-id> --artifact <artifact-id> --force \
      --output intel/collaboration/media/wemedia/drafts/generated/{A|B|C}/{文章标识}_infographic_sq.jpg

  无配图需求 → 跳过

  📋 → 自媒体群自推；监控群终态/异常由 main

═══════════════════════════════════════════════════════════
  🎭 Step 5.5 — 衍生内容生成（L 级推荐）
  Executor: 🪸 notebooklm
  Orchestrator: ☀️ main
═══════════════════════════════════════════════════════════

  珊瑚按内容特征推荐并生成：
    • podcast
    • mind-map
    • quiz
    • infographic

  📋 → 自媒体群自推；监控群终态/异常由 main

═══════════════════════════════════════════════════════════
  📱 Step 6 — 多平台适配 + 排期
  Executor: ✍️ wemedia /thinking high
  Orchestrator: ☀️ main
═══════════════════════════════════════════════════════════

  任务：
    • 生成各平台版本
    • 调整字数 / 标签 / 排版
    • 更新 content-calendar
    • 给出发布时间建议

  📋 → 自媒体群自推；监控群终态/异常由 main

═══════════════════════════════════════════════════════════
  📦 Step 7 — 晨星确认 + 交付
  Executor: ☀️ main
═══════════════════════════════════════════════════════════

  交付摘要必须包含：
    ✅ 选题 + 目标平台
    🧭 内容宪法 / 内容计划摘要
    📊 审查评分 + 状态
    📱 各平台版本预览
    🎨 配图 / 衍生内容（如有）
    🗓️ 建议发布时间

  → 自媒体群 (-5146160953)
  → 监控群 (-5131273722)
  → 晨星 (1099011886)

  ⛔ 未经晨星确认，绝不发布到外部平台

  ✅ 晨星确认后 → main 通知 wemedia 执行 Step 7.5：

    1. main 下发最终发布指令与发布包路径
    2. wemedia 读取平台适配产物与素材路径
    3. 按平台调用执行工具
       - 小红书 → `xiaohongshu/scripts/publish_pipeline.py`
       - 抖音 → `douyin/scripts/publish_douyin.py`
    4. wemedia 将结果回传给 main
    5. main 更新 HOT-QUEUE.md 状态并推送监控通知

═══════════════════════════════════════════════════════════
  📦 Step 7.5 — wemedia 调用平台 skill 发布
  Executor: ✍️ wemedia
  Orchestrator: ☀️ main
═══════════════════════════════════════════════════════════

  wemedia 从发布包读取：
    • 标题 / 正文 / 标签
    • 配图 / 视频 / 封面路径
    • 可见性 / 音乐等平台参数

  执行发布（按平台调用）：
    ```bash
    # 小红书
    cd ~/.openclaw/skills/xiaohongshu
    python3 scripts/publish_pipeline.py --pack /path/to/xhs-pack.md

    # 抖音
    cd ~/.openclaw/skills/douyin
    python3 scripts/publish_douyin.py --pack /path/to/douyin-pack.md --step full
    ```

  收尾动作：
    • wemedia 回传发布 / 审核结果给 main
    • main 更新 HOT-QUEUE.md 状态 → ✅ 已发布
    • main 记录帖子 ID / 审核状态 → 监控群通知
    • 触发 Step 8 日结（如需要）

  失败降级：
    • 脚本 / CDP 报错 → 由 main 降级为手动发布（晨星介入）
    • 配图或封面缺失 → 退回 Step 6 补齐后再发布

═══════════════════════════════════════════════════════════
  🏁 END
═══════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════
  📢 Push Rules
═══════════════════════════════════════════════════════════

  默认原则：
    • sub-agent：默认向各自职能群自推步骤级通知（best-effort），结果同时返回 main
    • main：监控群 + 晨星 DM 的可靠通知节点；监控群只承接终态/异常
    • 晨星DM：不是流水账通道，只用于确认、阻塞失败、最终结果、长任务阶段摘要
    • 如果任务本身就在晨星DM中进行，默认直接在当前对话回复，不额外重复主动 DM
    • 原因：agent 自推只能算 best-effort，可靠通知以 main 为准
    • `message(action="send")` 单发必须用 `target`，不要用 `targets`
    • 同时发多个群时，按单目标串行发送多次；`targets` 只允许给 `action="broadcast"`
    • 注意：本流程图中的推送定义是**路由说明**；真正生效的执行规则以 `skills/wemedia/SKILL.md` 的 Notification Rules 与 `agents/wemedia/AGENTS.md` 为准

  完成通知要求：
    • 方案类 / 调研类 / 审查类任务完成时不得只发 done
    • 必须附带摘要 / 结论 / 下一步

═══════════════════════════════════════════════════════════
```
