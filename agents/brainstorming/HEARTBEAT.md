# HEARTBEAT.md - Brainstorming Agent (灵感熔炉) 健康检查

## 健康检查（每次心跳时运行）

### 待分析任务
检查是否有未完成的根因分析任务：
```bash
# 读取最近的 memory 日志
tail -n 50 memory/$(date +%Y-%m-%d).md
```

### 历史方案回顾
定期回顾之前的方案是否有效：
```bash
# 检查工作目录
ls -la ~/workspace/agents/brainstorming/
```

### 知识库更新
检查是否有新的踩坑经验需要学习：
```bash
# 检查 shared-context
cat shared-context/FEEDBACK-LOG.md | tail -n 20
```

### 故障恢复
如果发现中断的分析任务：
1. 读取 `memory/YYYY-MM-DD.md` 确认上下文
2. 检查是哪个阶段中断（根因分析/方案设计/风险评估）
3. 推送状态到灵感熔炉群（-5231604684）+ 监控群（-5131273722）
4. 等待 main 或 review 指令

---

**原则**:
- 不要自己决定是否继续中断的分析
- 复杂场景（R3/TF-3/Step 5.5）必须用 opus/high
- 从历史失败中学习，避免重复同样的方案
