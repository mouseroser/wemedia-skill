# 记忆系统优化建议 v1

日期：2026-03-26

## 目标

本轮优化不重做三层记忆架构，而是在现有体系上做四个方向的轻量增强：

1. 分层健康检查（稳主链、减少误判）
2. 轻量 recall benchmark（让优化可测）
3. 外部研究资产分层治理（避免外部参考污染内部规则）
4. 教训型记忆优先（降低过程噪音）

---

## 方向 1：分层健康检查

### 现状问题
- heartbeat 里 memory、rerank、cron timeout、delivery 问题容易混报
- 多个 cron 同时 timeout 时，容易被误判成“记忆系统坏了”
- 实际上 Layer 1 / Layer 2 / rerank / cron 是不同层

### 本轮动作
- 已更新 `HEARTBEAT.md`
- 新增分层检查口径：
  - Layer 1 = 文件层
  - Layer 2 = 检索层
  - Rerank sidecar = 重排层
  - Cron / 模型调用 = 执行层
- 明确：`network connection error` / `timeout` 优先定性为执行链路问题，不直接报 memory failure

### 预期收益
- 减少误报
- 更快定位问题层级
- 下次断网时不再误判为 memory 崩溃

---

## 方向 2：轻量 recall benchmark

### 目标
建立一套小而稳的 benchmark，用来验证 recall 质量变化，而不是靠体感。

### 建议结构
维护 12-20 条固定查询，分 5 类：

1. 用户偏好类
2. 系统规则类
3. 最近决策类
4. 已知踩坑类
5. 外部研究资产类

### 建议记录字段
- Query
- Category
- Expected target
- Top1 hit
- Top3 hit
- Noise present
- Conflict recall
- Needs Layer3
- Notes

### 建议存放
- `reports/memory-recall-benchmark-lite.md`
- 后续每次验证结果追加到 scorecard，而不是改 benchmark 本体

### 预期收益
- recall 优化可比较
- rerank / prompt / capture 调整后能判断变好还是变差
- 减少“今天感觉还行”的主观判断

---

## 方向 3：外部研究资产分层治理

### 现状问题
像 Berryxia 这类高价值外部文章，既有研究价值，也有表达价值；如果边界不清，后续容易把外部参考当成内部 canonical 规则。

### 建议分类

#### A. Canonical internal
用于内部真相源：
- MEMORY.md
- AGENTS.md
- 已确认决策
- 内部规则与偏好

#### B. Operational memory
用于近期执行与排障：
- memory/YYYY-MM-DD.md
- `.learnings/ERRORS.md`
- 当日决策、故障、修复、执行状态

#### C. Research assets
用于外部参考与内容资产：
- NotebookLM `media-research`
- 外部长文 Markdown / 图片包
- 对外叙事、选题、表达框架资料

### 执行规则
- 外部文章默认入 `media-research`，不直接升格为内部 canonical
- 引用外部资料时，明确标注为“参考源 / 外部印证”
- 如果某条外部观点变成内部规则，必须经过一次显式决策再写入内部规则层

### 预期收益
- 降低知识边界混淆
- 提高 NotebookLM 研究资产复用率
- 防止“外部表达”污染“内部约束”

---

## 方向 4：教训型记忆优先

### 现状问题
系统已经能记很多东西，但长期最有价值的通常不是过程，而是：
- 踩坑
- 偏好变化
- 会改变执行路线的决策

### 建议优先写入内容
优先保留：
1. 已证实的踩坑与修复
2. 用户明确收紧 / 修改的偏好
3. 会影响未来行为的执行规则
4. 高复用的外部研究结论（但放研究资产层）

降权内容：
1. 单次成功过程
2. 普通完成通知
3. 无复用价值的中间状态
4. 已有完整日志覆盖的重复播报

### 写入判断问题
写之前先问自己：
- 这条信息 7 天后还值钱吗？
- 它会改变下一次做法吗？
- 它是规则 / 偏好 / 教训，而不只是过程吗？

如果三个问题都偏否，就不应占用高权重记忆位。

### 预期收益
- 提升 recall 精度
- 降低噪音记忆比例
- 让 memory 更像规则系统，而不是流水账

---

## 一周内可执行项

### 已完成
- [x] 更新 `HEARTBEAT.md`，加入分层健康检查口径
- [x] 明确外部研究资产与内部规则的边界

### 待做
- [ ] 建立 `reports/memory-recall-benchmark-lite.md`
- [ ] 先写 12 条 benchmark 查询
- [ ] 设计一个最简 scorecard 模板
- [ ] 挑 3 条已有外部研究资产，手动标注“external reference / not canonical”
- [ ] 回顾最近 7 天日志，抽样判断噪音占比

---

## 暂不建议做的

- 不重构三层记忆架构
- 不新增更多层级
- 不把所有外部资料塞进 canonical memory
- 不为了“更智能”而牺牲稳定性

---

## 当前优先级结论

### P1
1. 分层健康检查
2. 轻量 benchmark

### P2
3. 外部研究资产治理
4. 教训型记忆权重治理

---

## 一句话结论

当前记忆系统的最优优化路径不是推翻重来，而是：

**分层看健康、基准化看 recall、边界化管研究资产、提高教训型记忆权重。**
