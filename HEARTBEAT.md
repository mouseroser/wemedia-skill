# HEARTBEAT.md - 小光（main）健康检查

## 原则

- main 的 heartbeat 只关注**业务层**健康：自媒体运营链路 + TODO。
- 运行时健康（浏览器 / rerank / Layer 1-3 / cron / 守护脚本）已移交给 `control-plane`（守夜人）。
- 记忆系统分层判断以 `MEMORY-ARCHITECTURE.md` 为准：不要把执行链路问题误报成记忆系统故障。
- 如果所有检查都正常，回复 `HEARTBEAT_OK`。

## 1. 自媒体运营链路

### 今日信号
检查：
```bash
today=$(date +%F)
if [ -f ~/.openclaw/workspace/intel/media-ops/DAILY-SIGNAL-BRIEF.md ]; then
  grep -q "$today\|最后更新:" ~/.openclaw/workspace/intel/media-ops/DAILY-SIGNAL-BRIEF.md && echo SIGNAL_OK || echo SIGNAL_MISSING
else
  echo SIGNAL_MISSING
fi
```

时间感知：
- **07:30 前 signal 缺失不算故障**
- 07:30 后仍缺失，再报异常

### 今日计划
检查：
```bash
[ -f ~/.openclaw/workspace/intel/media-ops/DAILY-PUBLISH-PLAN.md ] && echo PLAN_OK || echo PLAN_MISSING
```

### 待确认积压
检查：
```bash
rg -n '待确认' ~/.openclaw/workspace/intel/media-ops/HOT-QUEUE.md
```

判定：
- 只有存在真实待确认积压时才提醒

## 2. TODO

先看：
```bash
rg -n '立即执行（今天）|本周执行|观察期' ~/.openclaw/todo/master-execution-plan.md
```

判定：
- 优先看 `master-execution-plan.md`
- 不要把历史完成区块、旧观察期说明、回顾快照误报为当前待办
- 只提醒**当前未完成且需要行动**的项目

## 输出格式

有问题时，按下面格式简洁汇报：
```text
⚠️ <问题类型>
- 影响：<简述>
- 是否需要晨星介入：<是/否>
```

如果所有检查都正常：
```text
HEARTBEAT_OK
```
