# Builtin memorySearch vs memory/archive 冲突方案比较 — 2026-03-14

## 已确认事实
1. OpenClaw builtin memorySearch 默认会索引 `MEMORY.md` + `memory/**/*.md`
2. docs/配置中**没有找到** builtin memorySearch 的 exclude / ignore archive 开关
3. 当前 `memory/archive/` 下存在超大归档文件，实际触发：
   - `Ollama embeddings HTTP 500: the input length exceeds the context length`
4. 当前生产主链路仍是 `memory-lancedb-pro`，builtin memorySearch 只是影子评估链路

---

## 方案 A：把 `memory/archive/` 挪出 `memory/`

### 做法
例如迁移到：
- `workspace/archive/memory/`
- 或 `workspace/memory-archive/`

### 优点
- 从根上解决 builtin 默认索引范围冲突
- 不需要改 OpenClaw core config
- 后续 builtin memorySearch benchmark 才能公平进行

### 风险
- 需要检查所有脚本/文档/cron 是否硬编码依赖 `memory/archive/`
- 会改变当前三层记忆架构文档描述
- 需要一次性迁移已有归档文件

### 适用前提
- 确认项目内没有强依赖 `memory/archive/`
- 愿意接受一次目录规范调整

---

## 方案 B：保留 `memory/archive/`，关闭 builtin memorySearch 评估线

### 做法
- 不再继续评估 builtin memorySearch
- 保留 `memory-lancedb-pro` 为唯一主力
- 把优化重点继续放在主插件 recall 质量与记忆内容治理

### 优点
- 零迁移风险
- 不改目录结构
- 当前生产最稳

### 风险
- 放弃对 OpenClaw 最新 builtin 记忆能力的跟进
- hybrid/MMR/temporalDecay/sessionMemory 暂时无法落地评估

### 适用前提
- 近期目标以稳定为先
- 接受 builtin 先搁置

---

## 方案 C：临时缩小 archive 内容规模，但不改目录

### 做法
- 继续把超大文件压缩/拆分
- 尽量让 `memory/archive/` 中不再保留超长单文件

### 优点
- 不用改目录结构
- 可能缓解 builtin sync 失败

### 风险
- 这是治标不治本
- 只要后续再出现大归档文件，builtin 又会被打爆
- 会把 archive 维护逻辑变复杂

### 适用前提
- 只想短期试跑 builtin，不想动目录结构

---

## 当前推荐
**推荐顺序：B > A > C**

### 为什么先推荐 B
因为当前：
- 生产主链路健康
- builtin 只是影子线
- 目录迁移属于架构动作，不是必须立即做

所以最稳的策略是：
1. 先维持现状
2. 完成 7 天观察期与 benchmark 设计
3. 如果确定要认真评估 builtin memorySearch，再做方案 A

### 什么时候切到 A
满足以下两个条件时再迁移最合理：
- 确认 builtin memorySearch 确实值得继续跟
- 确认项目内无硬依赖 `memory/archive/`

---

## 一句话结论
> 当前最稳妥的做法不是立刻迁移 archive，而是先把 builtin memorySearch 明确为“暂缓评估的影子线”；等需要认真评估时，再把 archive 移出 `memory/`。