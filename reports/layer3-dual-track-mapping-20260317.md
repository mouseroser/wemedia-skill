# Layer 3 路线图落地映射表（TODO / cron / reports）

**创建时间**: 2026-03-17
**对应上游文档**: `reports/layer3-dual-track-roadmap-20260317.md`
**目的**: 把《Layer 3 后续优化路线图（本地版 / 上游版双轨）》直接映射到现有任务系统，明确：
1. 哪些已被现有 TODO 覆盖
2. 哪些已经挂到 cron
3. 哪些会产出到 reports
4. 哪些仍然缺正式任务位（需要后补）

---

# 一、已经有“正式任务位”的部分

## A. 4E 观察期（本地版主线）

### 已有 TODO 位
- `~/.openclaw/todo/master-execution-plan.md`
  - `4E.4` Day 4（03-18）
  - `4E.5` Day 5（03-19）
  - `4E.6` Day 6（03-20）
  - `4E.7` Day 7（03-21）
- `~/.openclaw/todo/memory-retrieval-optimization-2026-03-14.md`
  - `P2.2` 观察期 7 天
- `~/.openclaw/todo/memory-optimization-2026-03-13.md`
  - 观察期 Phase 6（对应 9.1 / 9.2 / 9.3）

### 已挂 cron
- `memory-observation-day4-20260318`
- `memory-observation-day5-20260319`
- `memory-observation-day6-20260320`
- `memory-observation-day7-20260321`

### 固定产出 reports
- `reports/memory-retrieval-scorecard-20260318.md`
- `reports/memory-retrieval-scorecard-20260319.md`
- `reports/memory-retrieval-scorecard-20260320.md`
- `reports/memory-retrieval-scorecard-20260321.md`
- 持续更新：`reports/memory-retrieval-observation-20260314.md`

---

## B. 9.1 / 9.2 / 9.3 两周观察期（日常验证）

### 已有 TODO 位
- `~/.openclaw/todo/master-execution-plan.md`
  - `9.1` 每日测试关键查询
  - `9.2` 记录召回准确率
  - `9.3` 记录是否有冲突记忆被召回
- `~/.openclaw/todo/memory-optimization-2026-03-13.md`
  - Phase 6 每日检查三项

### 已挂 cron
- `memory-optimization-daily-20260322`
- `memory-optimization-daily-20260323`
- `memory-optimization-daily-20260324`
- `memory-optimization-daily-20260325`
- `memory-optimization-daily-20260326`
- `memory-optimization-daily-20260327-final`

### 固定产出 reports
- `reports/memory-retrieval-scorecard-20260322.md`
- `reports/memory-retrieval-scorecard-20260323.md`
- `reports/memory-retrieval-scorecard-20260324.md`
- `reports/memory-retrieval-scorecard-20260325.md`
- `reports/memory-retrieval-scorecard-20260326.md`
- `reports/memory-retrieval-scorecard-20260327.md`
- 持续更新：`reports/memory-retrieval-observation-20260314.md` 的 extended observation 区块

---

## C. 观察期后续裁决（4F）

### 已有 TODO 位
- `~/.openclaw/todo/master-execution-plan.md`
  - `4F.5` 基于 4E 数据，决定是否调整 L3 触发阈值（minScore/minResults）
  - `4F.6` 基于 4E 数据，决定是否需要 notebook 自动刷新机制
  - `4F.7` 基于 4E 数据，决定是否实现预计算缓存（方案 C）

### 路线图对应关系
- 本地版 Day 2（Strict Fallback v1） → **4F.5**
- 本地版 Day 4（4E 收口 + notebook 自动刷新判断） → **4F.6**
- 本地版 Day 6（缓存 / 预计算评估） → **4F.7**

### 当前结论
这三项**不需要新建 TODO**，观察期跑完后直接把结论灌回 `4F.5 ~ 4F.7` 即可。

---

# 二、路线图中“已有 reports 承接，但没有独立 TODO 编号”的部分

这些部分可以先靠 report 落地；如果后面反复做，再决定是否升级成独立 TODO。

## 1. 本地版 Day 1：补可观测性

### 现有承接位
- `reports/memory-retrieval-scorecard-YYYYMMDD.md`
- `reports/memory-retrieval-observation-20260314.md`

### 建议写入内容
- L3 触发理由
- L3 结果状态分类
- L3 耗时
- L3 是否新增有效信息

### 当前缺口
- `master-execution-plan.md` 里**没有单独的“观测字段补强”编号**

### 建议
先在 reports 中落地；如果做完后发现值得固化，再补一个：
- `4F.4A` 观测字段补强（可选）

---

## 2. 本地版 Day 3：Added Value Rubric

### 现有承接位
- `reports/memory-retrieval-observation-20260314.md`
- 可新增轻量文档：`reports/layer3-added-value-rubric-20260320.md`

### 当前缺口
- TODO 中**没有显式的“L3 A/B/C 价值分类”任务位**

### 建议
先作为 report 输出；如果 Day 6 / Day 7 还在持续引用，再升级成 `4F` 子项。

---

## 3. 本地版 Day 5：输出兼容策略

### 现有承接位
- 可新增报告：`reports/layer3-output-mode-policy-20260322.md`

### 当前缺口
- TODO 中**没有“legacy-compatible / layered-readable 输出策略”专门任务**

### 建议
先以 policy report 形式存在；如果后续真进入实现，再补成 TODO 子项。

---

## 4. 本地版 Day 7：Local Layer 3 Policy v1

### 现有承接位
- 可新增报告：`reports/local-layer3-policy-v1-20260324.md`
- `reports/memory-retrieval-observation-20260314.md` 可写阶段总结

### 当前缺口
- TODO 中**没有单独“冻结本地 v1 策略”编号**

