# Memory Retrieval Benchmark — 2026-03-14

## 目标
建立一套后续可重复执行的 benchmark，用来评估：
- 中文语义召回
- 精确关键词召回
- 时间敏感召回
- 会话级短期记忆召回
- 结果重复度 / 歧义度

---

## 评分口径

### 每条查询记录 4 个维度
1. **命中率**
   - 2 = 直接命中核心答案
   - 1 = 命中相关内容但不够准
   - 0 = 未命中

2. **排名质量**
   - 2 = Top 1 就对
   - 1 = Top 3 内才对
   - 0 = Top 3 仍不对

3. **重复度**
   - 2 = 结果互补、不重复
   - 1 = 有少量重复
   - 0 = 多条结果其实在说同一件事

4. **时效性**
   - 2 = 优先召回最新/有效结论
   - 1 = 新旧混杂但仍可用
   - 0 = 旧结论抢排位

**单条满分：8 分**

---

## Benchmark 查询集

### A. 中文语义查询
1. 晨星主要用什么渠道联系？
   - 期望：Telegram / 1099011886
2. 主私聊会话有什么约束？
   - 期望：main 不承载长时间编排
3. 同一问题三次未解决怎么办？
   - 期望：必须切换方向
4. OpenClaw 有新版本时要做什么联动？
   - 期望：更新 `openclaw-docs` notebook

### B. 精确关键词查询
5. TODO 文件应该放在哪里？
   - 期望：`~/.openclaw/todo/`
6. 系统级 scripts 应该放在哪里？
   - 期望：`~/.openclaw/scripts/`
7. skill 自带脚本应该放在哪里？
   - 期望：skill 自己的 `scripts/` 目录
8. monitor-bot 的 chat id 是多少？
   - 期望：`-5131273722`
9. 当前主记忆插件是什么？
   - 期望：`memory-lancedb-pro`

### C. 时间敏感 / 最近决策
10. 升级到 memory-lancedb-pro@1.1.0-beta.8 后出现了什么回归？
   - 期望：`memory_list` / `memory_stats` 默认返回 0
11. 什么时候必须执行完整 openclaw gateway restart？
   - 期望：插件源码修复后，轻量 reload 不够
12. 记忆压缩检查的阈值是多少？
   - 期望：40k tokens

### D. 会话级短期记忆（后续专项）
13. 刚才新建的记忆检索优化 TODO 文件叫什么？
   - 期望：`memory-retrieval-optimization-2026-03-14.md`
14. 刚才确认的 builtin memorySearch 新阻塞点是什么？
   - 期望：`memory/archive/` 超长文件导致 embeddings context length 错误
15. 刚才决定的策略是什么？
   - 期望：先 benchmark / 不直接改配置 / 不切主插件

> 说明：13-15 依赖 sessionMemory 或当日日志写入，适合作为“短期会话记忆”专项测试。

---

## 当前初测结果

### memory-lancedb-pro / memory_recall

| 查询 | 结果 | 备注 |
|---|---:|---|
| TODO 文件应该放在哪里？ | 2/2 | 直接命中 `~/.openclaw/todo/` |
| 升级到 beta.8 后出现什么回归？ | 2/2 | 直接命中默认 0 条回归 |
| OpenClaw 新版本联动规则 | 2/2 | 直接命中 openclaw-docs 联动 |
| 主私聊会话有什么约束？ | 2/2 | 直接命中 |
| 同一问题三次未解决怎么办？ | 2/2 | 直接命中 |
| scripts 应该放在哪里？ | 1/2 | 命中两套规则，存在术语歧义 |

**初步判断**：主插件召回整体良好，主要问题是“词项歧义”，不是系统性不可用。

### OpenClaw builtin memorySearch

| 查询 | 结果 | 备注 |
|---|---:|---|
| TODO 文件应该放在哪里？ | 0/2 | No matches + sync failed |
| Telegram | 0/2 | No matches + sync failed |
| monitor-bot | 1/2 | 能命中旧日志，但每次伴随 sync failed |

**初步判断**：当前 builtin 先要解决索引范围 / 超长文件问题，不然 benchmark 成绩没有代表性。

---

## 关键 benchmark 注意事项
1. `scripts` 必须拆成：
   - 系统级脚本
   - skill 自带脚本
   否则问题本身含糊，会误判召回质量。
2. “会话级短期记忆”不能只看 memory files，需要单独验证 sessionMemory。
3. 如果 archive 继续放在 `memory/` 下，builtin memorySearch 的 benchmark 会长期失真。

---

## 下一步
1. 继续扩展 benchmark 到 15 条
2. 给每条查询定义“标准答案”
3. 在配置变更前后各跑一轮对比
4. 如果要认真评估 builtin memorySearch，先解决 archive 索引冲突