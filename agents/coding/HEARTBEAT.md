# HEARTBEAT.md - Coding Agent 健康检查

## 健康检查（每次心跳时运行）

### 工作目录状态
检查当前是否有未完成的任务：
```bash
git status
```
如果有未提交的代码变更，检查是否是中断的任务。

### 依赖完整性
检查关键依赖是否可用：
```bash
# 检查 Node.js
node --version

# 检查 Python（如果项目需要）
python3 --version

# 检查包管理器
npm --version || yarn --version
```

### 测试环境
确保测试工具可用：
```bash
# 检查测试框架（根据项目调整）
npm test --version 2>/dev/null || echo "测试环境需要检查"
```

### 故障恢复
如果发现中断的任务：
1. 检查最后的 commit 消息
2. 读取 `memory/YYYY-MM-DD.md` 确认上下文
3. 推送状态到代码编程群（-5039283416）+ 监控群（-5131273722）
4. 等待 main 指令

---

**原则**:
- 不要自己决定是否继续中断的任务
- 发现问题立即报告，不要尝试自动修复
- 保持工作目录干净，完成的任务及时提交
