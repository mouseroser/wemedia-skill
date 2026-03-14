# HEARTBEAT.md - Monitor-Bot Agent (监控告警) 健康检查

## 健康检查（每次心跳时运行）

### 监控群连接状态
检查监控群是否可达：
```bash
# 检查 Telegram 连接
openclaw status | grep -i telegram
```

### 告警历史回顾
检查最近的告警记录：
```bash
# 读取最近的 memory 日志
tail -n 100 memory/$(date +%Y-%m-%d).md | grep -i "告警\|失败\|阻塞"
```

### 系统健康状态
定期汇总系统健康状态：
```bash
# 检查 OpenClaw 状态
openclaw status

# 检查 cron 任务
openclaw cron list
```

### 故障恢复
如果发现问题：
1. **监控群不可达** → 立即推送到晨星 DM (1099011886)
2. **告警积压** → 汇总后推送到监控群（-5131273722）
3. **系统异常** → 🔴 紧急告警，立即通知晨星

---

**原则**:
- 监控群必须始终可用
- 不要过滤告警，让晨星决定优先级
- 定期汇总系统健康状态（每天一次）
- 紧急问题立即通知，不要等待定期汇总
