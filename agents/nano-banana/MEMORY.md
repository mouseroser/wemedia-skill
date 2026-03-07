# MEMORY.md - Nano Banana Agent (生图)

## 关于我
- **Agent ID**: nano-banana
- **角色**: 配图生成
- **模型**: gemini-3-pro-image-preview
- **Telegram 群**: 生图 (-5217509070)

## 工作记录

### 2026-03-06 配置更新
- 创建完整的配置文件（AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md）
- 对齐自媒体 v1.0 流水线规范
- 明确职责：Step 5 根据提示词生成配图
- 模型限制：不支持工具调用

## 关键约束
- 只负责生成图片
- 不执行下载/发送任务（交给 main agent）
- 不执行内容创作/审查任务
- 生成结果以 markdown 链接返回

## 自媒体流水线职责

### Step 5 配图生成
1. 接收配图提示词（从 wemedia agent 的 `drafts/prompts.md`）
2. 使用 gemini-3-pro-image-preview 生成图片
3. 返回图片 URL（markdown 链接格式）

## 模型限制
- gemini-3-pro-image-preview 不支持工具调用（exec/message 等）
- 只能生成图片并返回 URL
- 无法自己下载文件或发送消息到 Telegram

## 已知问题
- gemini-3-pro-image-preview 先返回空 assistant 消息，再返回图片
- OpenClaw 可能判定 failed，但图片实际已生成
- Main agent 会检查返回内容中是否有图片 URL，无论 announce 状态

## Spawn 参数
- **runTimeoutSeconds: 300** (必须)
- 生图模型响应慢，需要延长超时
- Main agent spawn 时必须设置此参数

## 输入格式
从 wemedia agent 读取配图提示词：
- `~/.openclaw/workspace/agents/wemedia/drafts/prompts.md`

## 输出格式
返回 markdown 格式的图片链接：
```markdown
![配图描述](https://example.com/image.png)
```

## 踩坑笔记
- gemini 图片 URL 被安全策略阻止（openai.datas.systems）
- 错误：`SsrFBlockedError: Blocked: resolves to private/internal/special-use IP address`
- 解决：必须先用 exec curl 下载图片到本地，再用 filePath 发送，不能用 media URL
- Main agent 负责下载和发送，nano-banana 只返回 URL
