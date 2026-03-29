# MEMORY-ARCHITECTURE.md

> 2026-03-28 最终收口版。
> 目标不是继续加结构，而是把三层记忆系统的职责、边界、维护动作和反模式彻底钉死，避免再次漂移。

---

## 一句话总纲

- **Layer 1**：文件层 — 原始记录、长期护栏、人类可读
- **Layer 2**：召回层 — 日常快速检索
- **Layer 3**：深理解层 — 归档、深研究、跨会话洞察

正确主链：

```text
Layer 1 沉淀事实与护栏
    ↓ 自动捕获 / 索引
Layer 2 负责 90% 日常召回
    ↓ 需要深理解时再升级
Layer 3 做长期归档与深推理
```

不是三层一起抢活。
不是所有问题都往 Layer 3 推。
不是所有内容都写进 MEMORY.md。

---

## Layer 1 — 文件层

### 作用
- 人类可读
- 可追溯
- 结构化沉淀长期护栏
- 为 Layer 2 / Layer 3 提供高质量上游材料

### 组成
- `MEMORY.md` — 长期护栏
- `memory/YYYY-MM-DD.md` — 当天账本与晋升池
- `shared-context/` — 跨 agent 知识
- `intel/` — 情报与协作层
- sub-agent `MEMORY.md` — agent-specific 长期伤疤

### root `MEMORY.md` 的职责
只放系统级、跨 agent、长期有效的内容。

统一骨架：
1. 血泪教训
2. 错误示范 / 反模式
3. 长期稳定规则
4. 长期偏好

### sub-agent `MEMORY.md` 的职责
只放这个 agent 自己会反复踩、代价高、已经验证的长期伤疤。

统一骨架同 root：
1. 血泪教训
2. 错误示范 / 反模式
3. 长期稳定规则
4. 长期偏好（可选）

### 写入门槛
至少满足以下 3 条才进 `MEMORY.md`：
- 高代价
- 可复发
- 已验证
- 长期有效
- 不写进去以后大概率还会再犯

### `memory/YYYY-MM-DD.md` 的职责
这是**当天账本**，不是长期护栏。

放：
- 当天事件
- 当天判断
- 当天错误
- 当天修复
- 待后续晋升到 `MEMORY.md` 的候选项

不放：
- 已经稳定的长期规则（应晋升后移入 `MEMORY.md`）

### Layer 1 反模式
- 把执行手册写进 `MEMORY.md`
- 把路径说明写进 `MEMORY.md`
- 把模板 / contract / workflow 写进 `MEMORY.md`
- 把当天流水账长期堆在 `MEMORY.md`
- 因为“看起来重复”就 blanket trimming 文件

这些内容应分别进入：
- `AGENTS.md`
- `TOOLS.md`
- `memory/YYYY-MM-DD.md`

---

## Layer 2 — 召回层

### 作用
- 日常快速检索
- 运行时 recall
- 90% 场景下的主召回层

### 组成
- `memory-lancedb-pro`
- 向量检索 + keyword / BM25 + rerank
- 自动捕获 / 自动召回

### 正确定位
Layer 2 是**主召回层**，不是：
- 人工档案系统
- 长期规则手册
- NotebookLM 替代品

### 当前口径
- 优先保证 recall 稳定、噪音低、rerank 正常
- 问题优先按层判断：
  - rerank sidecar 异常 = 重排退化
  - recall 失败 = Layer 2 链路问题
  - cron timeout ≠ Layer 2 故障

### Layer 2 噪音治理
重点清理：
- `Conversation info (untrusted metadata)`
- `Sender (untrusted metadata)`
- WhatsApp gateway connect / disconnect 包络
- heartbeat ack
- 其他纯系统 envelope

### Layer 2 反模式
- 把系统包络当有效记忆
- 把单次 timeout 误判成记忆系统故障
- 看到 recall 结果差就盲目继续加结构

---

## Layer 3 — 深理解层

### 作用
- 长期归档
- 深研究
- 跨会话分析
- 需要“整本理解”时的升级层

### 正确定位
Layer 3 是**深理解层**，不是：
- 日常主召回层
- 所有问题的默认 fallback
- 只要红灯就怀疑它坏了的背锅层

### 什么时候用 Layer 3
- Layer 2 命中不足，但问题需要更长时间跨度
- 需要整合多周 / 多月材料
- 需要 NotebookLM 的研究或深推理能力

### Layer 3 反模式
- 把所有复杂问题都升级到 Layer 3
- 单次同步失败就定性为 Layer 3 架构损坏
- 把本应留在对应 sub-agent 的工具坑全写回 root MEMORY

---

## 三层边界

### 正确分工
- **Layer 1** 负责“写什么、沉淀什么、长期护栏是什么”
- **Layer 2** 负责“平时怎么快速想起来”
- **Layer 3** 负责“需要整本书级理解时怎么深挖”

### 错误分工
- Layer 1 什么都不写，指望 Layer 2 / 3 自己懂
- Layer 2 承担长期护栏语义
- Layer 3 被当作日常主召回层

---

## 维护策略

### control-plane 负责的维护类动作
默认由 `control-plane` 承担：
- health check
- quality audit
- 压缩 / 归档
- 周期报告
- 观察期维护

### main 不再承担
- routine heartbeat
- routine cron 宿主
- 维护类定时任务执行

### 重大调整后的规则
一旦对记忆系统做了结构级调整：
1. 写入 `master-execution-plan.md`
2. 运行观察 2-3 天
3. 用 control-plane 自动维护观察期
4. 只根据真实使用反馈做下一轮小修
5. 不在同一天反复继续加结构

---

## 这次收口后的最终反模式清单

### 不再做
- 把记忆优化做成“到处加 cron / 到处加机制”
- 把 `MEMORY.md` 当万能杂物箱
- 把执行链路问题误报成记忆系统故障
- 把“结构优化”理解成继续扩张或继续瘦身
- 因为形式一致而继续动刀

### 只做
- 主语纠偏
- 噪音治理
- 真实痛点驱动的小修
- 观察后再收口

---

## 最终判断标准

如果未来再优化记忆系统，只问 4 个问题：
1. 这是 Layer 1 / Layer 2 / Layer 3 的哪一层问题？
2. 这是主语错位，还是链路故障，还是噪音问题？
3. 这个改动是解决真实痛点，还是在修景观？
4. 这次改动是否值得进入观察期？

答不清这 4 个问题，就先别动。

---

**最后更新**: 2026-03-28 15:50
**维护者**: main（小光）
