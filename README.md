# workspace/ - OpenClaw 工作区结构

## 目录结构

```
workspace/
├── SOUL.md                    # 小光（主 agent）的人格定义
├── IDENTITY.md                # 小光的快速参考卡
├── AGENTS.md                  # 根级行为规则（所有 agent 继承）
├── USER.md                    # 关于晨星（所有 agent 共享）
├── MEMORY.md                  # 小光的长期记忆（仅 main session）
├── HEARTBEAT.md               # 自愈检查清单
├── TOOLS.md                   # 工具配置和偏好
├── BOOTSTRAP.md               # 首次启动指南
│
├── shared-context/            # 跨 agent 知识层
│   ├── THESIS.md              # 当前世界观和工作重点
│   ├── FEEDBACK-LOG.md        # 跨 agent 纠错日志
│   └── SIGNALS.md             # 追踪的趋势和灵感
│
├── intel/                     # Agent 间信息共享（单写者原则）
│   └── README.md              # 协作规范说明
│
├── agents/                    # Agent 专属工作区
│   ├── README.md              # Agent 组织说明
│   ├── coding/                # 代码编程 agent
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── memory/
│   ├── review/                # 交叉审核 agent
│   ├── test/                  # 代码测试 agent
│   ├── brainstorming/         # 头脑风暴 agent
│   ├── docs/                  # 项目文档 agent
│   ├── gemini/                # 织梦 agent
│   ├── notebooklm/            # 珊瑚（知识检索）agent
│   ├── wemedia/               # 自媒体管家 agent
│   ├── nano-banana/           # 生图 agent
│   └── monitor-bot/           # 监控告警 agent
│
├── memory/                    # 记忆目录
│   ├── README.md              # 记忆组织说明
│   ├── chenxing/              # 晨星的私人笔记（仅 main session）
│   ├── shared/                # 跨 agent 共享上下文
│   └── YYYY-MM-DD.md          # 每日操作日志（main agent）
│
├── skills/                    # 技能工具目录
│
├── .archive/                  # 归档目录（不活跃的文件）
│   ├── README.md
│   ├── tmp-images/
│   └── agent-teams-openclaw/
│
└── [project files]            # 项目相关文件
    ├── pipeline-v1.8.md
    ├── starchain-flowchart.md
    ├── notebooklm-py-analysis.md
    ├── fetch-docs-site.sh
    └── import-docs-to-nlm.sh
```

## 三层架构

### 第一层：身份层
定义"这是谁？为谁服务？"
- `SOUL.md` - 人格定义
- `IDENTITY.md` - 快速参考卡
- `USER.md` - 服务对象信息

### 第二层：操作层
定义"如何工作？如何自愈？"
- `AGENTS.md` - 行为规则和会话启动流程
- `HEARTBEAT.md` - 自愈检查清单
- `agents/*/` - Agent 专属指南

### 第三层：知识层
定义"学到了什么？"
- `MEMORY.md` - 长期记忆（精炼产品）
- `memory/YYYY-MM-DD.md` - 每日日志（原材料）
- `shared-context/` - 跨 agent 知识共享
- `intel/` - Agent 协作文件

## 设计原则

1. **文件系统即集成层** - 不需要消息队列或数据库
2. **单写者原则** - 每个共享文件只有一个写者，多个读者
3. **调度保证协作** - 依赖关系通过执行顺序保证
4. **记忆即文件** - 脑子里的东西会消失，文件不会
5. **渐进式进化** - 让系统随使用自然生长，不要试图一次搭完

## 与 Shubham 架构的对应

| Shubham 的设计 | 我们的实现 | 说明 |
|---------------|-----------|------|
| Monica (主 agent) | 小光 (main) | 顶层编排中心 |
| Dwight (研究) | notebooklm (珊瑚) | 知识检索和情报 |
| Kelly (Twitter) | wemedia | 自媒体内容创作 |
| Rachel (LinkedIn) | wemedia | 多平台适配 |
| Pam (通讯) | monitor-bot | 监控和通知 |
| agents/ 子目录 | agents/ | Agent 专属工作区 |
| shared-context/ | shared-context/ | 跨 agent 知识层 |
| intel/ | intel/ | Agent 协作文件 |
| memory/shubham/ | memory/chenxing/ | 私人笔记 |
| memory/shared/ | memory/shared/ | 共享上下文 |

---

_这个结构会随着使用持续进化。第 1 天和第 40 天用的是同一个模型，区别在于这些不断变丰富的文件。_
