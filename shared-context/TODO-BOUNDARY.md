# TODO Boundary

## 一句话结论
`todo` 更适合定位为 **全局编排控制面（control plane）**，而不是“系统级任务本体”。

---

## 三层边界

### 1. `~/.openclaw/todo/master-execution-plan.md`
**角色**：全局当前执行态的 canonical。

它负责：
- 全局优先级（P0 / P1 / P2 / P3）
- 当前活跃任务队列
- 里程碑
- 跨文件阻塞 / 依赖
- autopilot 的主要入口

它**不应该**负责：
- 承载所有任务的完整背景
- 取代每个源 todo 文件的任务语义
- 变成唯一永久真相源

---

### 2. `~/.openclaw/todo/*.md` 源 todo 文件
**角色**：任务语义和细节的 canonical。

它们负责：
- 原始任务定义
- 背景 / 证据 / 约束
- 子步骤
- 完成标准
- 领域上下文

它们**不应该**负责：
- 全局优先级排序
- 跨文件调度
- 全局当前执行态总览

---

### 3. `workspace/reports/` / agent 产物 / repo 内文件
**角色**：执行证据层。

它们负责：
- 报告
- 产出物
- 实现结果
- 验证结果
- 运行日志

它们不是 todo，也不应该承担调度职能。

---

## Autopilot 边界
`todo-autopilot` 只应自动推进：
- 已进入 master 的活跃项
- 边界清晰的内部安全任务
- 可明确委派给单一 agent 的任务

`todo-autopilot` 不应自动推进：
- 只存在于源文件、但尚未进入 master 的局部 backlog
- 需要用户确认的动作
- 对外发送 / 发布 / 危险删除 / live runtime 变更

---

## 双向同步原则
双向同步不是“双主写”。

正确规则：
- **master** = 当前全局执行态 canonical
- **源 todo** = 任务语义 canonical

因此：
- 勾选完成 → 两边都更新
- 进度推进 → 两边都补简短说明
- 优先级 / 截止日期调整 → 先改 master，再同轮回写源文件
- 语义冲突 → 不强行覆盖，显式标注冲突 / BLOCKED

---

## 目录位置判断
### 当前目录：`~/.openclaw/todo/`
**结论：合适。**

理由：
1. 它是 **全局控制面**，不是某个 workspace repo 的局部 backlog。
2. 放在 `~/.openclaw/` 下，和 `skills/`、`scripts/`、`state/` 属于同一级的用户级控制目录，语义一致。
3. 放在 workspace 外，可以避免把全局执行计划误当成某个 repo 的项目文件。
4. 现有约定已经一致：`PATHS.md`、`FEEDBACK-LOG.md`、`HEARTBEAT.md`、autopilot / daily-check 都已按这个位置运行。

### 不建议的位置：`~/.openclaw/workspace/todo/`
不建议，原因：
- 容易和项目文件混淆
- 容易被当成 workspace repo 的普通文档一起 commit
- 会削弱它“跨项目 / 跨 agent 的全局控制面”身份

---

## 适用范围
适合进入 `~/.openclaw/todo/` 的任务：
- 影响全局优先级判断
- 需要跨 agent 协调
- 需要 autopilot / cron / main 收口
- 会改变“现在该做什么”

更适合留在项目内 / repo 内 / issue tracker 的任务：
- 纯局部 backlog
- 完成标准高度依赖 repo 语义
- 不影响全局排程
- 只是某个大任务内部的细碎子步骤

---

## 当前判定（2026-03-17）
- 保持 `~/.openclaw/todo/` 不变
- 继续把它当作 **global active queue / control plane**
- 不把它升级成“everything plane”
- autopilot 只推进进入 master 的活跃项，不直接扫全部局部 backlog 乱动
