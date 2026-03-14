# HEARTBEAT.md - Claude Agent (小克) 健康检查

## 健康检查（每次心跳时运行）

### API 可用性
检查 Claude API 是否可用：
```bash
# 检查 OpenClaw 配置
openclaw status | grep -i claude
```

### 待设计任务
检查是否有未完成的方案设计任务：
```bash
# 读取最近的 memory 日志
tail -n 50 memory/$(date +%Y-%m-%d).md
```

### 方案历史回顾
定期回顾之前的方案是否有效：
```bash
# 检查工作目录
ls -la ~/workspace/agents/claude/
```

### 故障恢复
如果发现中断的设计任务：
1. 读取 `memory/YYYY-MM-DD.md` 确认上下文
2. 检查是哪个阶段中断（背景分析/方案设计/风险评估）
3. 推送状态到小克群（-5101947063）+ 监控群（-5131273722）
4. 等待 main 指令

---

**原则**:
- 不要自己决定是否继续中断的设计
- 方案必须基于问题宪法，不能偏离
- 从历史方案中学习，避免重复同样的问题
