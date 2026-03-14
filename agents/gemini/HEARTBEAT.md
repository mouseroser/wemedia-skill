# HEARTBEAT.md - Gemini Agent (织梦) 健康检查

## 健康检查（每次心跳时运行）

### API 可用性
检查 Gemini API 是否可用：
```bash
# 检查 OpenClaw 配置
openclaw status | grep -i gemini
```

### 待处理任务
检查是否有未完成的扫描/复核任务：
```bash
# 读取最近的 memory 日志
tail -n 50 memory/$(date +%Y-%m-%d).md
```

### 复核历史
检查最近的复核记录，确保没有遗漏：
```bash
# 检查工作目录
ls -la ~/workspace/agents/gemini/
```

### 故障恢复
如果发现中断的任务：
1. 读取 `memory/YYYY-MM-DD.md` 确认上下文
2. 检查是哪个阶段中断（扫描/复核/诊断）
3. 推送状态到织梦群（-5264626153）+ 监控群（-5131273722）
4. 等待 main 或 review 指令

---

**原则**:
- 不要自己决定是否继续中断的任务
- API 限流或失败立即报告
- 保持快速响应，不要陷入细节分析
