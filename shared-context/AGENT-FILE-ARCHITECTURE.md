# AGENT-FILE-ARCHITECTURE.md

> 2026-03-28 纠偏版。
> 核心目标:**文件语义固定,文件数量可增长。**
> 这套多智能体架构的重点不是把 sub-agent 永远压成最少文件,而是让同一套模型随着真实使用,通过越来越丰富的文件系统持续进化。

---

## README 原则(当前最高口径)

> 这个结构会随着使用持续进化。第 1 天和第 40 天用的是同一个模型,区别在于这些不断变丰富的文件。

这句话的含义是:
- 文件不是噪音,而是系统进化载体
- 我们追求的是**主语清晰**,不是**文件越少越好**
- sub-agent 可以从最小骨架起步,但不能被静态锁死在三件套

---

## 一句话总纲

- `IDENTITY.md`:名片
- `SOUL.md`:人格与边界
- `AGENTS.md`:执行手册(sub-agent 默认也承载"服务对象"段)
- `HEARTBEAT.md`:值班清单
- `TOOLS.md`:环境坑位
- `MEMORY.md`:长期伤疤与护栏
- `memory/YYYY-MM-DD.md`:当天账本与晋升池

重点:
**这些文件的语义是固定的;是否存在、长到多厚,取决于真实使用。**

---

## 主语矩阵

| 文件 | 主语 | 回答的问题 |
|------|------|------------|
| `IDENTITY.md` | agent 自己 | 我是谁 |
| `SOUL.md` | agent 自己 | 我怎么判断和行动 |
| `AGENTS.md` | 当前执行单元 | 我这类任务通常怎么跑 |
| `HEARTBEAT.md` | 值班动作 | 查什么、何时报警 |
| `TOOLS.md` | 本地环境 / 工具链 | 这套工具和环境有什么坑 |
| `MEMORY.md` | 长期学习结果 | 我们学到了什么 |
| `memory/YYYY-MM-DD.md` | 当天事实与判断 | 今天发生了什么 |

---

## 文件职责

### `IDENTITY.md`
只做身份卡。

放:
- 名字
- 角色
- 气质
- emoji
- 灵感来源

不放:
- 大段规则
- 流程说明
- 历史记录

### `SOUL.md`
只放 agent 自己的内在操作方式。

标准骨架:
- 核心身份
- 你的角色
- 你的原则
- 你的边界
- 你的风格

### sub-agent 的"服务对象"信息
默认写入 `AGENTS.md` 的"服务对象"段,而不是机械恢复独立 `USER.md`。

适合承载:
- 服务对象基本信息
- 协作偏好
- 少量稳定硬规则

什么时候才恢复独立 `USER.md`:
- 这个 agent 长期直接面向服务对象
- 服务对象上下文已经厚到会显著挤压 `AGENTS.md`
- 独立文件能减少长期重复编辑成本

### `AGENTS.md`
执行手册,不是人格文件。

适合承载:
- 每次会话先读什么
- 职责
- 执行规则
- 通知规则
- 记忆规则
- 稳定的任务 contract / handoff 习惯

什么时候该长出来:
- 该 agent 已经形成稳定、重复、可复用的工作流
- 单靠 `SOUL.md` 已不足以承载执行规则

### `HEARTBEAT.md`
值班 runbook。

适合承载:
- 检查项
- 具体命令
- 时间条件
- 异常输出格式

### `TOOLS.md`
只记环境的脾气。

适合承载:
- 路径坑
- schema 坑
- CLI / gateway / proxy / 浏览器怪癖
- 工作目录约定
- 输入输出路径

什么时候该长出来:
- 这个 agent 有自己稳定的工具链坑位
- 这些坑放在 root `TOOLS.md` 太细,放在 `MEMORY.md` 又会混主语

### `MEMORY.md`
只放长期内容,不放当天流水账。

推荐保留四类:
1. 血泪教训
2. 错误示范 / 反模式
3. 长期稳定规则
4. 少量长期偏好

