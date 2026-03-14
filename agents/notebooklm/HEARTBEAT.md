# HEARTBEAT.md - NotebookLM Agent (珊瑚) 健康检查

## 健康检查（每次心跳时运行）

### NotebookLM 服务状态
检查 NotebookLM 是否可用：
```bash
# 检查 NotebookLM CLI
notebooklm --version 2>/dev/null || echo "NotebookLM CLI 需要检查"

# 检查认证状态
ls -la ~/.notebooklm/storage_state.json 2>/dev/null || echo "认证文件缺失"
```

### Notebook 健康检查
检查关键 notebook 是否可用：
```bash
# 检查 notebook 配置
cat ~/.openclaw/skills/notebooklm/config/notebooks.json 2>/dev/null
```

需要监控的 notebook：
- `memory` — 记忆系统
- `openclaw-docs` — OpenClaw 文档
- `media-research` — 自媒体调研

### 文档刷新任务
检查定时任务是否正常运行：
```bash
# 检查 cron 任务
openclaw cron list | grep -i notebooklm
```

### 故障恢复
如果发现问题：
1. **NotebookLM 不可用** → 降级到 web_search + web_fetch
2. **Notebook 被删除** → 立即更新 `config/notebooks.json`
3. **认证过期** → 推送告警到珊瑚群（-5202217379）+ 监控群（-5131273722）
4. **代理失败** → 检查 Surge 增强模式是否开启

---

**原则**:
- 工具失败不阻塞流水线，立即降级
- Notebook ID 变更必须同步更新配置
- 代理问题优先检查节点（美国、台湾）
