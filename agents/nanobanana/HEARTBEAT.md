# HEARTBEAT.md - Nano-Banana Agent (生图) 健康检查

## 健康检查（每次心跳时运行）

### 生图模型状态
检查代理 Gemini 生图链路是否可用：
```bash
# 检查脚本帮助和配置
node ~/.openclaw/workspace/agents/nano-banana/proxy-generate-image.mjs --help
```

### 待处理任务
检查是否有未完成的生图任务：
```bash
# 读取最近的 memory 日志
tail -n 50 memory/$(date +%Y-%m-%d).md
```

### 生图历史
检查最近生成的图片质量：
```bash
# 检查工作目录
ls -la ~/workspace/agents/nano-banana/
```

### 故障恢复
如果发现问题：
1. **生图超时** → 检查是否设置了 300 秒超时
2. **模型不可用** → 推送告警到生图群（-5217509070）+ 监控群（-5131273722）
3. **图片质量问题** → 调整 prompt，重新生成
4. **API 限流** → 等待后重试

---

**原则**:
- 生图响应慢是正常的，必须设置足够的超时时间
- 真实生图由代理 `gemini-3.1-flash-image` 完成，返回后必须解码落盘
- 只返回本地路径，不负责对外发送