什么时候该长出来:
- 该 agent 已有高代价、可复发、agent-specific 的长期伤疤
- 这些内容值得沉淀,不该每次临时重讲

### `memory/YYYY-MM-DD.md`
当天作战日志。

适合承载:
- 当天事件
- 当天判断
- 当天错误
- 当天修复
- 当天待跟进
- 值得后续晋升到 `MEMORY.md` 的候选项

什么时候该长出来:
- 这个 agent 的日常工作已经积累到"当天账本有独立价值"
- 需要保留 agent 自己的连续作战上下文

---

## Main 与 sub-agent 的关系

### Main
main 是系统级 owner,天然拥有完整控制面。

### Sub-agent
sub-agent 不是"固定三件套机器"。

更准确的说法是:
- **Day 1**:可以只靠最小骨架启动
- **Day 40**:应该因为真实使用而长出更多文件

所以:
- `IDENTITY.md` / `SOUL.md` / `HEARTBEAT.md` 常常是最小启动骨架
- 但它们**不是上限**
- `USER.md` / `TOOLS.md` / `MEMORY.md` / `AGENTS.md` / `BOOTSTRAP.md` / agent `memory/` 都可以随着使用自然长出

判断标准不是"这是不是例外",而是:
1. 有没有真实价值
2. 主语是否清晰
3. 能否减少重复 prompt / 重复踩坑 / 重复解释
4. 是否真正帮助该 agent 在未来做得更好

---

## 设计原则

### 1. 主语清晰 > 文件数量少
把文件压少不是目标。
目标是每个文件都知道自己在回答什么问题。

### 2. 最小启动可以轻,长期运行必须会长
新 agent 可以很轻。
成熟 agent 不应被人为削成"瘦身模板"。

### 3. 文档增长应该由真实使用驱动
- 重复出现的 handoff → 长成 `AGENTS.md`
- 重复出现的工具坑 → 长成 `TOOLS.md`
- 重复出现的服务对象偏好 → 写入 `AGENTS.md` 的"服务对象"段(sub-agent),或长成独立 `USER.md`(main / 特殊长期 agent)
- 重复出现的伤疤 → 长成 `MEMORY.md`
- 重复出现的日级上下文 → 长成 agent `memory/`

### 4. 反对两种极端
- 极端 A:什么都塞进一个文件,主语混乱
- 极端 B:把所有 agent 永远压成三件套,拒绝成长

正确做法是:
**语义拆清,同时允许增长。**

---

## 当前落地决策（2026-03-28）

1. root 继续保留完整控制面
2. README 的"持续进化"原则高于"默认三件套上限"口径
3. sub-agent 最小骨架：`SOUL.md` + `IDENTITY.md` + `AGENTS.md`（含服务对象段）+ `memory/`
4. `HEARTBEAT.md` / `TOOLS.md` / `MEMORY.md` / `BOOTSTRAP.md` 按真实使用自然长出
5. 服务对象信息默认收敛到 `AGENTS.md` 的"服务对象"段，不再默认恢复独立 `USER.md`
6. 协作产物走 `intel/collaboration/{starchain|stareval|media}/`，不存 agent 私有 `reports/`
7. 后续判断文件是否保留，只看真实价值与主语清晰度，不做 blanket trimming

## 跨 agent 共享文档

| 文件 | 主语 | 作用 |
|------|------|------|
| `shared-context/THESIS.md` | 整个实例 | 当前世界观 / 总判断 / 主线优先级 |
| `shared-context/FEEDBACK-LOG.md` | 全体 agent | 跨 agent 纠偏账本（含失效管理） |
| `shared-context/SIGNALS.md` | 外部世界 | 外部信号池 / 趋势 / 来源 |
| `shared-context/PATHS.md` | 系统 | 路径索引 |
| `shared-context/AGENT-FILE-ARCHITECTURE.md` | 架构 | 文件语义与边界 |

---

**维护者**:main(小光)
**生效时间**:2026-03-28
