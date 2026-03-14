# HEARTBEAT.md - Wemedia Agent (自媒体管家) 健康检查

## 健康检查（每次心跳时运行）

### 内容日历检查
检查是否有待发布的内容：
```bash
# 检查内容日历
ls -la ~/.openclaw/workspace-wemedia/content-calendar/ 2>/dev/null
```

### 平台账号状态
检查各平台账号是否正常：
```bash
# 检查平台配置
cat ~/.openclaw/workspace-wemedia/platforms/config.json 2>/dev/null
```

需要监控的平台：
- 小红书
- 抖音/TikTok
- 知乎

### 数据监控
检查最近发布内容的数据：
```bash
# 检查分析数据
ls -la ~/.openclaw/workspace-wemedia/analytics/ 2>/dev/null
```

### 故障恢复
如果发现问题：
1. **内容创作中断** → 读取 `memory/YYYY-MM-DD.md` 确认进度
2. **平台账号异常** → 推送告警到自媒体群（-5146160953）+ 监控群（-5131273722）
3. **待发布内容积压** → 检查是否等待晨星确认
4. **数据异常** → 分析原因，调整内容策略

---

**原则**:
- 绝不自动发布，必须等待晨星确认
- 平台规则变化要及时更新策略
- 数据反馈要定期回顾和优化
