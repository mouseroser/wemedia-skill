# memory/ - 记忆目录结构

## 目录组织

```
memory/
├── chenxing/           # 晨星的私人笔记（仅 main session 可见）
│   └── [private notes]
├── shared/             # 跨 agent 共享上下文
│   └── [shared notes]
└── YYYY-MM-DD.md       # 每日操作日志（main agent）
```

## 使用规范

### 每日日志（根目录）
- `memory/YYYY-MM-DD.md` - main agent（小光）的每日操作日志
- 记录当天发生的事情、决策、问题、解决方案
- 只保留今天和昨天的日志在上下文中
- 每周回顾：提取重要内容到 MEMORY.md，归档旧日志

### 私人笔记（chenxing/）
- 晨星的个人想法、计划、敏感信息
- **仅在 main session 可见**，不在群聊或 sub-agent 中加载
- 用于存储不应该泄露给其他人的内容

### 共享上下文（shared/）
- 跨 agent 可见的笔记和参考资料
- 项目相关的背景知识、决策记录
- 不包含敏感信息

### Agent 专属日志
- 每个 agent 的日志在 `agents/<agent-name>/memory/YYYY-MM-DD.md`
- 例如：`agents/coding/memory/2026-03-05.md`
- Agent 只写自己的日志，不修改其他 agent 的日志

## 记忆压缩

**警告：** 日志会快速膨胀。Kelly 的日志曾达到 161k tokens → 输出质量急剧下降。

**维护规则：**
1. 每周回顾一次（周日晚上）
2. 提取重要内容到 `MEMORY.md`
3. 压缩或归档超过 40k tokens 的日志
4. 删除不再需要的旧日志

**原则：**
- 每日日志 = 原材料
- MEMORY.md = 精炼产品
- 两者缺一不可，但要定期维护

---

_记忆即文件。脑子里的东西会消失，文件不会。_
