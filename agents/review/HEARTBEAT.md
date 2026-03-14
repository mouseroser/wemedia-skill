# HEARTBEAT.md - Review Agent 健康检查

## 健康检查（每次心跳时运行）

### 待审查任务
检查是否有未完成的审查任务：
```bash
# 读取最近的 memory 日志
tail -n 50 memory/$(date +%Y-%m-%d).md
```

### 审查历史
检查最近的审查记录：
```bash
# 检查工作目录
ls -la ~/workspace/agents/review/
```

### 模型可用性
检查常用审查模型是否可用：
```bash
# 检查 OpenClaw 状态
openclaw status
```

### 故障恢复
如果发现中断的审查任务：
1. 读取 `memory/YYYY-MM-DD.md` 确认上下文
2. 检查是哪个阶段中断（主审/预审/复核/仲裁）
3. 推送状态到交叉审核群（-5242448266）+ 监控群（-5131273722）
4. 等待 main 指令

---

**原则**:
- 不要自己决定是否继续中断的审查
- 只执行 main 分配的审查任务，不 spawn 其他 agent
- 保持审查标准一致，不要因为时间压力降低要求
