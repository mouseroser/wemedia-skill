# 智能体目录结构规范

**创建时间**: 2026-03-06
**适用范围**: 所有子智能体

---

## 目录结构设计原则

每个智能体都有专属的工作目录，按照工作产物类型组织文件：

- **输入文件** - 从其他 agent 读取的文件
- **工作产物** - 自己生成的文件
- **归档文件** - 历史记录和备份

---

## 各智能体目录结构

### 1. Brainstorming (方案智囊)
```
~/.openclaw/workspace/agents/brainstorming/
├── specs/              # Spec-Kit 四件套
│   └── {feature}/
│       ├── spec.md     # WHAT/WHY
│       ├── plan.md     # 技术决策
│       ├── tasks.md    # 任务分解
│       └── research.md # 研究资料
├── reports/            # 修复方案、Epoch 决策
├── archives/           # 历史归档
└── *.md               # 配置文件
```

### 2. Coding (开发执行)
```
~/.openclaw/workspace/agents/coding/
├── code/              # 开发产物
├── patches/           # 修复补丁
├── logs/              # 冒烟测试日志
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 3. Review (交叉审查)
```
~/.openclaw/workspace/agents/review/
├── reviews/           # 审查报告
├── verdicts/          # Verdict JSON
├── reports/           # 分析报告
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 4. Test (测试执行)
```
~/.openclaw/workspace/agents/test/
├── test-results/      # 测试结果
├── logs/              # 测试日志
├── reports/           # 测试报告
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 5. Docs (文档生成)
```
~/.openclaw/workspace/agents/docs/
├── docs/              # 最终文档
├── drafts/            # 文档草稿
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 6. Gemini (织梦)
```
~/.openclaw/workspace/agents/gemini/
├── reports/           # 分析报告
│   ├── step-1.5-analysis.md
│   ├── step-5.5-diagnosis.md
│   ├── step-6-outline.md
│   ├── media-research.md
│   └── content-review.json
├── analysis/          # 深度分析
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 7. NotebookLM (珊瑚)
```
~/.openclaw/workspace/agents/notebooklm/
├── reports/           # 查询结果
│   ├── step-1.5-knowledge.md
│   ├── step-6-template.md
│   └── media-deep-research.md
├── artifacts/         # 衍生内容
│   ├── podcast.mp3
│   ├── mind-map.png
│   ├── quiz.json
│   └── infographic.png
├── queries/           # 查询历史
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 8. Wemedia (自媒体管家)
```
~/.openclaw/workspace/agents/wemedia/
├── drafts/            # 内容草稿
│   ├── draft.md
│   └── prompts.md
├── platforms/         # 各平台版本
│   ├── xiaohongshu.md
│   ├── douyin.md
│   └── zhihu.md
├── content-calendar/  # 内容排期
├── analytics/         # 数据分析
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 9. Monitor-bot (全局监控)
```
~/.openclaw/workspace/agents/monitor-bot/
├── alerts/            # 告警记录
├── logs/              # 监控日志
├── reports/           # 监控报告
├── archives/          # 历史归档
└── *.md              # 配置文件
```

### 10. Nano-banana (生图)
```
~/.openclaw/workspace/agents/nano-banana/
├── images/            # 生成的图片
├── prompts/           # 提示词记录
├── archives/          # 历史归档
└── *.md              # 配置文件
```

---

## Main Agent 目录结构

```
~/.openclaw/workspace/
├── reports/           # 验证报告、分析文档
├── scripts/           # 工具脚本
├── memory/            # 每日记忆
├── intel/             # Agent 协作文件（单写者原则）
│   ├── DAILY-INTEL.md
│   └── collaboration/ # 多 agent 共读的外部项目 / 本地镜像 / 共享分析材料
├── shared-context/    # 共享上下文
├── agents/            # 子智能体工作目录
└── *.md              # Main agent 配置文件
```

---

## 文件命名规范

### 时间戳格式
- 日期：`YYYY-MM-DD`
- 时间：`YYYY-MM-DD-HHMM`
- 示例：`2026-03-06-verification-report.md`

### 文件类型后缀
- 报告：`-report.md`
- 分析：`-analysis.md`
- 日志：`-log.txt`
- 配置：`.json` / `.yaml`
- 草稿：`-draft.md`

### 版本控制
- 使用时间戳作为版本标识
- 归档文件保留完整时间戳
- 当前工作文件使用简短名称

---

## 归档策略

### 自动归档
- 每周日凌晨 04:00 执行记忆压缩
- 30 天前的文件自动归档到 `archives/`

### 手动归档
- 流水线完成后，将工作产物归档
- 保留最近 3 次运行的完整记录
- 更早的记录压缩后归档

### 归档文件命名
```
archives/
├── 2026-03-06-step-3-review.json
├── 2026-03-05-step-5-test-results.txt
└── 2026-03-04-step-6-docs.md
```

---

## 多 Agent 联合工作材料

**规则**：只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`

- **正式产物**：报告、审查结论、修复代码、文档交付等 → 放各自 agent 目录
- **非正式产物**：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → 放 `intel/collaboration/`
- clone / 更新该共享仓库由一个 agent 负责，其他 agent 只读，仍然符合单写者原则
- 临时查看可先 clone 到 `/tmp/`，任务升级后统一转到 `intel/collaboration/`

## 协作文件读取路径

### Brainstorming 读取
- 织梦初稿：`~/.openclaw/workspace/agents/gemini/reports/step-1.5-analysis.md`
- 珊瑚知识：`~/.openclaw/workspace/agents/notebooklm/reports/step-1.5-knowledge.md`

### Coding 读取
- 任务分解：`~/.openclaw/workspace/agents/brainstorming/specs/{feature}/tasks.md`
- 修复方案：`~/.openclaw/workspace/agents/brainstorming/reports/fix-plan.json`

### Review 读取
- 代码产物：`~/.openclaw/workspace/agents/coding/code/`
- 需求规格：`~/.openclaw/workspace/agents/brainstorming/specs/{feature}/spec.md`

### Test 读取
- 代码产物：`~/.openclaw/workspace/agents/coding/code/`

### Docs 读取
- 织梦大纲：`~/.openclaw/workspace/agents/gemini/reports/step-6-outline.md`
- 代码产物：`~/.openclaw/workspace/agents/coding/code/`
- 审查摘要：`~/.openclaw/workspace/agents/review/reports/`
- 珊瑚模板：`~/.openclaw/workspace/agents/notebooklm/reports/step-6-template.md`

### Wemedia 读取
- 调研摘要：`~/.openclaw/workspace/agents/gemini/reports/media-research.md`
- 深度调研：`~/.openclaw/workspace/agents/notebooklm/reports/media-deep-research.md`

### Nano-banana 读取
- 配图提示词：`~/.openclaw/workspace/agents/wemedia/drafts/prompts.md`

---

## 更新记录

- 2026-03-06: 创建标准目录结构，为所有智能体建立专属文件夹
