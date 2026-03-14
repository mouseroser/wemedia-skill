# NotebookLM 功能扩展规划 v2.0

**制定日期**: 2026-03-09
**合并来源**: 00:30 初版规划 + 09:20 扩展版规划
**负责人**: 小光 (main agent)
**审核人**: 晨星
**状态**: Draft -> Review -> Active

---

## 一、规划目标

这版规划以"先解决当前痛点，再逐步平台化"为原则，不追求一口气做大，而是分三层推进：

1. 先把零散经验变成可查询、可复用的知识库
2. 再让 NotebookLM 真正进入多智能体协作链路
3. 最后再做自动沉淀、联合查询、推荐和图谱

核心定位不是"多建几个 notebook"，而是把 NotebookLM 从当前的辅助查询工具，升级成：

- 故障排查知识中心
- 项目演进档案库
- 多智能体共享知识层
- 流水线中的动态补料系统

---

## 二、当前现状

### 已有共享层架构

你的系统已经有完整的多层共享架构：

**文件系统共享层**：
- `shared-context/` (THESIS.md, FEEDBACK-LOG.md, SIGNALS.md)
- `intel/` (agent 间协作文件，单写者原则)
- `intel/collaboration/` (多 agent 联合工作的非正式材料)

**记忆共享层**：
- `memory/YYYY-MM-DD.md` (日志)
- `MEMORY.md` (长期记忆，main session only)
- memory-lancedb-pro (向量数据库，刚接入，观察期)

**NotebookLM 共享层**：
- `memory`: Agent 共享记忆和上下文
- `openclaw-docs`: OpenClaw 配置、故障、架构、命令专用
- `media-research`: 自媒体调研知识库

### 当前已知约束

- `openclaw-docs` 只能用于 OpenClaw 自身问题，不能泛化使用
- notebook 删除重建后必须立即同步 `config/notebooks.json`
- NotebookLM 当前在星链和自媒体里已接入，但仍偏"点状使用"
- MEMORY.md 中已有大量踩坑记录，但尚未结构化进入专门问题库

### 当前主要痛点

NotebookLM 的真正问题不是"没有共享层"，而是：

1. **结构化检索能力不足**：踩坑经验分散在 `MEMORY.md` / `memory/*.md`，文件系统共享层难以精确检索
2. **领域知识库覆盖不够**：只有 3 个 notebook，无法覆盖故障排查、项目档案、技术栈、智能体协作等关键领域
3. **自动化程度低**：还没有形成自动沉淀和主动推送能力，依赖手动维护
4. **可靠性保障缺失**：NotebookLM 不可用时，缺少明**流程集成浅**：虽然已接入星链和自媒体，但仍偏"点状使用"，未深度融入流程

**NotebookLM 的定位**：
- 不是替代现有共享层，而是增强它
- 补充文件系统共享层的"结构化检索"能力
- 补充记忆共享层的"领域知识库"能力
- 与 memory-lancedb-pro 形成互补（NotebookLM 做领域知识，LanceDB 做记忆检索）

---

## 三、总体策略

采用"两条主线 + 一条保障线"推进：

### 主线 A：知识库建设
先补最有价值的 notebook，优先解决"问题找不到答案"和"经验无法复用"的问题。

### 主线 B：流水线集成
把 NotebookLM 从手动工具变成星链 / 自媒体流程中的标准部件。

### 保障线：运行可靠性
补齐 ACL、缓存 TTL、故障降级、更新 SOP，避免知识系统越做越脆。

---

## 四、Notebook 规划（合并优化后）

### P0：立即建设

#### 1. `troubleshooting`
定位：问题解决库，优先级最高

内容范围：
- 常见问题和解决方案
- 从 `MEMORY.md` 提取的踩坑记录
- OpenClaw / Telegram / memory / NotebookLM / workflow 配置坑
- 最佳实践总结
- 配置模板和最小可行示例

价值：
- 直接提高排障效率
- 最快产生可见收益
- 适合先建立结构化模板

#### 2. `project-archives`
定位：项目档案库

内容范围：
- 星链流水线演进历史
- 自媒体流水线优化记录
- 重要项目完整文档
- ADR（架构决策记录）
- 关键版本变更与回滚记录

价值：
- 把"为什么这样设计"保存下来
- 方便回顾历史决策和版本分歧

### P1：本周到下周建设

#### 3. `tech-stack`
定位：技术栈知识库

内容范围：
- OpenClaw 深度使用资料（非官方部分放这里，不放 openclaw-docs）
- Ollama 使用指南
- LanceDB / memory-lancedb-pro 实战经验
- Telegram Bot 配置经验
- 常用脚本、环境、依赖链说明

#### 4. `agent-knowledge`
定位：智能体共享知识库

内容范围：
- 各 agent 职责边界
- 协作案例
- 模型选择与调优记录
- 多 agent 编排经验
- 推送、补发、announce、职责分工约定

#### 5. `ideas-vault`
定位：灵感与创意库

