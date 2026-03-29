# Memory Recall Benchmark Lite

日期：2026-03-26
目的：用一套小而稳的查询集观察 recall 质量变化，避免只靠体感判断。

## 使用规则

- 这是 benchmark 定义文件，不记录每日结果
- 每次测试请把结果写到独立 scorecard
- 如果标准答案因真实决策变化而漂移，显式标注“基准漂移”
- 不要偷偷改 query 以迎合当前系统表现

---

## Scorecard 字段建议

- Query
- Category
- Expected target
- Top1 hit (Y/N)
- Top3 hit (Y/N)
- Noise present (Y/N)
- Conflict recall (Y/N)
- Needs Layer3 (Y/N)
- Notes

---

## Benchmark Queries

| ID | Category | Query | Expected target |
|----|----------|-------|-----------------|
| Q01 | user-preference | 晨星要求默认使用什么浏览器读取 X 网页内容？ | 托管浏览器优先，不用本地浏览器 / `profile="user"`，除非明确指定 |
| Q02 | user-preference | 晨星对沟通风格的核心偏好是什么？ | 简洁有力，默认执行，不反复确认 |
| Q03 | system-rule | Main 编排时能不能直接编辑应用代码？ | 不能，必须 spawn coding agent；系统文件例外 |
| Q04 | system-rule | Heartbeat 发现 cron 错误时应该如何判断 memory 是否真的坏了？ | 先做分层判断，区分 Layer1 / Layer2 / rerank / cron timeout |
| Q05 | recent-decision | StarChain v2.9 plugin suite 当前能否说具有统计学显著性？ | 不能；只能说首轮真实验证完成、工程有效 |
| Q06 | recent-decision | 如果后续想逼近统计学意义，优先补什么？ | 扩样本、加 baseline/弱对照、用更硬指标 |
| Q07 | pitfall | `read` / `write` / `edit` 工具使用路径时有什么已知坑？ | 不要依赖 `~` 展开，优先绝对路径 |
| Q08 | pitfall | 小红书发布时标签为什么会变成正文文本？ | 绕过 pipeline 导致标签未进入话题选择器，只被当正文 |
| Q09 | pitfall | 本地 rerank sidecar 之前为什么启动失败？ | 损坏 `.venv/bin/python3` 缺失 `libpython3.12.dylib` |
| Q10 | research-asset | Berryxia 那篇 X 长文在系统里应被当成什么？ | 外部研究/内容/叙事参考源，不是内部 canonical 规则 |
| Q11 | research-asset | Berryxia 材料当前优先入库到哪里？ | NotebookLM `media-research` |
| Q12 | research-asset | Berryxia 材料优先使用哪份更干净的 source？ | `article-archive.md` |
| Q13 | operational | 记忆系统当前的三层分别是什么？ | Layer 1 本地文件，Layer 2 memory-lancedb-pro，Layer 3 NotebookLM |
| Q14 | operational | memory 系统异常时，哪类错误更像执行链路问题而不是 memory failure？ | `network connection error` / `timeout` / delivery 报错 |
| Q15 | operational | `message(action=send)` 最近确认过的工具层坑是什么？ | 部分路径会误要求 `buttons`，可用 `buttons=[]` 绕过 |

---

## 结果解释建议

### 好
- Top1 命中率高
- Top3 基本可找回
- 噪音少
- 几乎无冲突召回

### 可接受
- Top1 不稳定，但 Top3 可找回
- 个别 query 需要 Layer3
- 有少量噪音但不影响判断

### 需要优化
- Canonical internal 和 research asset 混淆
- 用户偏好类命中不稳
- 已知踩坑类 recall 漏掉
- 出现冲突召回或旧规则压过新规则
