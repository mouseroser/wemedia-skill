# HEARTBEAT.md - Test Agent 健康检查

## 健康检查（每次心跳时运行）

### 测试环境状态
检查测试工具是否可用：
```bash
# 检查测试框架（根据项目调整）
npm test --version 2>/dev/null || echo "测试环境需要检查"

# 检查覆盖率工具
npx jest --version 2>/dev/null || echo "Jest 未安装"
```

### 测试数据完整性
检查测试数据和 fixtures 是否完整：
```bash
# 检查测试目录
ls -la tests/ 2>/dev/null || ls -la __tests__/ 2>/dev/null
```

### 待测试任务
检查是否有未完成的测试任务：
```bash
# 读取最近的 memory 日志
tail -n 50 memory/$(date +%Y-%m-%d).md
```

### 故障恢复
如果发现中断的测试任务：
1. 读取 `memory/YYYY-MM-DD.md` 确认上下文
2. 检查是哪个测试用例中断
3. 推送状态到代码测试群（-5245840611）+ 监控群（-5131273722）
4. 等待 review 或 main 指令

---

**原则**:
- 不要自己决定是否继续中断的测试
- 测试环境问题立即报告，不要尝试自动修复
- 保持测试标准一致，不要因为时间压力跳过测试