内容范围：
- 待实现功能想法
- 外部方案吸收记录
- 实验性项目草案
- 优化方向池

### P2：第二阶段补齐

#### 6. `starchain-knowledge`
定位：星链案例知识库

内容范围：
- L2/L3 历史案例
- 成功交付案例
- 失败 Epoch 复盘
- 阶段性策略和 best practices

说明：
- 这个 notebook 保留，但不放到最前面做
- 它更适合在 `project-archives` 有基础之后再沉淀案例级知识

#### 7. `content-templates`
定位：自媒体内容模板库

内容范围：
- 不同平台模板
- 爆款结构
- 风格规范
- 选题与改写模板

#### 8. `review-patterns` / `test-strategies`
定位：代码审查与测试专项知识库

说明：
- 这两个属于二级优化项
- 等主干 notebook 成熟后再拆分最合理
- 前期可先把相关内容归入 `troubleshooting` / `agent-knowledge`

---

## 五、分阶段执行方案

## Phase 1：基础知识库建设（1-2 周）

目标：先把最值钱、最常用、最容易散掉的知识收拢起来。

### 任务 1：建立 `troubleshooting`

执行内容：
- 从 `MEMORY.md` 提取踩坑记录
- 从最近 `memory/*.md` 提取高频问题
- 统一整理成结构化条目

推荐条目模板：

```md
# 问题标题

## 现象
...

## 根因
...

## 解决方案
...

## 相关配置/命令
...

## 适用范围
...

## 备注
...
```

优先收录类别：
- Telegram 配置坑
- openclaw.json 字段坑
- memory / embeddings / Ollama 坑
- NotebookLM notebook ID / proxy / auth 坑
- sessions / bindings / group 配置坑

### 任务 2：建立 `project-archives`

执行内容：
- 整理星链 v2.5 演进过程
- 整理自媒体流程版本演进
- 整理 NotebookLM skill 接入过程和关键决策
- 建立 ADR 模板

推荐目录结构：

```text
project-archives/
  starchain/
  wemedia/
  notebooklm/
  adr/
```

### 任务 3：补 `tech-stack`

执行内容：
- 补 Ollama 使用说明
- 补 LanceDB / memory-lancedb-pro 实战记录
- 补 Telegram Bot 配置经验
- 补本地服务与 sidecar 经验

### Phase 1 验收标准

- `troubleshooting` 中至少整理 20 条高价值问题条目
- `project-archives` 中至少完成星链 v2.5 和 NotebookLM 接入两条主档案
- `tech-stack` 至少覆盖 Ollama / LanceDB / Telegram 3 个主题
- 每个 notebook 都已写入注册表并可查询

---

## Phase 2：智能体协作增强（2-4 周）

目标：让 NotebookLM 真正进入 agent 协作链路，而不只是 main 手动查。

### 任务 4：建立 `agent-knowledge`

执行内容：
- 整理各 agent 的职责边界
- 汇总多 agent 协作案例
- 总结模型切换策略
- 提炼通知/补发/审查/执行的边界规则

### 任务 5：建立 `ideas-vault`

执行内容：
- 把零散想法统一归档
- 外部方案吸收后存入创意池
- 给后续产品化做储备

### 任务 6：接入流程查询点

优先接入：
- 星链 Step 1.5S：查询 `project-archives` / `troubleshooting` / `starchain-knowledge`
- 星链 Step 5.5：查询历史失败案例和回滚经验
- 自媒体调研：查询 `media-research` + `content-templates`
- 问题诊断：优先查 `troubleshooting`

### 任务 7：优化 ACL 和 notebook 使用边界

目标：谁能写、谁能读、谁能查什么，要明确。

建议方向：
- `main`: admin
- `notebooklm`: admin 或 contributor
- `coding/review/test/docs`: reader 或 contributor（按 notebook 精细化）
- `wemedia/gemini/brainstorming`: 对对应 notebook 有 contributor 权限

### Phase 2 验收标准

- 至少 5 个 agent 开始稳定使用 notebook
- 星链 / 自媒体至少各有 2 个固定接入点
- ACL 配置完成细化，不再只有粗粒度权限
- 智能体能根据任务类型选择合适 notebook

---

## Phase 3：自动化和集成（1-2 个月）

目标：把手动维护变成自动沉淀和自动补料。

### 任务 8：自动知识沉淀

沉淀方向：
- 每周从 `memory/*.md` 提取重要内容进入对应 notebook
- 自动生成项目进展报告
- 完成任务后归档到 `project-archives`
- 高价值故障案例自动进入 `troubleshooting`

建议优先自动化的对象：
1. `troubleshooting`
2. `project-archives`
3. `starchain-knowledge`

### 任务 9：主动知识推送

目标：不是等 agent 来查，而是在关键阶段自动补料。

典型场景：
- coding 开始前，自动推送相关技术文档
- review 开始前，自动推送历史类似问题
- main 做需求分级时，自动推送历史相似案例

### 任务 10：跨 notebook 联合查询

目标：支持一个问题同时查多个 notebook，然后融合结果。