### 建议
当前不急着新建 TODO；先让 4E + 4F 跑出数据，再把 v1 policy 作为报告定稿。

---

# 三、上游版路线图如何落到现有体系

## 1. PR #227 小修线

### 现有承接位
- 不是 TODO 主线任务，但已在日常 PR 跟进中推进
- 相关状态检查 cron：`check-memory-lancedb-pr-status`

### 对应关系
- 上游版 Day 2（继续只推进 PR #227） → **直接沿用现有 PR 跟进节奏**

### 建议
不必单独加新 TODO，除非 reviewer 再提一轮需要拆明确 action items。

---

## 2. PR-A（CLI runner hardening）

### 现有 TODO 位
- `master-execution-plan.md` 里**没有直接对应项**

### 最近邻承接位
- `4F.1 ~ 4F.4` 仍偏本地 fallback 实现细节
- 不适合硬塞进去

### 建议落点
如果要正式推进，建议新增一个小节，例如：
- `4H. Upstream hardening（新增）`
  - `4H.1` CLI runner hardening scope 定义
  - `4H.2` 本地验证
  - `4H.3` 提交 PR-A

当前阶段先不用马上加，等 PR #227 这轮 reviewer 定调后再补。

---

## 3. PR-B（strict fallback, contract-safe）

### 现有 TODO 位
- 与 `4F.5` 最接近，但 **4F.5 是本地基于观察期做阈值决策**，不是上游 PR 设计任务

### 建议落点
同样建议未来归到：
- `4H.4` strict fallback 方案草案
- `4H.5` 新工具 vs behind flag 决策
- `4H.6` 提交 PR-B / issue 草案

### 当前结论
现在先**不要急着补 TODO**。先把本地 4E / 4F 跑出证据，再决定上游方案究竟是：
- 新工具
- behind flag
- 还是只保留 hardening

---

# 四、路线图逐日 → 现有任务系统的精确映射

| 路线图项 | 优先落点 | cron | reports | 说明 |
|---|---|---|---|---|
| 本地 Day 1（可观测性） | 4E.4 当日执行 + report 承接 | `memory-observation-day4-20260318` | `scorecard-20260318` + observation | 先不单独建 TODO |
| 本地 Day 2（Strict Fallback v1） | `4F.5` 预判输入 | `memory-observation-day5-20260319` | `scorecard-20260319` + observation | 观察后形成阈值决策 |
| 本地 Day 3（Added Value Rubric） | report 承接 | `memory-observation-day6-20260320` | `scorecard-20260320` + observation | 暂无独立 TODO 位 |
| 本地 Day 4（4E 收口） | `4E.7` + `4F.5/4F.6` 输入 | `memory-observation-day7-20260321` | `scorecard-20260321` + observation summary | 正式阶段结论 |
| 本地 Day 5（输出兼容） | policy report | `memory-optimization-daily-20260322` | `scorecard-20260322` + policy draft | 暂无独立 TODO 位 |
| 本地 Day 6（缓存评估） | `4F.7` | `memory-optimization-daily-20260323` | `scorecard-20260323` + observation | 方案 C go/no-go |
| 本地 Day 7（冻结 v1） | policy report | `memory-optimization-daily-20260324` | `scorecard-20260324` + policy v1 | 先报告后决定是否补 TODO |
| 上游 Day 1（放弃 PR #206 路线） | roadmap/report | 无 | `layer3-dual-track-roadmap-20260317.md` | 已完成文档化 |
| 上游 Day 2（继续 PR #227） | 现有 PR 跟进 | `check-memory-lancedb-pr-status` | 无固定 report | 已有机制 |
| 上游 Day 3（PR-A） | 建议未来新增 `4H` | 无 | 未来可出 proposal report | 目前缺正式 TODO 位 |
| 上游 Day 4（PR-B） | 建议未来新增 `4H` | 无 | 未来可出 proposal report | 目前缺正式 TODO 位 |
| 上游 Day 5（新工具 vs flag） | 建议未来新增 `4H` | 无 | decision memo | 目前缺正式 TODO 位 |
| 上游 Day 6（evidence pack） | report 承接 | 无 | evidence list | 先不强行入 TODO |
| 上游 Day 7（两步走计划） | report 承接 | 无 | roadmap update | 先不强行入 TODO |

---

# 五、现在就能直接执行的最小落地原则

## 已经自动化的
- `4E.4 ~ 4E.7`
- `9.1 / 9.2 / 9.3` 的每日验证
- scorecard / observation 的持续产出

## 观察期结束后直接回填的
- `4F.5`
- `4F.6`
- `4F.7`

## 先写 report，不急着建 TODO 的
- Added Value Rubric
- 输出兼容策略
- Local Layer 3 Policy v1
- 上游 PR-A / PR-B proposal

## 真要补 TODO，也建议只补一组新编号
未来若要正式纳入，建议统一新建：
- `4H. Upstream hardening & compatibility`

而不是把上游工作零散塞进 `4F` 或其它本地观察项里。

---

# 六、当前推荐动作顺序

1. **先按 02:30 的 cron 跑完 4E / 9.1-9.3**
2. **让 4E 结果喂给 4F.5 / 4F.6 / 4F.7**
3. **本地版缺口先用 report 承接，不急着继续扩 TODO**
4. **上游版等 PR #227 / reviewer 信号更清楚后，再考虑新增 4H**

---

## 结论

现在这张路线图里：
- **本地线**已经有成熟的 TODO + cron + reports 承接骨架
- **上游线**目前更适合先用 roadmap/report 驱动，而不是立刻扩成新的大 TODO 树

也就是说，**这周真正要跑起来的主链路已经落好了**；缺的不是执行骨架，而是少数“策略型输出”的正式命名与归档。