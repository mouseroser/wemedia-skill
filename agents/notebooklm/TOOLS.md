# TOOLS.md - NotebookLM Agent

## nlm-gateway.sh 工具

### 查询 notebook
```bash
~/.openclaw/skills/notebooklm/scripts/nlm-gateway.sh query \
  --agent notebooklm \
  --notebook openclaw-docs \
  --query "问题"
```

### 生成衍生内容
```bash
~/.openclaw/skills/notebooklm/scripts/nlm-gateway.sh artifact \
  --agent notebooklm \
  --notebook media-research \
  --type podcast \
  --output artifacts/podcast.mp3
```

## Notebooks
- **openclaw-docs**: OpenClaw 文档知识库（50源，满载）
- **media-research**: 自媒体调研知识库（3源）
- **memory**: 记忆知识库（5源，待迁移）

## 衍生内容类型
- **podcast**: 音频播客（深度长文 >2000字）
- **mind-map**: 思维导图（知识类内容）
- **quiz/flashcards**: 问答卡片（教程类内容）
- **infographic**: 信息图（数据类内容）

## 智能推荐逻辑
分析内容特征，推荐最适合的衍生类型：
- 深度长文 → podcast
- 知识类 → mind-map
- 教程类 → quiz/flashcards
- 数据类 → infographic

## 工作目录
- 查询结果：`~/.openclaw/workspace/agents/notebooklm/reports/`
- 衍生内容：`~/.openclaw/workspace/agents/notebooklm/artifacts/`

## 代理配置
- Surge 代理：127.0.0.1:8234
- 必须切换到美国节点（香港不行）
- 增强模式默认开启

---
