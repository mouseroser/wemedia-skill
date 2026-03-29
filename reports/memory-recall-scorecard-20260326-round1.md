# Memory Recall Scorecard — 2026-03-26 Round 1

基于 `reports/memory-recall-benchmark-lite.md` 的第一轮抽样实测。

## 结果摘要

- 已实测：15 条中的首批核心查询
- 整体表现：长期规则 / 稳定架构 / 已反复沉淀的踩坑命中较稳
- 当前短板：新近高价值决策、外部研究资产边界、今晚新增工具坑
- 结论：Layer 2 对“长期稳定记忆”表现较强，但对“刚沉淀的新原子记忆”仍需补强

---

## Scorecard

| ID | Query | Category | Expected target | Top1 hit | Top3 hit | Noise present | Conflict recall | Needs Layer3 | Notes |
|----|-------|----------|-----------------|----------|----------|---------------|-----------------|--------------|-------|
| Q01 | 晨星要求默认使用什么浏览器读取 X 网页内容？ | user-preference | 托管浏览器优先，不用本地浏览器 / `profile="user"` | N | N | Y | N | N | 命中旧决策与无关规则，未稳中今晚新偏好 |
| Q02 | 晨星对沟通风格的核心偏好是什么？ | user-preference | 简洁有力，默认执行，不反复确认 | N | Y | Y | N | N | 命中 Telegram/中文等基础事实，偏好未直接顶到 Top1 |
| Q03 | Main 编排时能不能直接编辑应用代码？ | system-rule | 不能，必须 spawn coding agent | Y | Y | N | N | N | 命中稳定，表现好 |
| Q04 | Heartbeat 发现 cron 错误时应该如何判断 memory 是否真的坏了？ | system-rule | 先做分层判断，区分 Layer1/Layer2/rerank/cron | N | N | Y | N | N | 命中旧配置守护与 cron 错误记忆，未打中新分层规则 |
| Q05 | StarChain v2.9 plugin suite 当前能否说具有统计学显著性？ | recent-decision | 不能，只能说工程有效 | N | N | Y | N | N | 未命中今晚新决策 |
| Q06 | 如果后续想逼近统计学意义，优先补什么？ | recent-decision | 扩样本、baseline/弱对照、硬指标 | N | N | Y | N | N | 命中“先查上下文”等旧规则，不相关 |
| Q07 | `read` / `write` / `edit` 工具使用路径时有什么已知坑？ | pitfall | 不要依赖 `~` 展开，优先绝对路径 | N | Y | Y | N | N | 命中到别的工具坑，路径坑未稳定在 Top1 |
| Q08 | 小红书发布时标签为什么会变成正文文本？ | pitfall | 绕过 pipeline，标签未进话题选择器 | N | Y | Y | Y | N | 命中两条互相竞争的旧/新记忆，需去重与提纯 |
| Q09 | 本地 rerank sidecar 之前为什么启动失败？ | pitfall | 损坏 `.venv/bin/python3` 缺失 `libpython3.12.dylib` | N | N | Y | N | N | 召回到技术栈配置而非故障根因 |
| Q10 | Berryxia 那篇 X 长文在系统里应被当成什么？ | research-asset | 外部研究资产，不是 internal canonical | N | N | Y | N | N | 命中到更旧的 Berryxia 对比分析 |
| Q11 | Berryxia 材料当前优先入库到哪里？ | research-asset | NotebookLM `media-research` | N | N | Y | N | N | 未命中今晚 source 入库决策 |
| Q12 | Berryxia 材料优先使用哪份更干净的 source？ | research-asset | `article-archive.md` | N | N | Y | N | N | 命中无关 NotebookLM 历史记忆 |
| Q13 | 记忆系统当前的三层分别是什么？ | operational | Layer1 文件 / Layer2 lancedb / Layer3 NotebookLM | N | Y | Y | N | N | 命中旧三层架构定义，但夹带旧 notebook id 信息 |
| Q14 | memory 系统异常时，哪类错误更像执行链路问题而不是 memory failure？ | operational | `network connection error` / `timeout` / delivery | N | Y | Y | N | N | 命中到“要主动记录”之类旧规则，未稳中最新分层判断 |
| Q15 | `message(action=send)` 最近确认过的工具层坑是什么？ | operational | 误要求 `buttons`，可传 `buttons=[]` | N | N | Y | N | N | 今晚新坑尚未形成稳定 recall |

---

## 阶段结论

### 强项
- 稳定系统规则
- 反复沉淀的长期约束
- 旧架构信息

### 弱项
- 今晚刚确认的新偏好
- 今晚刚形成的新决策
- 外部研究资产边界
- 刚新增的工具级 workaround

### 建议动作
1. 补高价值原子记忆（已开始）
2. 对互相竞争的旧/新记忆做后续提纯
3. 随后立即跑 Round 2 复测，观察新原子记忆是否进入 Top1/Top3
