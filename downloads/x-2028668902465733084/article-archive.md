# OpenClaw养成记，从0开始！（归档版）

- 作者：Berryxia.AI (@berryxia)
- 原帖：https://x.com/berryxia/status/2028668902465733084
- 整理时间：2026-03-26 21:42 CST

## 内容定位

这是一篇把 Shubham Saboo 关于「如何让 OpenClaw Agents 随时间真正进化」的实践，整理翻译成中文并结合 OpenClaw 讲解的长文。

## 核心结论

- 智能体真正进化的不是模型，而是围绕它持续演化的 Markdown 文件体系
- 文件系统本身就是集成层
- 三层结构分别解决：身份、操作、自愈、知识沉淀
- 持续反馈 + 文件化纠错，比一次性 prompt 优化更重要

## 三层文件架构

```text
第一层：身份层
SOUL.md | IDENTITY.md | USER.md

第二层：操作层
AGENTS.md | HEARTBEAT.md | 角色专属指南

第三层：知识层
MEMORY.md | 每日日志 | shared-context/
```

## 关键内容摘要

### 1. 身份层
- `SOUL.md`：人格、职责、原则
- `IDENTITY.md`：快速参考卡
- `USER.md`：服务对象及其偏好

### 2. 操作层
- `AGENTS.md`：每次会话如何启动、读取哪些文件、如何管理记忆、安全边界是什么
- `HEARTBEAT.md`：监控浏览器、定时任务、自愈检查

### 3. 知识层
- `MEMORY.md`：精华长期记忆，重点记录血泪教训与错误示范
- 每日日志：原始操作记录
- `shared-context/`：跨智能体共享的世界观、反馈和信号层

### 4. 协作方式
- 不依赖复杂消息队列
- 文件系统就是协作总线
- 单写者原则：每个共享文件一个写者、多个读者

### 5. 演化方式
- 第一天和第 40 天模型可以是同一个
- 差异来自文件越来越丰富、具体、贴合个人需求
- 智能体进化靠长期反馈沉淀，不靠一次性 prompt 神技

## 参考代码片段

### AGENTS.md 启动规则
```text
1. 读取 SOUL.md
2. 读取 USER.md
3. 读取 memory/YYYY-MM-DD.md（今天 + 昨天）
4. 如果在主会话中：同时读取 MEMORY.md
```

### shared-context/
```text
shared-context/
├── THESIS.md
├── FEEDBACK-LOG.md
└── SIGNALS.md
```

### 基于文件的协作
```text
Dwight -> DAILY-INTEL.md -> Kelly / Rachel / Pam
```

## 图片编号对照

- 图1 → `01-HCbEGcbbIAAKeK2.jpg`
- 图2 → `02-HCa_7xebEAAJBLf.jpg`
- 图3 → `03-HCa_24eboAAJJva.jpg`
- 图4 → `04-HCa_w68bUAAfrKm.jpg`
- 图5 → `05-HCa__VaagAAeywK.jpg`
- 图6 → `06-HCbALLXb0AAgVjs.jpg`
- 图7 → `07-HCbAZ7nbcAAlug8.jpg`
- 图8 → `08-HCbAtB8aEAAkds3.jpg`
- 图9 → `09-HCbCJfebkAAnHx7.jpg`
- 图10 → `10-HCbCQDJbAAA8l3o.jpg`
- 图11 → `11-HCbC740aAAApIes.jpg`

## 参考链接

- 原始参考：Shubham Saboo《How to Build OpenClaw Agents That Actually Evolve Over Time》
- 来源：https://x.com/Saboo_Shubham_/status/2027463195150131572
- 整理翻译：https://berryxia.ai/
