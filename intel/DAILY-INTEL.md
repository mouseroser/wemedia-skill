# 2026-03-29 每日情报

> 扫描时间：2026-03-29 07:30 CST（Asia/Shanghai）
> 范围：过去 12 小时内可见的 AI / Agent / LLM / 开发工具动态
> 口径：优先记录"值得知道"的技术、工具、行业与生态信号；不确定项标注 **[UNVERIFIED]**。

## 🔥 重要动态
- [Cursor 官方：Improving Composer through real-time RL](https://cursor.com/blog/real-time-rl-for-composer) — Cursor 公开用 real-time RL 持续优化 Composer，释放出"AI 编程工具开始边使用边自我改进"的明确信号；这更接近产品层持续学习闭环，而不只是一次性模型升级。
- [GitHub Trending](https://github.com/trending) / [obra/superpowers](https://github.com/obra/superpowers) — superpowers 今日爆量（昨晚已进入高增速区间），定位为 Agentic Skills Framework + software development methodology；说明"Skill 化 / 文件化 / 可组合 agent 工作流"正在形成更强社区共识。
- [GitHub Trending](https://github.com/trending) / [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) — 面向 Claude Code 的 teams-first 多 agent 编排项目继续走强，表明"单体 coding agent → 多 agent 团队协作"的叙事仍在升温。

## 🛠 技术 / 工具
- [GitHub Trending](https://github.com/trending) / [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) — 研究型 agent skill 继续处于高热状态：跨 Reddit / X / YouTube / HN / Web 做多源扫描并输出 grounded summary，适合内容研究、情报归纳、选题验证等流程。
- [GitHub Trending](https://github.com/trending) / [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) — Sakana AI 推进 scientist agent 路线，用 agentic tree search 指向更完整的研究发现工作流；虽偏研究，但代表 agent 能力边界继续外移。
- [GitHub Trending](https://github.com/trending) / [microsoft/VibeVoice](https://github.com/microsoft/VibeVoice) — 微软开源语音 AI 项目，说明大厂仍在加码 voice + agent 入口，值得持续跟踪"语音前端 + agent 后端"融合方向。

## 🏢 行业 / 竞品
- [Hacker News](https://news.ycombinator.com/item?id=47543139) / [Anatomy of the .claude/ folder](https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder) — HN 热帖继续发酵，核心不是某个技巧，而是"如何把 agent 的规则、上下文、记忆、技能组织成文件系统"；对所有做 agent 工作流的人都有方法论价值。
- [Product Hunt：AI Coding Agents 分类页](https://www.producthunt.com/categories/ai-coding-agents) — **[UNVERIFIED]** 分类页在近 12 小时仍有活跃更新与排序变化，可视作"AI coding agent 赛道持续拥挤"的弱信号，但不宜当作单独新闻事件引用。
- [llm-stats 每日更新页](https://llm-stats.com/llm-updates) — **[UNVERIFIED]** 聚合站点继续汇总模型版本、API 与定价变更，适合作为辅助雷达，不应替代官方源做最终判断。

## 💡 值得关注
- Skill 正在从 prompt 技巧上升为 **agent 工作流的标准组织单元**：superpowers、last30days-skill、.claude/ 文件夹讨论共同强化了这个方向。
- coding agent 竞争焦点正在迁移：从"谁更会补全/改代码"，转向"谁更会组织上下文、调用技能、形成多 agent 协作与持续优化闭环"。
- research / scientist agent 方向持续抬头：从内容研究到科学发现，agent 的价值正从"执行一步"升级为"编排完整流程"。

## 📝 早间 Top 3
1. **Cursor real-time RL for Composer**：AI 编程工具进入持续自我优化叙事。
2. **superpowers 持续爆量**：Skill 化 / Agentic workflow 成为强共识信号。
3. **.claude/ 文件系统方法论**：上下文工程正在产品化、结构化。

---

## 🕛 午间增量（12:30 CST）

### 🔥 重要动态
- **MiniMax M2.5 正式发布**（今日 12:15 CST）— MiniMax 推出旗舰模型 M2.5，coding / agentic tool use / search / office work 均宣称 SOTA；SWE-Bench Verified 和自研 VIBE Pro benchmark 与 Claude Opus 4.5 持平；RL 在数十万真实环境大规模训练；M2.5-highspeed 高 TPS 版同步上线；通用 Agent 平台同步开放。**[国产模型正面对标顶级 agentic 能力的最新信号]**
- **MiniMax M2.7 曝光**（昨日，持续发酵）— 定位"Self-Evolution 早期回响"，强调 native Agent Teams（多 agent 协作）和模型层级的角色边界与行为分化，表明 MiniMax 正在构建下一代 multi-agent 原生能力。
- **Anthropic Claude Mythos 泄露事件**（昨日 3/27，今日仍发酵）— Anthropic 意外将未发布模型 Claude Mythos 的描述文档暴露于公开可访问的数据缓存中（Fortune 首发）；市场解读该模型具有前所未有的网络安全攻击能力；单日蒸发网络安全股市值约 145 亿美元（CrowdStrike -7%、Palo Alto -6%、Zscaler -4.5% 等）。Anthropic 被报道"害怕发布"该模型。**[AI 能力边界与安全叙事的重大市场事件]**
- **Apple 付费 10 亿美元用 Gemini 为 Siri 赋能**（昨日，持续发酵）— Apple 内部 AI 投资被认为已全面失败，转而付费引入 Google Gemini 支持 Siri；标志大厂 AI 能力分化进一步加剧。**[UNVERIFIED 细节，需官方确认]**

### 🏢 行业 / 竞品
- **Google Gemini Drop March 2026**（昨日）— 推出"Import Memory to Gemini"数据导入工具、Personal Intelligence 免费开放等 5 项新功能；记忆与个人化成为 Google AI 产品层重点发力方向。
- **Google 拟为 Anthropic 50 亿美元数据中心提供融资支持**（今日）— 利用自身信用评级帮助 Anthropic 以更低利率融资，Google 与 Anthropic 的深度绑定进一步加强。

### 💡 午间洞察
- MiniMax 快速迭代（M2 → M2.1 → M2.5 → M2.7）的节奏，叠加 agentic 能力对标顶级闭源模型，国产模型的竞争烈度正在快速提升。
- Claude Mythos 泄露事件揭示：AI 安全能力的"双刃剑"叙事已从学术讨论进入资本市场定价，后续每一次顶级模型发布都可能引发安全股连锁反应。

---

## 🌙 晚间总结（18:00 CST，2026-03-29 by control-plane evening cron）

### 今日最重要的 3 件事

1. **MiniMax M2.5 发布 + M2.7 曝光**：国产模型正面对标 Claude Opus 4.5 agentic 能力；M2.7 原生 multi-agent 设计预示下一代模型竞争维度已从单体能力移至团队协作。这是今天最值得认真对待的行业信号。

2. **Claude Mythos 泄露引发安全股集体下跌**：单一 AI 模型安全能力的「预期」已足以让网络安全板块蒸发约 145 亿美元市值，说明 AI 能力边界与资本市场定价的耦合已进入不可忽视的阶段；后续每次顶级模型发布都可能重演。

3. **Skill 化 / 上下文工程成为今日全天最强共振信号**：superpowers（118K stars/今日 2752/day）、`.claude/` 文件夹方法论、last30days-skill、Cursor real-time RL 四条信号同日强化同一叙事——AI 工具正在从「一次性 prompt 工程」转向「可维护、可组合、持续自进化的 Skill 系统」。这不是单日热点，是 2026 年 Agent 方法论的结构性转变。

### 值得持续跟踪的趋势

- **国产模型 agentic 竞争**：MiniMax M2.5/M2.7、Apple 付费引入 Gemini for Siri — 模型层合纵连横进入新阶段，国产 vs 闭源的边界正在模糊，值得每周一次的专项观察。
- **AI 安全能力的资本市场定价**：Claude Mythos 事件是个预警；下次顶级模型发布（无论 OpenAI / Google / Anthropic）前后，安全叙事可能再次引发市场波动，值得建立信号联动机制。
- **Skill 化生态的产品化节奏**：superpowers / last30days-skill / oh-my-claudecode 同日爆量，说明从「个人实践」到「工具产品」的跨越正在提速；若明后两天有媒体跟进报道「Agent Skill 化成为市场共识」，可升作 L 级内容角度。
