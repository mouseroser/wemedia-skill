# HEARTBEAT.md - 守夜人（control-plane）健康检查

## 原则

- 先判层，再报警。不要把所有红灯都报成"记忆系统坏了"。
- heartbeat 是值班清单，不是长篇说明文。
- 夜间（23:00-08:00）只报告真正需要处理的问题；能静默就静默。
- 如果所有检查都正常，回复 `HEARTBEAT_OK`。
- 结果推送到控制面群（-5281895495）；只有需要人工介入的才同时推监控群（-5131273722）。

## 1. 浏览器

检查：
```bash
openclaw browser status
```
如果 `running: false`：
```bash
openclaw browser start
```

## 2. Rerank sidecar

检查：
```bash
curl -s http://127.0.0.1:8765/health
```
如果无响应：
```bash
launchctl list | grep rerank
```

判定：
- rerank 异常但 `memory_stats` / `memory_list` 正常 → **重排退化**
- 不要误报成"记忆系统全坏"

## 3. Layer 1 — 文件层

检查：
```bash
[ -d ~/.openclaw/workspace/memory ]
[ -r ~/.openclaw/workspace/memory/$(date +%F).md ]
[ -r ~/.openclaw/workspace/MEMORY.md ]
```

判定：
- 缺目录 / 缺文件 / 权限异常 → **文件层问题**

## 4. Layer 2 — 检索层

用工具检查：
- `memory_stats`
- `memory_list`
- 必要时抽样 1 条 `memory_recall`

判定：
- 这些失败才叫 **memory-lancedb / recall 链路问题**
- 不要和 cron / rerank / delivery 混报

## 5. OpenClaw 守护脚本

运行：
```bash
bash ~/.openclaw/scripts/post-upgrade-guard.sh
```

判定：
- `RESULT=ok` → 正常
- `RESULT=auto_fixed` / `RESULT=version_changed` → 报告修复内容
- 分支异常 → 需要人工检查

硬规则：
- 绝不要把 runtime plugin load path 指回 PR / 开发树
- PR 分支只能在独立 worktree 切换

## 6. Cron 健康

检查：
```bash
openclaw cron list
```

重点关注：
- `post-upgrade-guard`
- `layer2-health-check`
- `memory-quality-audit`
- `openclaw-runtime-audit`
- `layer1-compress-check`

判定：
- `timeout` / `network connection error` / delivery 报错 → **执行链路问题**
- 不要直接报成 memory failure
- 只有 `lastRunAtMs > 26h` 才算超时未运行

## 7. 自媒体运营链路

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

## 输出格式

有问题时：
```text
⚠️ <问题类型>
- 定性：<文件层 / recall 链路 / 重排退化 / 执行链路>
- 影响：<简述>
- 是否需要人工介入：<是/否>
```

如果所有检查都正常：
```text
HEARTBEAT_OK
```
