# OpenClaw 目录约定

**版本**: 2.0  
**生效日期**: 2026-03-13  
**适用范围**: 所有 OpenClaw agent

**主要变更（v2.0）**：
- 脚本按 Skill 分类，放在各自 skill 目录下
- Skills 分为项目特定和通用工具两类
- 采用高内聚原则，便于发布和维护

---

## 🎯 核心原则

**系统级 vs 工作区级**：
- **系统级**（`~/.openclaw/`）：全局共享，不绑定项目
- **工作区级**（`~/.openclaw/workspace/`）：项目相关，可以有多个 workspace

---

## 📁 目录约定

### 1. Skills 目录

#### 项目特定 Skills

**位置**: `~/.openclaw/skills/`

**约定**:
- ✅ **你自己创建的 skills**
- ✅ **你的流水线 skills**（starchain, stareval, wemedia）
- ✅ **你的项目集成 skills**（notebooklm）
- ❌ 不要放第三方或通用工具 skills

**原因**:
- 这些是你的项目特定代码
- 需要版本控制和发布到 GitHub
- 与通用工具区分开

**示例**:
```
~/.openclaw/skills/
├── agent-config-generator/
├── memory-architecture-manager/
├── architecture-generator/
├── notebooklm/
├── starchain/
├── stareval/
└── wemedia/
```

#### 通用工具 Skills

**位置**: `~/.openclaw/workspace/skills/`

**约定**:
- ✅ **第三方 skills**（tavily-search, weather）
- ✅ **通用框架 skills**（proactive-agent, self-improving-agent）
- ✅ **可复用工具 skills**（agent-browser, find-skills, skill-vetter）
- ❌ 不要放项目特定的 skills

**原因**:
- 这些是通用工具，不是你的项目代码
- 可能来自 ClawHub 或其他来源
- 不需要发布到你的 GitHub

**示例**:
```
~/.openclaw/workspace/skills/
├── agent-browser/
├── find-skills/
├── proactive-agent/
├── self-improving-agent/
├── skill-vetter/
├── tavily-search/
└── weather/
```

---

### 2. Scripts 目录

**位置**: 在各自的 skill 目录下

**约定**：
- ✅ **脚本应该放在对应的 skill 目录下**
- ✅ 例如：`~/.openclaw/skills/memory-architecture-manager/scripts/`
- ✅ 保持高内聚：脚本和 skill 在一起
- ❌ 不要在 `~/.openclaw/scripts/` 创建 skill 相关脚本

**原因**：
- 高内聚原则：脚本是 skill 的一部分，应该在一起
- 便于发布：打包 skill 时自动包含脚本
- 便于维护：修改 skill 时所有文件都在同一目录
- 便于删除：删除 skill 时一起删除

**示例**：
```
~/.openclaw/skills/
├── memory-architecture-manager/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── layer2-health-check.sh
│   │   ├── layer1-compress-check.sh
│   │   ├── layer3-monthly-archive.sh
│   │   └── layer3-deep-insights.sh
│   └── references/
├── notebooklm/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── sync-memory-to-notebooklm.sh
│   └── references/
└── todo-manager/
    ├── SKILL.md
    ├── scripts/
    │   └── todo-daily-check.sh
    └── references/
```

**通用系统脚本**（如果有）：
- 如果有真正通用的系统脚本（不属于任何 skill），可以放在 `~/.openclaw/scripts/`
- 但大多数脚本应该属于某个 skill

---

### 3. Todo 目录

**位置**: `~/.openclaw/todo/`

**约定**:
- ✅ **所有待办任务都应该在 `~/.openclaw/todo/`**
- ✅ 系统级任务管理，不绑定项目
- ❌ 不要在 `~/.openclaw/workspace/` 根目录或子目录创建 todo 文件

**原因**:
- Todo 是系统级任务管理
- 应该全局可见，不绑定到具体项目
- 便于 Cron 任务扫描

**示例**:
```
~/.openclaw/todo/
├── todo-2026-03-12.md
├── todo-2026-03-13.md
└── ...
```

---

### 4. Workspace 目录

**位置**: `~/.openclaw/workspace/`

**约定**:
- ✅ **只放项目相关的文件**
- ✅ 包括：SOUL.md, AGENTS.md, MEMORY.md, memory/, shared-context/, intel/, agents/
- ❌ 不要放 skills, scripts, todo

**原因**:
- Workspace 是项目工作区
- 可以有多个 workspace
- 保持清晰的职责边界

**示例**:
```
~/.openclaw/workspace/
├── SOUL.md
├── AGENTS.md
├── MEMORY.md
├── memory/
├── shared-context/
├── intel/
└── agents/
```

---