建议查询组合：
- 故障排查：`troubleshooting + tech-stack + openclaw-docs`
- 流水线决策：`project-archives + starchain-knowledge + agent-knowledge`
- 自媒体创作：`media-research + content-templates + ideas-vault`

### 任务 11：故障降级机制

原则：NotebookLM 失败不能卡死主流程。

降级顺序：
1. 优先使用缓存结果
2. 再退回本地结构化 markdown 文档
3. 必要时退回 `MEMORY.md` / `memory/*.md`
4. 流程继续推进，同时记录一次降级事件

### Phase 3 验收标准

- 每周自动沉淀机制可运行
- 至少 3 类任务支持主动补料
- 跨 notebook 联合查询可用
- NotebookLM 不可用时有明确降级路径

---

## Phase 4：长期增强（持续进行）

目标：做真正的数据驱动优化，而不是只堆文档。

### 可持续优化项

1. 知识图谱
- 将项目、问题、方案、模型、智能体之间建立关联

2. 智能推荐
- 根据任务上下文自动推荐最相关 notebook 和条目

3. 质量管理
- 识别过期内容
- 清理重复条目
- 标记低质量知识

4. 使用分析
- 统计查询频率、命中率、解决率、更新频率

---

## 六、优先级重排（最终版）

### P0（立即开始）
1. `troubleshooting`
2. `project-archives`
3. 故障降级机制设计

### P1（本周）
1. `tech-stack`
2. `agent-knowledge`
3. ACL 精细化

### P2（下周）
1. `ideas-vault`
2. 星链 / 自媒体固定接入点落地
3. 动态 TTL / 缓存优化

### P3（本月）
1. 自动知识沉淀
2. 主动知识推送
3. 跨 notebook 联合查询

### P4（后续增强）
1. `starchain-knowledge`
2. `content-templates`
3. `review-patterns` / `test-strategies`
4. 知识图谱 / 推荐系统

---

## 七、技术实现建议

### 1. 标准化模板先行
在自动化之前，先统一条目模板，否则越自动越乱。

优先模板：
- 故障条目模板
- 项目档案模板
- ADR 模板
- 智能体知识模板

### 2. 先人手整理，再自动化
前 1-2 周以人工整理为主，先确定结构和边界；不要一开始就全自动抓取。

### 3. 把 `openclaw-docs` 边界写死
明确规则：
- 只有 OpenClaw 自身问题才查 `openclaw-docs`
- 其他 notebook 查询不得默认走它

### 4. 缓存 TTL 动态化
建议方向：
- `openclaw-docs`: 长 TTL
- `memory`: 短 TTL
- `troubleshooting`: 中 TTL
- `project-archives`: 中长 TTL

### 5. ACL 精细化
不同 agent 对不同 notebook 用不同权限，避免所有人都能乱写。

---

## 八、度量指标（优化后）

### 建设指标
- 新增 notebook 数量
- 已结构化条目数量
- 已接入流程节点数量
- 已覆盖 agent 数量

### 使用指标
- 查询次数
- 查询命中率
- 查询后问题解决率
- 各 agent 使用频率

### 维护指标
- 每周新增条目数
- 每周更新条目数
- 过期条目比例
- 重复条目比例

### 价值指标
- 平均排障耗时是否下降
- 重复踩坑次数是否下降
- 流水线补料质量是否上升
- 历史案例复用率是否上升

---

## 九、动态调整机制

### 每周回顾
- 本周新建/更新了哪些 notebook
- 哪些 notebook 被实际使用了
- 哪些条目没价值或重复
- 下周优先补什么

### 每月调整
- 是否需要新增 notebook
- 是否有 notebook 应该合并或拆分
- 哪个阶段自动化值得推进

### 触发式调整条件
发生以下情况时，直接更新规划：
- NotebookLM API 或 CLI 大变更
- 星链 / 自媒体主流程调整
- 出现新的高频问题类型
- 晨星提出新的长期使用场景

原则：
- 规划是活的，不是一次写死
- 若连续三次在同一方向上收益不明显，就切换方向

---

## 十、建议的执行顺序

最务实的顺序是：

1. 先做 `troubleshooting`
2. 再做 `project-archives`
3. 然后补 `tech-stack`
4. 同时设计 ACL 和降级机制
5. 再推进 `agent-knowledge`
6. 等结构稳定后再做自动沉淀和主动推送

一句话总结：

**先把"问题能查到、历史能回看、协作有共识"做稳，再做自动化和智能化。**

---

## 十一、下一步

建议从以下 3 项里按顺序开始：

1. 整理 `MEMORY.md` 踩坑笔记，生成 `troubleshooting` 初始条目集
2. 整理星链 v2.5 / NotebookLM 接入过程，生成 `project-archives` 初始档案
3. 设计 NotebookLM 的 ACL v2 和降级策略草案

---

**版本历史**:
- v1.0 (2026-03-09): 初版扩展规划
- v2.0 (2026-03-09): 合并 00:30 版与 09:20 版，重排优先级，压实执行路径
