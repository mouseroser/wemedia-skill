# MEMORY.md - 小光的长期记忆

> 只保留长期伤疤、反模式、稳定规则与长期偏好。
> 旧版已归档：`memory/archive/MEMORY-2026-03-28-before-architecture-trim.md`

---

## ⚠️ 血泪教训（永不重犯）

1. **Review 不做编排**：review 只负责审查，所有编排由 main 负责。mode=run 的 announce 有轮次限制。
2. **Agent 自推不可靠**：关键通知必须由 main 补发，不能依赖 sub-agent 自推到群。
3. **Coding 结果不可信**：coding 的 announce 不可信，必须通过 review 或 main 直接验证。
4. **memory-lancedb-pro 升级回归**：升级会覆盖本地补丁（`resolveRuntimeAgentId(...) || 'main'`），每次升级后必须检查 `memory_stats` / `memory_list` 是否正常。修复后需完整 `openclaw gateway restart`。
5. **AI 生成的脚本必须当场验证**：先 `openclaw <cmd> --help` 确认子命令存在，不要盲目信任 agent 生成的 CLI 命令。
6. **Cron isolated session 不查记忆**：prompt 里写死的路径必须经过验证；需要调用 memory 工具的任务不写 shell 脚本，用 agentTurn 直接调工具。
7. **重要工作记录缺一不可**：完成重要工作后必须同步写 `memory/YYYY-MM-DD.md`；如形成长期规则，再写 `MEMORY.md` 与 `memory_store`；如踩坑复发风险高，再补 `.learnings/ERRORS.md`。
8. **小红书发布前必检 checklist**：标题 ≤20 字 / 标签 ≤10 个 / 先 content-data 检查是否已有同标题笔记 / 配图 1:1 方图。
9. **MiniMax 禁止用于发布 / 创作**：MiniMax 禁止用于小红书发布、CDP 自动化、多步骤外部操作、wemedia 创作。必须用 Opus 或 Sonnet。
10. **卡点处理：最多重试 2 次就切方向**：遇到链路不通，最多重试 2 次，第 3 次必须切换方向，禁止停在解释或等待上。
11. **执行前必须查记忆**：发布 / 生图 / 多步骤任务执行前，先 `memory_recall` 查已知坑。
20. **新建 agent 必须调用 agent-config-generator**：新建任何 agent 时，必须先读 `agent-config-generator` SKILL.md，用它生成 SOUL/IDENTITY/HEARTBEAT 三件套，再手写 AGENTS.md；不得依赖 gateway 自动生成的默认空壳模板。
21. **编排型 agent 必须配置六件套**：新建需要 spawn/send 其他 agent 的 agent，openclaw.json 必须同时配置：agents.list 条目、bindings、主 agent allowAgents、tools.allow（含 sessions_spawn/sessions_send/message）、subagents.allowAgents、**subagents.maxSpawnDepth:2**；缺任何一项都会导致工具不可用。maxSpawnDepth 默认 1，不配置则 sessions_spawn 报 `Tool not found`。
22. **织梭 thinking=off**：织梭（weaver）是协调引擎，spawn 时不传 thinking 或用 thinking=off；只在 BLOCKED 判断等需要推理的场景才用 thinking=medium。
12. **多步骤任务必发 4 类通知**：开始 / 关键进度 / 错误阻塞 / 完成结果，不能只在后台执行。
13. **旧 PR 基于过时分支时直接重建**：不要继续修脏 diff，基于 upstream 默认分支重建干净 PR。
14. **重命名目录后必须 grep 内部引用**：否则路径全断。
15. **小红书 CDP 发布频率限制**：单日 ≤3 篇、间隔 ≥3 小时、申诉期间暂停；main 有最高权力制止发布。
16. **browser upload 路径限制**：`browser(action=upload)` 要求文件必须在 `/tmp/openclaw/uploads/` 下；跨目录文件需先 `cp` 过去。
17. **NotebookLM 生图必须用临时 notebook**：必须走“创建临时 notebook → 加单一干净 source → 生成 → 下载 → 删除临时 notebook”流程，禁止直接用共用 notebook 生成配图。
18. **正式发布脚本失效时禁止 main 手工 browser 补发**：页面结构变更、CDP 异常、字段校验失败时，必须 `BLOCKED`，先修执行链路或转人工确认。
19. **发布成功页不等于内容正确**：正式发布前必须核对标题、正文、标签、素材路径与最终发布包完全一致。

---

## ❌ 错误示范 / 反模式

- 让 review 编排其他 agent → main 直接编排所有 agent
- 依赖 agent 自推到群 → main 统一补发可靠通知
- browser 直接访问 GitHub 做重操作 → 先拉本地仓库或用 gh / git
- 改配置后只做 reload → 必须 `openclaw gateway restart`
- skills 放 workspace 下 → 放 `~/.openclaw/skills/`
- TODO 放 workspace 下 → 放 `~/.openclaw/todo/`
- 发现问题先解释再等待 → 先修再报
- 修改 plugins 后直接重启 → 先清 `/tmp/jiti/` 再重启
- 截图落盘当正式配图 → 下载原图或走 NotebookLM / 生图链路
- profile=`openclaw` 做下载链路 → 优先 `profile="user"` 连本机 Chrome

---

## 📌 长期稳定规则

- **Main 只在主会话编排**：禁止用 isolated session 编排主链。
- **Main 不直接编辑应用代码**：应用代码修改必须交给 coding。
- **流水线默认自动推进**：除 Step 7 晨星确认外，中间步骤不停顿。
- **Step 7 未经确认绝不发布**：晨星确认后，Step 7.5 一律由 wemedia 执行；main 只监控、通知、回报。
- **关键通知 owner = main**：agent 自推只能算 best-effort，不能承载可靠通知。
- **文件分工固定**：IDENTITY = 名片；SOUL = 人格与边界；USER = 服务对象合同；AGENTS = 执行手册；HEARTBEAT = 值班清单；TOOLS = 环境坑位；MEMORY = 长期伤疤与护栏；daily log = 当天账本与晋升池。sub-agent 可以从最小骨架启动，但应随真实使用自然长出更多文件；目标是主语清晰，不是文件越少越好。

---

## 🌱 长期偏好

- 沟通用短句、短段，简洁有力。
- 默认自动执行，不反复确认。
- 遇到障碍先解决，再回报，不停在解释上。
- 重视职责边界与通知可靠性。
- 重要修复、踩坑与规则变更立即记录。

---

**最后更新**：2026-03-28 11:20
**下次回顾**：2026-04-04
