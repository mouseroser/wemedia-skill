# HEARTBEAT.md - OpenAI Agent (小曼) 健康检查

## 健康检查（每次心跳时运行）

### API 可用性
检查 OpenAI API 是否可用：
```bash
# 检查 OpenClaw 配置
openclaw status | grep -i openai
```

### 待处理任务
检查是否有未完成的宪法/仲裁任务：
```bash
# 读取最近的 memory 日志
tail -n 50 memory/$(date +%Y-%m-%d).md
```

### 仲裁历史回顾
定期回顾之前的仲裁决策是否合理：
```bash
# 检查工作目录
ls -la ~/workspace/agents/openai/
```

### 故障恢复
如果发现中断的任务：
1. 读取 `memory/YYYY-MM-DD.md` 确认上下文
2. 检查是哪个阶段中断（宪法制定/风险分析/仲裁决策）
3. 推送状态到小曼群（-5242027093）+ 监控群（-5131273722）
4. 等待 main 或 review 指令

---

**原则**:
- 不要自己决定是否继续中断的任务
- 仲裁时必须保持独立性，不能是之前参与过的 agent
- 从历史仲裁中学习，提升决策质量
