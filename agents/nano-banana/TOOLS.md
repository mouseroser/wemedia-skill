# TOOLS.md - Nano Banana Agent

## 生图模型
- **模型**: gemini-3-pro-image-preview
- **能力**: 根据提示词生成图片
- **限制**: 不支持工具调用（exec/message 等）

## 输入格式
从 wemedia agent 读取配图提示词：
- `~/.openclaw/workspace/agents/wemedia/drafts/prompts.md`

## 输出格式
返回 markdown 格式的图片链接：
```markdown
![配图描述](https://example.com/image.png)
```

## 超时配置
- 生图模型响应慢，需要 `runTimeoutSeconds: 300`
- main agent spawn 时必须设置此参数

## 工作流程
1. 接收配图提示词
2. 生成图片
3. 返回图片 URL（markdown 链接）
4. main agent 下载图片到 wemedia workspace
5. main agent 发送图片到群

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。

## 多 Agent 联合工作材料
- 只要是多 agent 联合工作（流水线尤为明显），除了正式产物之外全部放到 `intel/collaboration/`
- 正式产物：报告、审查结论、修复代码、文档交付等 → 各自 agent 目录
- 非正式产物：外部 GitHub 项目、本地镜像、共享分析材料、临时脚本、调研素材等 → `intel/collaboration/`