## 🚫 禁止的目录结构

### ❌ 错误示例 1: 通用工具 skills 在项目 skills 目录
```
~/.openclaw/skills/tavily-search/    # ❌ 错误，应该在 workspace/skills/
~/.openclaw/skills/weather/          # ❌ 错误，应该在 workspace/skills/
```

### ❌ 错误示例 2: 项目 skills 在 workspace 下
```
~/.openclaw/workspace/skills/starchain/    # ❌ 错误，应该在 ~/.openclaw/skills/
```

### ❌ 错误示例 3: Todo 在 workspace 下
```
~/.openclaw/workspace/todo/      # ❌ 错误
└── todo.md
```

### ❌ 错误示例 4: Skill 脚本在系统 scripts 目录
```
~/.openclaw/scripts/layer2-health-check.sh    # ❌ 错误，应该在 skill 目录下
```

---

## ✅ 正确的目录结构

```
~/.openclaw/
├── skills/              # 项目特定 skills ✅
│   ├── agent-config-generator/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── memory-architecture-manager/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── layer2-health-check.sh
│   │   │   ├── layer1-compress-check.sh
│   │   │   ├── layer3-monthly-archive.sh
│   │   │   └── layer3-deep-insights.sh
│   │   └── references/
│   ├── notebooklm/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── sync-memory-to-notebooklm.sh
│   │   └── references/
│   ├── starchain/
│   ├── stareval/
│   └── wemedia/
├── scripts/             # 通用系统脚本（如果有）✅
│   └── ...
├── todo/                # 所有待办任务 ✅
│   └── todo-2026-03-13.md
└── workspace/           # 项目工作区 ✅
    ├── skills/          # 通用工具 skills ✅
    │   ├── tavily-search/
    │   ├── weather/
    │   ├── proactive-agent/
    │   └── ...
    ├── SOUL.md
    ├── AGENTS.md
    ├── MEMORY.md
    ├── memory/
    ├── shared-context/
    ├── intel/
    └── agents/
```

---

## 📝 创建新内容时的检查清单

### 创建新 Skill
- [ ] 确认是项目特定还是通用工具
- [ ] 项目特定 → `~/.openclaw/skills/`
- [ ] 通用工具 → `~/.openclaw/workspace/skills/`

### 创建新脚本
- [ ] 确认脚本属于哪个 skill
- [ ] 放在对应 skill 的 `scripts/` 目录下
- [ ] 例如：`~/.openclaw/skills/memory-architecture-manager/scripts/`
- [ ] 如果是真正通用的系统脚本，才放在 `~/.openclaw/scripts/`

### 创建待办任务
- [ ] 确认放在 `~/.openclaw/todo/`
- [ ] 不要放在 workspace 下

### 更新 Cron 任务
- [ ] 使用完整的 skill 脚本路径
- [ ] 例如：`~/.openclaw/skills/memory-architecture-manager/scripts/layer2-health-check.sh`

---

## 🔄 迁移指南

如果发现文件在错误的位置：

### 迁移 Skills
```bash
# 项目特定 skills → ~/.openclaw/skills/
mv ~/.openclaw/workspace/skills/my-project-skill ~/.openclaw/skills/

# 通用工具 skills → ~/.openclaw/workspace/skills/
mv ~/.openclaw/skills/tavily-search ~/.openclaw/workspace/skills/
```

### 迁移 Scripts
```bash
# Skill 脚本 → skill 目录下
mkdir -p ~/.openclaw/skills/my-skill/scripts
mv ~/.openclaw/scripts/my-skill-script.sh ~/.openclaw/skills/my-skill/scripts/

# 记得更新 Cron 任务中的路径！
```

### 迁移 Todo
```bash
mv ~/.openclaw/workspace/todo/* ~/.openclaw/todo/
rmdir ~/.openclaw/workspace/todo
```

### 更新 Cron 路径
```bash
# 备份
cp ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.backup

# 批量替换路径
sed -i '' 's|~/.openclaw/scripts/my-script.sh|~/.openclaw/skills/my-skill/scripts/my-script.sh|g' ~/.openclaw/cron/jobs.json
```

---

## 📚 相关文档

- `MEMORY.md` - 错误示范和教训
- `shared-context/FEEDBACK-LOG.md` - 跨 agent 纠正
- `skills/architecture-generator/references/architecture-spec.md` - 架构规范

---

**维护者**: main (小光)  
**最后更新**: 2026-03-13  
**版本**: 2.0  
**状态**: ✅ 生效

**变更历史**：
- v2.0 (2026-03-13): 脚本按 Skill 分类，采用高内聚原则
- v1.0 (2026-03-12): 初始版本，建立基本目录约定
