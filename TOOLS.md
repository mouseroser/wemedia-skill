# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## 本地工具坑位

- `read` / `write` / `edit` 尽量使用绝对路径；`~` 在工具参数里不一定会像 shell 一样自动展开，容易触发 `ENOENT`。
- `browser(action=upload)` 要求文件必须先放到 `/tmp/openclaw/uploads/`。
- 小红书这类富文本发布页里，`browser act/type/fill` 对正文框和话题弹层**不可靠**：可能覆盖整段正文、selector 漂移、计数与预览不同步。**正式发布脚本失效时，不要用 main/browser 手工补发表单顶替。**
- 当前环境里 `message(action="send")` 调用应显式带上 `buttons: []`，否则可能命中 schema 校验错误；但在主链 `sessions_spawn` 场景下，仍应默认由 `main` 统一发送可靠通知，不依赖 sub-agent 自推。
- `message(action="send")` **单发必须用 `target`（或底层 `to`）**，不要传 `targets`。`targets` 只给 `action="broadcast"`。若需要发多个群，按单目标**串行发送多次**，不要把多个群 id 塞进一次 `send`，否则旧版本运行时可能把消息静默回退到当前私聊。

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---
若本目录下存在 agent/、sessions/，视为 OpenClaw 内核 runtime 子目录，不参与流水线，请勿修改。
