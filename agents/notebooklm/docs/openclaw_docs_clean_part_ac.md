erated_at: "2026-02-03T07:54:27Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b7f4bd657d0df4feb5035c9f5ee727f9c67b991e9cedfc7768f99d010553fa01
  source_path: start/setup.md
  workflow: 15
---

# 设置

最后更新：2026-01-01

## 太长不看

- **个性化设置存放在仓库之外：** `~/.openclaw/workspace`（工作区）+ `~/.openclaw/openclaw.json`（配置）。
- **稳定工作流：** 安装 macOS 应用；让它运行内置的 Gateway 网关。
- **前沿工作流：** 通过 `pnpm gateway:watch` 自己运行 Gateway 网关，然后让 macOS 应用以本地模式连接。

## 先决条件（从源码）

- Node `>=22`
- `pnpm`
- Docker（可选；仅用于容器化设置/e2e — 参阅 [Docker](/install/docker)）

## 个性化策略（让更新不会造成问题）

如果你想要"100% 为我定制"*并且*易于更新，将你的自定义内容保存在：

- **配置：** `~/.openclaw/openclaw.json`（JSON/JSON5 格式）
- **工作区：** `~/.openclaw/workspace`（Skills、提示、记忆；将其设为私有 git 仓库）

引导一次：

```bash
openclaw setup
```

在此仓库内部，使用本地 CLI 入口：

```bash
openclaw setup
```

如果你还没有全局安装，通过 `pnpm openclaw setup` 运行它。

## 稳定工作流（macOS 应用优先）

1. 安装并启动 **OpenClaw.app**（菜单栏）。
2. 完成新手引导/权限检查清单（TCC 提示）。
3. 确保 Gateway 网关是**本地**并正在运行（应用管理它）。
4. 链接表面（示例：WhatsApp）：

```bash
openclaw channels login
```

5. 完整性检查：

```bash
openclaw health
```

如果你的构建版本中没有新手引导：

- 运行 `openclaw setup`，然后 `openclaw channels login`，然后手动启动 Gateway 网关（`openclaw gateway`）。

## 前沿工作流（在终端中运行 Gateway 网关）

目标：开发 TypeScript Gateway 网关，获得热重载，保持 macOS 应用 UI 连接。

### 0)（可选）也从源码运行 macOS 应用

如果你也想让 macOS 应用保持前沿：

```bash
./scripts/restart-mac.sh
```

### 1) 启动开发 Gateway 网关

```bash
pnpm install
pnpm gateway:watch
```

`gateway:watch` 以监视模式运行 Gateway 网关，并在 TypeScript 更改时重新加载。

### 2) 将 macOS 应用指向你正在运行的 Gateway 网关

在 **OpenClaw.app** 中：

- 连接模式：**本地**
  应用将连接到在配置端口上运行的 Gateway 网关。

### 3) 验证

- 应用内 Gateway 网关状态应显示 **"Using existing gateway …"**
- 或通过 CLI：

```bash
openclaw health
```

### 常见陷阱

- **端口错误：** Gateway 网关 WS 默认为 `ws://127.0.0.1:18789`；保持应用 + CLI 在同一端口上。
- **状态存储位置：**
  - 凭证：`~/.openclaw/credentials/`
  - 会话：`~/.openclaw/agents/<agentId>/sessions/`
  - 日志：`/tmp/openclaw/`

## 凭证存储映射

在调试认证或决定备份什么时使用此映射：

- **WhatsApp**：`~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- **Telegram bot token**：配置/环境变量或 `channels.telegram.tokenFile`
- **Discord bot token**：配置/环境变量（尚不支持令牌文件）
- **Slack tokens**：配置/环境变量（`channels.slack.*`）
- **配对允许列表**：`~/.openclaw/credentials/<channel>-allowFrom.json`
- **模型认证配置文件**：`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **旧版 OAuth 导入**：`~/.openclaw/credentials/oauth.json`
  更多详情：[安全](/gateway/security#credential-storage-map)。

## 更新（不破坏你的设置）

- 将 `~/.openclaw/workspace` 和 `~/.openclaw/` 保持为"你的东西"；不要将个人提示/配置放入 `openclaw` 仓库。
- 更新源码：`git pull` + `pnpm install`（当锁文件更改时）+ 继续使用 `pnpm gateway:watch`。

## Linux（systemd 用户服务）

Linux 安装使用 systemd **用户**服务。默认情况下，systemd 在注销/空闲时停止用户服务，这会终止 Gateway 网关。新手引导会尝试为你启用 lingering（可能提示 sudo）。如果仍然关闭，运行：

```bash
sudo loginctl enable-linger $USER
```

对于常驻或多用户服务器，考虑使用**系统**服务而不是用户服务（不需要 lingering）。参阅 [Gateway 网关运行手册](/gateway) 了解 systemd 说明。

## 相关文档

- [Gateway 网关运行手册](/gateway)（标志、监督、端口）
- [Gateway 网关配置](/gateway/configuration)（配置模式 + 示例）
- [Discord](/channels/discord) 和 [Telegram](/channels/telegram)（回复标签 + replyToMode 设置）
- [OpenClaw 助手设置](/start/openclaw)
- [macOS 应用](/platforms/macos)（Gateway 网关生命周期）


---
# File: docs/zh-CN/start/showcase.md

---
description: Real-world OpenClaw projects from the community
summary: 社区构建的基于 OpenClaw 的项目和集成
title: 案例展示
x-i18n:
  generated_at: "2026-02-03T10:11:36Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b3460f6a7b9948799a6082fee90fa8e5ac1d43e34872aea51ba431813dcead7a
  source_path: start/showcase.md
  workflow: 15
---

# 案例展示

来自社区的真实项目。看看大家正在用 OpenClaw 构建什么。

<Info>
**想要展示你的项目？** 在 [Discord 的 #showcase 频道](https://discord.gg/clawd) 分享或在 [X 上 @openclaw](https://x.com/openclaw)。
</Info>

## 🎥 OpenClaw 实战演示

VelvetShark 的完整设置演练（28 分钟）。

<div
  style={{
    position: "relative",
    paddingBottom: "56.25%",
    height: 0,
    overflow: "hidden",
    borderRadius: 16,
  }}
>
  <iframe
    src="https://www.youtube-nocookie.com/embed/SaWSPZoPX34"
    title="OpenClaw: The self-hosted AI that Siri should have been (Full setup)"
    style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}
    frameBorder="0"
    loading="lazy"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowFullScreen
  />
</div>

[在 YouTube 上观看](https://www.youtube.com/watch?v=SaWSPZoPX34)

<div
  style={{
    position: "relative",
    paddingBottom: "56.25%",
    height: 0,
    overflow: "hidden",
    borderRadius: 16,
  }}
>
  <iframe
    src="https://www.youtube-nocookie.com/embed/mMSKQvlmFuQ"
    title="OpenClaw showcase video"
    style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}
    frameBorder="0"
    loading="lazy"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowFullScreen
  />
</div>

[在 YouTube 上观看](https://www.youtube.com/watch?v=mMSKQvlmFuQ)

<div
  style={{
    position: "relative",
    paddingBottom: "56.25%",
    height: 0,
    overflow: "hidden",
    borderRadius: 16,
  }}
>
  <iframe
    src="https://www.youtube-nocookie.com/embed/5kkIJNUGFho"
    title="OpenClaw community showcase"
    style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}
    frameBorder="0"
    loading="lazy"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowFullScreen
  />
</div>

[在 YouTube 上观看](https://www.youtube.com/watch?v=5kkIJNUGFho)

## 🆕 Discord 最新分享

<CardGroup cols={2}>

<Card title="PR 审查 → Telegram 反馈" icon="code-pull-request" href="https://x.com/i/status/2010878524543131691">
  **@bangnokia** • `review` `github` `telegram`

OpenCode 完成更改 → 打开 PR → OpenClaw 审查差异并在 Telegram 中回复"小建议"加上明确的合并决定（包括需要先应用的关键修复）。

  <img src="/assets/showcase/pr-review-telegram.jpg" alt="OpenClaw PR review feedback delivered in Telegram" />
</Card>

<Card title="几分钟内创建酒窖 Skill" icon="wine-glass" href="https://x.com/i/status/2010916352454791216">
  **@prades_maxime** • `skills` `local` `csv`

向"Robby"（@openclaw）请求一个本地酒窖 skill。它请求一个示例 CSV 导出 + 存储位置，然后快速构建/测试该 skill（示例中有 962 瓶酒）。

  <img src="/assets/showcase/wine-cellar-skill.jpg" alt="OpenClaw building a local wine cellar skill from CSV" />
</Card>

<Card title="Tesco 购物自动驾驶" icon="cart-shopping" href="https://x.com/i/status/2009724862470689131">
  **@marchattonhere** • `automation` `browser` `shopping`

每周餐饮计划 → 常购商品 → 预订配送时段 → 确认订单。无需 API，仅使用浏览器控制。

  <img src="/assets/showcase/tesco-shop.jpg" alt="Tesco shop automation via chat" />
</Card>

<Card title="SNAG 截图转 Markdown" icon="scissors" href="https://github.com/am-will/snag">
  **@am-will** • `devtools` `screenshots` `markdown`

快捷键选择屏幕区域 → Gemini 视觉 → 即时 Markdown 到剪贴板。

  <img src="/assets/showcase/snag.png" alt="SNAG screenshot-to-markdown tool" />
</Card>

<Card title="Agents UI" icon="window-maximize" href="https://releaseflow.net/kitze/agents-ui">
  **@kitze** • `ui` `skills` `sync`

跨 Agents、Claude、Codex 和 OpenClaw 管理 skills/命令的桌面应用。

  <img src="/assets/showcase/agents-ui.jpg" alt="Agents UI app" />
</Card>

<Card title="Telegram 语音备忘录 (papla.media)" icon="microphone" href="https://papla.media/docs">
  **社区** • `voice` `tts` `telegram`

封装 papla.media TTS 并将结果作为 Telegram 语音备忘录发送（无烦人的自动播放）。

  <img src="/assets/showcase/papla-tts.jpg" alt="Telegram voice note output from TTS" />
</Card>

<Card title="CodexMonitor" icon="eye" href="https://clawhub.com/odrobnik/codexmonitor">
  **@odrobnik** • `devtools` `codex` `brew`

Homebrew 安装的助手工具，用于列出/检查/监视本地 OpenAI Codex 会话（CLI + VS Code）。

  <img src="/assets/showcase/codexmonitor.png" alt="CodexMonitor on ClawHub" />
</Card>

<Card title="Bambu 3D 打印机控制" icon="print" href="https://clawhub.com/tobiasbischoff/bambu-cli">
  **@tobiasbischoff** • `hardware` `3d-printing` `skill`

控制和排查 BambuLab 打印机：状态、任务、摄像头、AMS、校准等。

  <img src="/assets/showcase/bambu-cli.png" alt="Bambu CLI skill on ClawHub" />
</Card>

<Card title="维也纳交通 (Wiener Linien)" icon="train" href="https://clawhub.com/hjanuschka/wienerlinien">
  **@hjanuschka** • `travel` `transport` `skill`

维也纳公共交通的实时发车时间、中断信息、电梯状态和路线规划。

  <img src="/assets/showcase/wienerlinien.png" alt="Wiener Linien skill on ClawHub" />
</Card>

<Card title="ParentPay 学校餐食" icon="utensils" href="#">
  **@George5562** • `automation` `browser` `parenting`

通过 ParentPay 自动预订英国学校餐食。使用鼠标坐标实现可靠的表格单元格点击。
</Card>

<Card title="R2 上传 (Send Me My Files)" icon="cloud-arrow-up" href="https://clawhub.com/skills/r2-upload">
  **@julianengel** • `files` `r2` `presigned-urls`

上传到 Cloudflare R2/S3 并生成安全的预签名下载链接。非常适合远程 OpenClaw 实例。
</Card>

<Card title="通过 Telegram 开发 iOS 应用" icon="mobile" href="#">
  **@coard** • `ios` `xcode` `testflight`

构建了一个完整的带有地图和语音录制功能的 iOS 应用，完全通过 Telegram 聊天部署到 TestFlight。

  <img src="/assets/showcase/ios-testflight.jpg" alt="iOS app on TestFlight" />
</Card>

<Card title="Oura 戒指健康助手" icon="heart-pulse" href="#">
  **@AS** • `health` `oura` `calendar`

个人 AI 健康助手，将 Oura 戒指数据与日历、预约和健身房计划集成。

  <img src="/assets/showcase/oura-health.png" alt="Oura ring health assistant" />
</Card>
<Card title="Kev 的梦之队 (14+ 智能体)" icon="robot" href="https://github.com/adam91holt/orchestrated-ai-articles">
  **@adam91holt** • `multi-agent` `orchestration` `architecture` `manifesto`

一个 Gateway 网关下的 14+ 智能体，Opus 4.5 编排器将任务委派给 Codex 工作者。全面的[技术文章](https://github.com/adam91holt/orchestrated-ai-articles)涵盖梦之队阵容、模型选择、沙箱隔离、webhook、心跳和委派流程。用于智能体沙箱隔离的 [Clawdspace](https://github.com/adam91holt/clawdspace)。[博客文章](https://adams-ai-journey.ghost.io/2026-the-year-of-the-orchestrator/)。
</Card>

<Card title="Linear CLI" icon="terminal" href="https://github.com/Finesssee/linear-cli">
  **@NessZerra** • `devtools` `linear` `cli` `issues`

与智能体工作流（Claude Code、OpenClaw）集成的 Linear CLI。从终端管理问题、项目和工作流。首个外部 PR 已合并！
</Card>

<Card title="Beeper CLI" icon="message" href="https://github.com/blqke/beepcli">
  **@jules** • `messaging` `beeper` `cli` `automation`

通过 Beeper Desktop 读取、发送和归档消息。使用 Beeper 本地 MCP API，让智能体可以在一个地方管理你的所有聊天（iMessage、WhatsApp 等）。
</Card>

</CardGroup>

## 🤖 自动化与工作流

<CardGroup cols={2}>

<Card title="Winix 空气净化器控制" icon="wind" href="https://x.com/antonplex/status/2010518442471006253">
  **@antonplex** • `automation` `hardware` `air-quality`

Claude Code 发现并确认了净化器控制，然后 OpenClaw 接管来管理房间空气质量。

  <img src="/assets/showcase/winix-air-purifier.jpg" alt="Winix air purifier control via OpenClaw" />
</Card>

<Card title="美丽天空相机拍摄" icon="camera" href="https://x.com/signalgaining/status/2010523120604746151">
  **@signalgaining** • `automation` `camera` `skill` `images`

由屋顶摄像头触发：让 OpenClaw 在天空看起来很美的时候拍一张照片——它设计了一个 skill 并拍摄了照片。

  <img src="/assets/showcase/roof-camera-sky.jpg" alt="Roof camera sky snapshot captured by OpenClaw" />
</Card>

<Card title="可视化晨间简报场景" icon="robot" href="https://x.com/buddyhadry/status/2010005331925954739">
  **@buddyhadry** • `automation` `briefing` `images` `telegram`

定时提示每天早上通过 OpenClaw 角色生成一张"场景"图片（天气、任务、日期、喜欢的帖子/引言）。
</Card>

<Card title="板式网球场地预订" icon="calendar-check" href="https://github.com/joshp123/padel-cli">
  **@joshp123** • `automation` `booking` `cli`
  
  Playtomic 可用性检查器 + 预订 CLI。再也不会错过空闲场地。
  
  <img src="/assets/showcase/padel-screenshot.jpg" alt="padel-cli screenshot" />
</Card>

<Card title="会计收件" icon="file-invoice-dollar">
  **社区** • `automation` `email` `pdf`
  
  从邮件收集 PDF，为税务顾问准备文档。月度会计自动运行。
</Card>

<Card title="沙发土豆开发模式" icon="couch" href="https://davekiss.com">
  **@davekiss** • `telegram` `website` `migration` `astro`

一边看 Netflix 一边通过 Telegram 重建整个个人网站——Notion → Astro，迁移了 18 篇文章，DNS 转到 Cloudflare。从未打开笔记本电脑。
</Card>

<Card title="求职智能体" icon="briefcase">
  **@attol8** • `automation` `api` `skill`

搜索职位列表，与简历关键词匹配，返回带链接的相关机会。使用 JSearch API 在 30 分钟内构建。
</Card>

<Card title="Jira Skill 构建器" icon="diagram-project" href="https://x.com/jdrhyne/status/2008336434827002232">
  **@jdrhyne** • `automation` `jira` `skill` `devtools`

OpenClaw 连接到 Jira，然后即时生成一个新的 skill（在它出现在 ClawHub 之前）。
</Card>

<Card title="通过 Telegram 创建 Todoist Skill" icon="list-check" href="https://x.com/iamsubhrajyoti/status/2009949389884920153">
  **@iamsubhrajyoti** • `automation` `todoist` `skill` `telegram`

自动化 Todoist 任务，并让 OpenClaw 直接在 Telegram 聊天中生成 skill。
</Card>

<Card title="TradingView 分析" icon="chart-line">
  **@bheem1798** • `finance` `browser` `automation`

通过浏览器自动化登录 TradingView，截取图表屏幕截图，并按需执行技术分析。无需 API——只需浏览器控制。
</Card>

<Card title="Slack 自动支持" icon="slack">
  **@henrymascot** • `slack` `automation` `support`

监视公司 Slack 频道，提供有用的回复，并将通知转发到 Telegram。在没有被要求的情况下自主修复了已部署应用中的生产 bug。
</Card>

</CardGroup>

## 🧠 知识与记忆

<CardGroup cols={2}>

<Card title="xuezh 中文学习" icon="language" href="https://github.com/joshp123/xuezh">
  **@joshp123** • `learning` `voice` `skill`
  
  通过 OpenClaw 实现带有发音反馈和学习流程的中文学习引擎。
  
  <img src="/assets/showcase/xuezh-pronunciation.jpeg" alt="xuezh pronunciation feedback" />
</Card>

<Card title="WhatsApp 记忆库" icon="vault">
  **社区** • `memory` `transcription` `indexing`
  
  导入完整的 WhatsApp 导出，转录 1k+ 条语音备忘录，与 git 日志交叉检查，输出链接的 markdown 报告。
</Card>

<Card title="Karakeep 语义搜索" icon="magnifying-glass" href="https://github.com/jamesbrooksco/karakeep-semantic-search">
  **@jamesbrooksco** • `search` `vector` `bookmarks`
  
  使用 Qdrant + OpenAI/Ollama embeddings 为 Karakeep 书签添加向量搜索。
</Card>

<Card title="Inside-Out-2 记忆" icon="brain">
  **社区** • `memory` `beliefs` `self-model`
  
  独立的记忆管理器，将会话文件转化为记忆 → 信念 → 演化的自我模型。
</Card>

</CardGroup>

## 🎙️ 语音与电话

<CardGroup cols={2}>

<Card title="Clawdia 电话桥接" icon="phone" href="https://github.com/alejandroOPI/clawdia-bridge">
  **@alejandroOPI** • `voice` `vapi` `bridge`
  
  Vapi 语音助手 ↔ OpenClaw HTTP 桥接。与你的智能体进行近实时电话通话。
</Card>

<Card title="OpenRouter 转录" icon="microphone" href="https://clawhub.com/obviyus/openrouter-transcribe">
  **@obviyus** • `transcription` `multilingual` `skill`

通过 OpenRouter（Gemini 等）进行多语言音频转录。可在 ClawHub 获取。
</Card>

</CardGroup>

## 🏗️ 基础设施与部署

<CardGroup cols={2}>

<Card title="Home Assistant 插件" icon="home" href="https://github.com/ngutman/openclaw-ha-addon">
  **@ngutman** • `homeassistant` `docker` `raspberry-pi`
  
  在 Home Assistant OS 上运行的 OpenClaw Gateway 网关，支持 SSH 隧道和持久状态。
</Card>

<Card title="Home Assistant Skill" icon="toggle-on" href="https://clawhub.com/skills/homeassistant">
  **ClawHub** • `homeassistant` `skill` `automation`
  
  通过自然语言控制和自动化 Home Assistant 设备。
</Card>

<Card title="Nix 打包" icon="snowflake" href="https://github.com/openclaw/nix-openclaw">
  **@openclaw** • `nix` `packaging` `deployment`
  
  开箱即用的 nixified OpenClaw 配置，用于可复现的部署。
</Card>

<Card title="CalDAV 日历" icon="calendar" href="https://clawhub.com/skills/caldav-calendar">
  **ClawHub** • `calendar` `caldav` `skill`
  
  使用 khal/vdirsyncer 的日历 skill。自托管日历集成。
</Card>

</CardGroup>

## 🏠 家居与硬件

<CardGroup cols={2}>

<Card title="GoHome 自动化" icon="house-signal" href="https://github.com/joshp123/gohome">
  **@joshp123** • `home` `nix` `grafana`
  
  Nix 原生家庭自动化，以 OpenClaw 作为界面，加上漂亮的 Grafana 仪表板。
  
  <img src="/assets/showcase/gohome-grafana.png" alt="GoHome Grafana dashboard" />
</Card>

<Card title="Roborock 扫地机器人" icon="robot" href="https://github.com/joshp123/gohome/tree/main/plugins/roborock">
  **@joshp123** • `vacuum` `iot` `plugin`
  
  通过自然对话控制你的 Roborock 扫地机器人。
  
  <img src="/assets/showcase/roborock-screenshot.jpg" alt="Roborock status" />
</Card>

</CardGroup>

## 🌟 社区项目

<CardGroup cols={2}>

<Card title="StarSwap 市场" icon="star" href="https://star-swap.com/">
  **社区** • `marketplace` `astronomy` `webapp`
  
  完整的天文设备市场。围绕 OpenClaw 生态系统构建。
</Card>

</CardGroup>

---

## 提交你的项目

有想分享的东西？我们很乐意展示它！

<Steps>
  <Step title="分享它">
    在 [Discord 的 #showcase 频道](https://discord.gg/clawd) 发布或在 [Twitter 上 @openclaw](https://x.com/openclaw)
  </Step>
  <Step title="包含详细信息">
    告诉我们它做什么，链接到仓库/演示，如果有的话分享截图
  </Step>
  <Step title="获得展示">
    我们会将优秀项目添加到此页面
  </Step>
</Steps>


---
# File: docs/zh-CN/start/wizard.md

---
read_when:
  - 运行或配置新手引导向导
  - 设置新机器
summary: CLI 新手引导向导：引导式配置 Gateway 网关、工作区、渠道和 Skills
title: 新手引导向导
x-i18n:
  generated_at: "2026-02-03T09:20:27Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 45e10d31048d927ee6546e35b050914f0e6e21a4dee298b3b277eebe7c133732
  source_path: start/wizard.md
  workflow: 15
---

# 新手引导向导（CLI）

新手引导向导是在 macOS、Linux 或 Windows（通过 WSL2；强烈推荐）上设置 OpenClaw 的**推荐**方式。
它可以在一个引导式流程中配置本地 Gateway 网关或远程 Gateway 网关连接，以及渠道、Skills 和工作区默认值。

主要入口：

```bash
openclaw onboard
```

最快开始聊天的方式：打开控制界面（无需设置渠道）。运行 `openclaw dashboard` 并在浏览器中聊天。文档：[控制面板](/web/dashboard)。

后续重新配置：

```bash
openclaw configure
```

推荐：设置 Brave Search API 密钥，以便智能体可以使用 `web_search`（`web_fetch` 无需密钥即可使用）。最简单的方式：`openclaw configure --section web`，它会存储 `tools.web.search.apiKey`。文档：[Web 工具](/tools/web)。

## 快速开始 vs 高级

向导从**快速开始**（默认值）vs **高级**（完全控制）开始。

**快速开始**保持默认值：

- 本地 Gateway 网关（loopback）
- 默认工作区（或现有工作区）
- Gateway 网关端口 **18789**
- Gateway 网关认证 **Token**（自动生成，即使在 loopback 上）
- Tailscale 暴露 **关闭**
- Telegram + WhatsApp 私信默认使用**允许列表**（系统会提示你输入电话号码）

**高级**暴露每个步骤（模式、工作区、Gateway 网关、渠道、守护进程、Skills）。

## 向导做了什么

**本地模式（默认）**引导你完成：

- 模型/认证（OpenAI Code (Codex) 订阅 OAuth、Anthropic API 密钥（推荐）或 setup-token（粘贴），以及 MiniMax/GLM/Moonshot/AI Gateway 选项）
- 工作区位置 + 引导文件
- Gateway 网关设置（端口/绑定/认证/tailscale）
- 提供商（Telegram、WhatsApp、Discord、Google Chat、Mattermost（插件）、Signal）
- 守护进程安装（LaunchAgent / systemd 用户单元）
- 健康检查
- Skills（推荐）

**远程模式**仅配置本地客户端连接到其他位置的 Gateway 网关。
它**不会**在远程主机上安装或更改任何内容。

要添加更多隔离的智能体（独立的工作区 + 会话 + 认证），使用：

```bash
openclaw agents add <name>
```

提示：`--json` **不**意味着非交互模式。脚本中请使用 `--non-interactive`（和 `--workspace`）。

## 流程详情（本地）

1. **现有配置检测**
   - 如果 `~/.openclaw/openclaw.json` 存在，选择**保留 / 修改 / 重置**。
   - 重新运行向导**不会**清除任何内容，除非你明确选择**重置**（或传递 `--reset`）。
   - 如果配置无效或包含遗留键名，向导会停止并要求你在继续之前运行 `openclaw doctor`。
   - 重置使用 `trash`（永不使用 `rm`）并提供范围选项：
     - 仅配置
     - 配置 + 凭证 + 会话
     - 完全重置（同时删除工作区）

2. **模型/认证**
   - **Anthropic API 密钥（推荐）**：如果存在则使用 `ANTHROPIC_API_KEY`，否则提示输入密钥，然后保存供守护进程使用。
   - **Anthropic OAuth（Claude Code CLI）**：在 macOS 上，向导检查钥匙串项目"Claude Code-credentials"（选择"始终允许"以便 launchd 启动不会阻塞）；在 Linux/Windows 上，如果存在则复用 `~/.claude/.credentials.json`。
   - **Anthropic 令牌（粘贴 setup-token）**：在任何机器上运行 `claude setup-token`，然后粘贴令牌（你可以命名它；空白 = 默认）。
   - **OpenAI Code (Codex) 订阅（Codex CLI）**：如果 `~/.codex/auth.json` 存在，向导可以复用它。
   - **OpenAI Code (Codex) 订阅（OAuth）**：浏览器流程；粘贴 `code#state`。
     - 当模型未设置或为 `openai/*` 时，将 `agents.defaults.model` 设置为 `openai-codex/gpt-5.2`。
   - **OpenAI API 密钥**：如果存在则使用 `OPENAI_API_KEY`，否则提示输入密钥，然后保存到 `~/.openclaw/.env` 以便 launchd 可以读取。
   - **OpenCode Zen（多模型代理）**：提示输入 `OPENCODE_API_KEY`（或 `OPENCODE_ZEN_API_KEY`，在 https://opencode.ai/auth 获取）。
   - **API 密钥**：为你存储密钥。
   - **Vercel AI Gateway（多模型代理）**：提示输入 `AI_GATEWAY_API_KEY`。
   - 更多详情：[Vercel AI Gateway](/providers/vercel-ai-gateway)
   - **MiniMax M2.1**：自动写入配置。
   - 更多详情：[MiniMax](/providers/minimax)
   - **Synthetic（Anthropic 兼容）**：提示输入 `SYNTHETIC_API_KEY`。
   - 更多详情：[Synthetic](/providers/synthetic)
   - **Moonshot（Kimi K2）**：自动写入配置。
   - **Kimi Coding**：自动写入配置。
   - 更多详情：[Moonshot AI（Kimi + Kimi Coding）](/providers/moonshot)
   - **跳过**：尚未配置认证。
   - 从检测到的选项中选择默认模型（或手动输入提供商/模型）。
   - 向导运行模型检查，如果配置的模型未知或缺少认证则发出警告。

- OAuth 凭证存储在 `~/.openclaw/credentials/oauth.json`；认证配置文件存储在 `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`（API 密钥 + OAuth）。
- 更多详情：[/concepts/oauth](/concepts/oauth)

3. **工作区**
   - 默认 `~/.openclaw/workspace`（可配置）。
   - 为智能体引导仪式播种所需的工作区文件。
   - 完整的工作区布局 + 备份指南：[智能体工作区](/concepts/agent-workspace)

4. **Gateway 网关**
   - 端口、绑定、认证模式、tailscale 暴露。
   - 认证建议：即使对于 loopback 也保持 **Token**，以便本地 WS 客户端必须进行认证。
   - 仅当你完全信任每个本地进程时才禁用认证。
   - 非 loopback 绑定仍需要认证。

5. **渠道**
   - [WhatsApp](/channels/whatsapp)：可选的二维码登录。
   - [Telegram](/channels/telegram)：机器人令牌。
   - [Discord](/channels/discord)：机器人令牌。
   - [Google Chat](/channels/googlechat)：服务账户 JSON + webhook 受众。
   - [Mattermost](/channels/mattermost)（插件）：机器人令牌 + 基础 URL。
   - [Signal](/channels/signal)：可选的 `signal-cli` 安装 + 账户配置。
   - [iMessage](/channels/imessage)：本地 `imsg` CLI 路径 + 数据库访问。
   - 私信安全：默认为配对。第一条私信发送验证码；通过 `openclaw pairing approve <channel> <code>` 批准或使用允许列表。

6. **守护进程安装**
   - macOS：LaunchAgent
     - 需要已登录的用户会话；对于无头环境，使用自定义 LaunchDaemon（未提供）。
   - Linux（和通过 WSL2 的 Windows）：systemd 用户单元
     - 向导尝试通过 `loginctl enable-linger <user>` 启用 lingering，以便 Gateway 网关在注销后保持运行。
     - 可能提示 sudo（写入 `/var/lib/systemd/linger`）；它首先尝试不使用 sudo。
   - **运行时选择：**Node（推荐；WhatsApp/Telegram 需要）。**不推荐** Bun。

7. **健康检查**
   - 启动 Gateway 网关（如果需要）并运行 `openclaw health`。
   - 提示：`openclaw status --deep` 在状态输出中添加 Gateway 网关健康探测（需要可达的 Gateway 网关）。

8. **Skills（推荐）**
   - 读取可用的 Skills 并检查要求。
   - 让你选择节点管理器：**npm / pnpm**（不推荐 bun）。
   - 安装可选依赖项（某些在 macOS 上使用 Homebrew）。

9. **完成**
   - 总结 + 后续步骤，包括用于额外功能的 iOS/Android/macOS 应用。

- 如果未检测到 GUI，向导会打印控制界面的 SSH 端口转发说明，而不是打开浏览器。
- 如果控制界面资源缺失，向导会尝试构建它们；回退方案是 `pnpm ui:build`（自动安装 UI 依赖）。

## 远程模式

远程模式配置本地客户端连接到其他位置的 Gateway 网关。

你将设置的内容：

- 远程 Gateway 网关 URL（`ws://...`）
- 如果远程 Gateway 网关需要认证则需要令牌（推荐）

注意事项：

- 不执行远程安装或守护进程更改。
- 如果 Gateway 网关仅限 loopback，使用 SSH 隧道或 tailnet。
- 发现提示：
  - macOS：Bonjour（`dns-sd`）
  - Linux：Avahi（`avahi-browse`）

## 添加另一个智能体

使用 `openclaw agents add <name>` 创建一个具有独立工作区、会话和认证配置文件的单独智能体。不带 `--workspace` 运行会启动向导。

它设置的内容：

- `agents.list[].name`
- `agents.list[].workspace`
- `agents.list[].agentDir`

注意事项：

- 默认工作区遵循 `~/.openclaw/workspace-<agentId>`。
- 添加 `bindings` 以路由入站消息（向导可以执行此操作）。
- 非交互标志：`--model`、`--agent-dir`、`--bind`、`--non-interactive`。

## 非交互模式

使用 `--non-interactive` 自动化或脚本化新手引导：

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

添加 `--json` 以获取机器可读的摘要。

Gemini 示例：

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Z.AI 示例：

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice zai-api-key \
  --zai-api-key "$ZAI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Vercel AI Gateway 示例：

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Moonshot 示例：

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice moonshot-api-key \
  --moonshot-api-key "$MOONSHOT_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Synthetic 示例：

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice synthetic-api-key \
  --synthetic-api-key "$SYNTHETIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

OpenCode Zen 示例：

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice opencode-zen \
  --opencode-zen-api-key "$OPENCODE_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

添加智能体（非交互）示例：

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

## Gateway 网关向导 RPC

Gateway 网关通过 RPC 暴露向导流程（`wizard.start`、`wizard.next`、`wizard.cancel`、`wizard.status`）。
客户端（macOS 应用、控制界面）可以渲染步骤而无需重新实现新手引导逻辑。

## Signal 设置（signal-cli）

向导可以从 GitHub releases 安装 `signal-cli`：

- 下载适当的发布资源。
- 存储在 `~/.openclaw/tools/signal-cli/<version>/` 下。
- 将 `channels.signal.cliPath` 写入你的配置。

注意事项：

- JVM 构建需要 **Java 21**。
- 可用时使用原生构建。
- Windows 使用 WSL2；signal-cli 安装在 WSL 内遵循 Linux 流程。

## 向导写入的内容

`~/.openclaw/openclaw.json` 中的典型字段：

- `agents.defaults.workspace`
- `agents.defaults.model` / `models.providers`（如果选择了 Minimax）
- `gateway.*`（模式、绑定、认证、tailscale）
- `channels.telegram.botToken`、`channels.discord.token`、`channels.signal.*`、`channels.imessage.*`
- 当你在提示中选择加入时的渠道允许列表（Slack/Discord/Matrix/Microsoft Teams）（名称在可能时解析为 ID）。
- `skills.install.nodeManager`
- `wizard.lastRunAt`
- `wizard.lastRunVersion`
- `wizard.lastRunCommit`
- `wizard.lastRunCommand`
- `wizard.lastRunMode`

`openclaw agents add` 写入 `agents.list[]` 和可选的 `bindings`。

WhatsApp 凭证存储在 `~/.openclaw/credentials/whatsapp/<accountId>/` 下。
会话存储在 `~/.openclaw/agents/<agentId>/sessions/` 下。

某些渠道以插件形式提供。当你在新手引导期间选择一个时，向导会在配置之前提示安装它（npm 或本地路径）。

## 相关文档

- macOS 应用新手引导：[新手引导](/start/onboarding)
- 配置参考：[Gateway 网关配置](/gateway/configuration)
- 提供商：[WhatsApp](/channels/whatsapp)、[Telegram](/channels/telegram)、[Discord](/channels/discord)、[Google Chat](/channels/googlechat)、[Signal](/channels/signal)、[iMessage](/channels/imessage)
- Skills：[Skills](/tools/skills)、[Skills 配置](/tools/skills-config)


---
# File: docs/zh-CN/tools/agent-send.md

---
read_when:
  - 添加或修改智能体 CLI 入口点
summary: 直接 `openclaw agent` CLI 运行（带可选投递）
title: Agent Send
x-i18n:
  generated_at: "2026-02-03T07:54:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a84d6a304333eebe155da2bf24cf5fc0482022a0a48ab34aa1465cd6e667022d
  source_path: tools/agent-send.md
  workflow: 15
---

# `openclaw agent`（直接智能体运行）

`openclaw agent` 运行单个智能体回合，无需入站聊天消息。
默认情况下它**通过 Gateway 网关**运行；添加 `--local` 以强制在当前机器上使用嵌入式运行时。

## 行为

- 必需：`--message <text>`
- 会话选择：
  - `--to <dest>` 派生会话键（群组/频道目标保持隔离；直接聊天折叠到 `main`），**或**
  - `--session-id <id>` 通过 ID 重用现有会话，**或**
  - `--agent <id>` 直接定位已配置的智能体（使用该智能体的 `main` 会话键）
- 运行与正常入站回复相同的嵌入式智能体运行时。
- 思考/详细标志持久化到会话存储中。
- 输出：
  - 默认：打印回复文本（加上 `MEDIA:<url>` 行）
  - `--json`：打印结构化负载 + 元数据
- 可选使用 `--deliver` + `--channel` 将回复投递回渠道（目标格式与 `openclaw message --target` 匹配）。
- 使用 `--reply-channel`/`--reply-to`/`--reply-account` 覆盖投递而不更改会话。

如果 Gateway 网关不可达，CLI 会**回退**到嵌入式本地运行。

## 示例

```bash
openclaw agent --to +15555550123 --message "status update"
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --to +15555550123 --message "Summon reply" --deliver
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

## 标志

- `--local`：本地运行（需要你的 shell 中有模型提供商 API 密钥）
- `--deliver`：将回复发送到所选渠道
- `--channel`：投递渠道（`whatsapp|telegram|discord|googlechat|slack|signal|imessage`，默认：`whatsapp`）
- `--reply-to`：投递目标覆盖
- `--reply-channel`：投递渠道覆盖
- `--reply-account`：投递账户 ID 覆盖
- `--thinking <off|minimal|low|medium|high|xhigh>`：持久化思考级别（仅限 GPT-5.2 + Codex 模型）
- `--verbose <on|full|off>`：持久化详细级别
- `--timeout <seconds>`：覆盖智能体超时
- `--json`：输出结构化 JSON


---
# File: docs/zh-CN/tools/apply-patch.md

---
read_when:
  - 你需要跨多个文件进行结构化编辑
  - 你想要记录或调试基于补丁的编辑
summary: 使用 apply_patch 工具应用多文件补丁
title: apply_patch 工具
x-i18n:
  generated_at: "2026-02-01T21:39:24Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8cec2b4ee3afa9105fc3dd1bc28a338917df129afc634ac83620a3347c46bcec
  source_path: tools/apply-patch.md
  workflow: 15
---

# apply_patch 工具

使用结构化补丁格式应用文件更改。这非常适合多文件
或多段编辑，在这些场景下单次 `edit` 调用会很脆弱。

该工具接受一个 `input` 字符串，其中包含一个或多个文件操作：

```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

## 参数

- `input`（必需）：完整的补丁内容，包括 `*** Begin Patch` 和 `*** End Patch`。

## 说明

- 路径相对于工作区根目录解析。
- 在 `*** Update File:` 段中使用 `*** Move to:` 可重命名文件。
- 需要时使用 `*** End of File` 标记仅在文件末尾的插入。
- 实验性功能，默认禁用。通过 `tools.exec.applyPatch.enabled` 启用。
- 仅限 OpenAI（包括 OpenAI Codex）。可选通过
  `tools.exec.applyPatch.allowModels` 按模型进行限制。
- 配置仅在 `tools.exec` 下。

## 示例

```json
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```


---
# File: docs/zh-CN/tools/browser-linux-troubleshooting.md

---
read_when: Browser control fails on Linux, especially with snap Chromium
summary: 修复 Linux 上 OpenClaw 浏览器控制的 Chrome/Brave/Edge/Chromium CDP 启动问题
title: 浏览器故障排除
x-i18n:
  generated_at: "2026-02-03T07:55:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bac2301022511a0bf8ebe1309606cc03e8a979ff74866c894f89d280ca3e514e
  source_path: tools/browser-linux-troubleshooting.md
  workflow: 15
---

# 浏览器故障排除（Linux）

## 问题："Failed to start Chrome CDP on port 18800"

OpenClaw 的浏览器控制服务器无法启动 Chrome/Brave/Edge/Chromium，出现以下错误：

```
{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}
```

### 根本原因

在 Ubuntu（和许多 Linux 发行版）上，默认的 Chromium 安装是 **snap 包**。Snap 的 AppArmor 限制会干扰 OpenClaw 启动和监控浏览器进程的方式。

`apt install chromium` 命令安装的是一个重定向到 snap 的存根包：

```
Note, selecting 'chromium-browser' instead of 'chromium'
chromium-browser is already the newest version (2:1snap1-0ubuntu2).
```

这不是真正的浏览器——它只是一个包装器。

### 解决方案 1：安装 Google Chrome（推荐）

安装官方 Google Chrome `.deb` 包，它不受 snap 沙箱限制：

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # if there are dependency errors
```

然后更新你的 OpenClaw 配置（`~/.openclaw/openclaw.json`）：

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

### 解决方案 2：使用 Snap Chromium 的仅附加模式

如果你必须使用 snap Chromium，配置 OpenClaw 附加到手动启动的浏览器：

1. 更新配置：

```json
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "headless": true,
    "noSandbox": true
  }
}
```

2. 手动启动 Chromium：

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

3. 可选创建 systemd 用户服务以自动启动 Chrome：

```ini
# ~/.config/systemd/user/openclaw-browser.service
[Unit]
Description=OpenClaw Browser (Chrome CDP)
After=network.target

[Service]
ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

启用：`systemctl --user enable --now openclaw-browser.service`

### 验证浏览器是否工作

检查状态：

```bash
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'
```

测试浏览：

```bash
curl -s -X POST http://127.0.0.1:18791/start
curl -s http://127.0.0.1:18791/tabs
```

### 配置参考

| 选项                     | 描述                                                          | 默认值                                           |
| ------------------------ | ------------------------------------------------------------- | ------------------------------------------------ |
| `browser.enabled`        | 启用浏览器控制                                                | `true`                                           |
| `browser.executablePath` | Chromium 系浏览器二进制文件路径（Chrome/Brave/Edge/Chromium） | 自动检测（当默认浏览器是 Chromium 系时优先使用） |
| `browser.headless`       | 无 GUI 运行                                                   | `false`                                          |
| `browser.noSandbox`      | 添加 `--no-sandbox` 标志（某些 Linux 设置需要）               | `false`                                          |
| `browser.attachOnly`     | 不启动浏览器，仅附加到现有浏览器                              | `false`                                          |
| `browser.cdpPort`        | Chrome DevTools Protocol 端口                                 | `18800`                                          |

### 问题："Chrome extension relay is running, but no tab is connected"

你正在使用 `chrome` 配置文件（扩展中继）。它期望 OpenClaw 浏览器扩展附加到一个活动标签页。

修复选项：

1. **使用托管浏览器：** `openclaw browser start --browser-profile openclaw`
   （或设置 `browser.defaultProfile: "openclaw"`）。
2. **使用扩展中继：** 安装扩展，打开一个标签页，然后点击 OpenClaw 扩展图标来附加它。

注意事项：

- `chrome` 配置文件在可能时使用你的**系统默认 Chromium 浏览器**。
- 本地 `openclaw` 配置文件自动分配 `cdpPort`/`cdpUrl`；仅为远程 CDP 设置这些。


---
# File: docs/zh-CN/tools/browser-login.md

---
read_when:
  - 你需要为浏览器自动化登录网站
  - 你想在 X/Twitter 上发布更新
summary: 用于浏览器自动化 + X/Twitter 发帖的手动登录
title: 浏览器登录
x-i18n:
  generated_at: "2026-02-03T07:55:03Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8ceea2d5258836e3db10f858ee122b5832a40f83a72ba18de140671091eef5a8
  source_path: tools/browser-login.md
  workflow: 15
---

# 浏览器登录 + X/Twitter 发帖

## 手动登录（推荐）

当网站需要登录时，请在**主机**浏览器配置文件（openclaw 浏览器）中**手动登录**。

**不要**将你的凭证提供给模型。自动登录通常会触发反机器人防御并可能锁定账户。

返回主浏览器文档：[浏览器](/tools/browser)。

## 使用哪个 Chrome 配置文件？

OpenClaw 控制一个**专用的 Chrome 配置文件**（名为 `openclaw`，橙色调 UI）。这与你的日常浏览器配置文件是分开的。

两种简单的访问方式：

1. **让智能体打开浏览器**，然后你自己登录。
2. **通过 CLI 打开**：

```bash
openclaw browser start
openclaw browser open https://x.com
```

如果你有多个配置文件，传入 `--browser-profile <name>`（默认是 `openclaw`）。

## X/Twitter：推荐流程

- **阅读/搜索/话题：** 使用 **bird** CLI Skills（无浏览器，稳定）。
  - 仓库：https://github.com/steipete/bird
- **发布更新：** 使用**主机**浏览器（手动登录）。

## 沙箱隔离 + 主机浏览器访问

沙箱隔离的浏览器会话**更容易**触发机器人检测。对于 X/Twitter（和其他严格的网站），优先使用**主机**浏览器。

如果智能体在沙箱中，浏览器工具默认使用沙箱。要允许主机控制：

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

然后定位主机浏览器：

```bash
openclaw browser open https://x.com --browser-profile openclaw --target host
```

或者为发布更新的智能体禁用沙箱隔离。


---
# File: docs/zh-CN/tools/browser.md

---
read_when:
  - 添加智能体控制的浏览器自动化
  - 调试 openclaw 干扰你自己 Chrome 的问题
  - 在 macOS 应用中实现浏览器设置和生命周期管理
summary: 集成浏览器控制服务 + 操作命令
title: 浏览器（OpenClaw 托管）
x-i18n:
  generated_at: "2026-02-03T09:26:06Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a868d040183436a1fb355130995e79782cb817b5ea298beaf1e1d2cb82e21c4c
  source_path: tools/browser.md
  workflow: 15
---

# 浏览器（openclaw 托管）

OpenClaw 可以运行一个由智能体控制的**专用 Chrome/Brave/Edge/Chromium 配置文件**。
它与你的个人浏览器隔离，通过 Gateway 网关内部的小型本地控制服务进行管理（仅限 loopback）。

新手视角：

- 把它想象成一个**独立的、仅供智能体使用的浏览器**。
- `openclaw` 配置文件**不会**触及你的个人浏览器配置文件。
- 智能体可以在安全的通道中**打开标签页、读取页面、点击和输入**。
- 默认的 `chrome` 配置文件通过扩展中继使用**系统默认的 Chromium 浏览器**；切换到 `openclaw` 可使用隔离的托管浏览器。

## 功能概览

- 一个名为 **openclaw** 的独立浏览器配置文件（默认橙色主题）。
- 确定性标签页控制（列出/打开/聚焦/关闭）。
- 智能体操作（点击/输入/拖动/选择）、快照、截图、PDF。
- 可选的多配置文件支持（`openclaw`、`work`、`remote` 等）。

此浏览器**不是**你的日常浏览器。它是一个安全、隔离的界面，用于智能体自动化和验证。

## 快速开始

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

如果出现"Browser disabled"，请在配置中启用它（见下文）并重启 Gateway 网关。

## 配置文件：`openclaw` 与 `chrome`

- `openclaw`：托管的隔离浏览器（无需扩展）。
- `chrome`：到你**系统浏览器**的扩展中继（需要将 OpenClaw 扩展附加到标签页）。

如果你希望默认使用托管模式，请设置 `browser.defaultProfile: "openclaw"`。

## 配置

浏览器设置位于 `~/.openclaw/openclaw.json`。

```json5
{
  browser: {
    enabled: true, // default: true
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    remoteCdpTimeoutMs: 1500, // remote CDP HTTP timeout (ms)
    remoteCdpHandshakeTimeoutMs: 3000, // remote CDP WebSocket handshake timeout (ms)
    defaultProfile: "chrome",
    color: "#FF4500",
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
  },
}
```

注意事项：

- 浏览器控制服务绑定到 loopback 上的端口，该端口从 `gateway.port` 派生（默认：`18791`，即 gateway + 2）。中继使用下一个端口（`18792`）。
- 如果你覆盖了 Gateway 网关端口（`gateway.port` 或 `OPENCLAW_GATEWAY_PORT`），派生的浏览器端口会相应调整以保持在同一"系列"中。
- 未设置时，`cdpUrl` 默认为中继端口。
- `remoteCdpTimeoutMs` 适用于远程（非 loopback）CDP 可达性检查。
- `remoteCdpHandshakeTimeoutMs` 适用于远程 CDP WebSocket 可达性检查。
- `attachOnly: true` 表示"永不启动本地浏览器；仅在浏览器已运行时附加"。
- `color` + 每个配置文件的 `color` 为浏览器 UI 着色，以便你能看到哪个配置文件处于活动状态。
- 默认配置文件是 `chrome`（扩展中继）。使用 `defaultProfile: "openclaw"` 来使用托管浏览器。
- 自动检测顺序：如果系统默认浏览器是基于 Chromium 的则使用它；否则 Chrome → Brave → Edge → Chromium → Chrome Canary。
- 本地 `openclaw` 配置文件会自动分配 `cdpPort`/`cdpUrl` — 仅为远程 CDP 设置这些。

## 使用 Brave（或其他基于 Chromium 的浏览器）

如果你的**系统默认**浏览器是基于 Chromium 的（Chrome/Brave/Edge 等），OpenClaw 会自动使用它。设置 `browser.executablePath` 可覆盖自动检测：

CLI 示例：

```bash
openclaw config set browser.executablePath "/usr/bin/google-chrome"
```

```json5
// macOS
{
  browser: {
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
  }
}

// Windows
{
  browser: {
    executablePath: "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
  }
}

// Linux
{
  browser: {
    executablePath: "/usr/bin/brave-browser"
  }
}
```

## 本地控制与远程控制

- **本地控制（默认）：** Gateway 网关启动 loopback 控制服务，可以启动本地浏览器。
- **远程控制（节点主机）：** 在有浏览器的机器上运行节点主机；Gateway 网关将浏览器操作代理到该节点。
- **远程 CDP：** 设置 `browser.profiles.<name>.cdpUrl`（或 `browser.cdpUrl`）以附加到远程的基于 Chromium 的浏览器。在这种情况下，OpenClaw 不会启动本地浏览器。

远程 CDP URL 可以包含认证信息：

- 查询令牌（例如 `https://provider.example?token=<token>`）
- HTTP Basic 认证（例如 `https://user:pass@provider.example`）

OpenClaw 在调用 `/json/*` 端点和连接 CDP WebSocket 时会保留认证信息。建议使用环境变量或密钥管理器存储令牌，而不是将其提交到配置文件中。

## 节点浏览器代理（零配置默认）

如果你在有浏览器的机器上运行**节点主机**，OpenClaw 可以自动将浏览器工具调用路由到该节点，无需任何额外的浏览器配置。这是远程 Gateway 网关的默认路径。

注意事项：

- 节点主机通过**代理命令**暴露其本地浏览器控制服务器。
- 配置文件来自节点自己的 `browser.profiles` 配置（与本地相同）。
- 如果不需要可以禁用：
  - 在节点上：`nodeHost.browserProxy.enabled=false`
  - 在 Gateway 网关上：`gateway.nodes.browser.mode="off"`

## Browserless（托管远程 CDP）

[Browserless](https://browserless.io) 是一个托管的 Chromium 服务，通过 HTTPS 暴露 CDP 端点。你可以将 OpenClaw 浏览器配置文件指向 Browserless 区域端点，并使用你的 API 密钥进行认证。

示例：

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserless",
    remoteCdpTimeoutMs: 2000,
    remoteCdpHandshakeTimeoutMs: 4000,
    profiles: {
      browserless: {
        cdpUrl: "https://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        color: "#00AA00",
      },
    },
  },
}
```

注意事项：

- 将 `<BROWSERLESS_API_KEY>` 替换为你真实的 Browserless 令牌。
- 选择与你的 Browserless 账户匹配的区域端点（请参阅其文档）。

## 安全性

核心理念：

- 浏览器控制仅限 loopback；访问通过 Gateway 网关的认证或节点配对进行。
- 将 Gateway 网关和任何节点主机保持在私有网络上（Tailscale）；避免公开暴露。
- 将远程 CDP URL/令牌视为机密；优先使用环境变量或密钥管理器。

远程 CDP 提示：

- 尽可能使用 HTTPS 端点和短期令牌。
- 避免在配置文件中直接嵌入长期令牌。

## 配置文件（多浏览器）

OpenClaw 支持多个命名配置文件（路由配置）。配置文件可以是：

- **openclaw 托管**：具有独立用户数据目录和 CDP 端口的专用基于 Chromium 的浏览器实例
- **远程**：显式 CDP URL（在其他地方运行的基于 Chromium 的浏览器）
- **扩展中继**：通过本地中继 + Chrome 扩展访问你现有的 Chrome 标签页

默认值：

- 如果缺少 `openclaw` 配置文件，会自动创建。
- `chrome` 配置文件是内置的，用于 Chrome 扩展中继（默认指向 `http://127.0.0.1:18792`）。
- 本地 CDP 端口默认从 **18800–18899** 分配。
- 删除配置文件会将其本地数据目录移至回收站。

所有控制端点接受 `?profile=<name>`；CLI 使用 `--browser-profile`。

## Chrome 扩展中继（使用你现有的 Chrome）

OpenClaw 还可以通过本地 CDP 中继 + Chrome 扩展驱动**你现有的 Chrome 标签页**（无需单独的"openclaw"Chrome 实例）。

完整指南：[Chrome 扩展](/tools/chrome-extension)

流程：

- Gateway 网关在本地运行（同一台机器）或节点主机在浏览器所在机器上运行。
- 本地**中继服务器**在 loopback 的 `cdpUrl` 上监听（默认：`http://127.0.0.1:18792`）。
- 你点击标签页上的 **OpenClaw Browser Relay** 扩展图标来附加（它不会自动附加）。
- 智能体通过选择正确的配置文件，使用普通的 `browser` 工具控制该标签页。

如果 Gateway 网关在其他地方运行，请在浏览器所在机器上运行节点主机，以便 Gateway 网关可以代理浏览器操作。

### 沙箱会话

如果智能体会话是沙箱隔离的，`browser` 工具可能默认为 `target="sandbox"`（沙箱浏览器）。
Chrome 扩展中继接管需要主机浏览器控制，因此要么：

- 在非沙箱模式下运行会话，或者
- 设置 `agents.defaults.sandbox.browser.allowHostControl: true` 并在调用工具时使用 `target="host"`。

### 设置

1. 加载扩展（开发/未打包）：

```bash
openclaw browser extension install
```

- Chrome → `chrome://extensions` → 启用"开发者模式"
- "加载已解压的扩展程序" → 选择 `openclaw browser extension path` 打印的目录
- 固定扩展，然后在你想要控制的标签页上点击它（徽章显示 `ON`）。

2. 使用它：

- CLI：`openclaw browser --browser-profile chrome tabs`
- 智能体工具：`browser` 配合 `profile="chrome"`

可选：如果你想要不同的名称或中继端口，创建你自己的配置文件：

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

注意事项：

- 此模式依赖 Playwright-on-CDP 进行大多数操作（截图/快照/操作）。
- 再次点击扩展图标可分离。

## 隔离保证

- **专用用户数据目录**：永不触及你的个人浏览器配置文件。
- **专用端口**：避免使用 `9222` 以防止与开发工作流冲突。
- **确定性标签页控制**：通过 `targetId` 定位标签页，而非"最后一个标签页"。

## 浏览器选择

本地启动时，OpenClaw 选择第一个可用的：

1. Chrome
2. Brave
3. Edge
4. Chromium
5. Chrome Canary

你可以使用 `browser.executablePath` 覆盖。

平台：

- macOS：检查 `/Applications` 和 `~/Applications`。
- Linux：查找 `google-chrome`、`brave`、`microsoft-edge`、`chromium` 等。
- Windows：检查常见安装位置。

## 控制 API（可选）

仅用于本地集成，Gateway 网关暴露一个小型的 loopback HTTP API：

- 状态/启动/停止：`GET /`、`POST /start`、`POST /stop`
- 标签页：`GET /tabs`、`POST /tabs/open`、`POST /tabs/focus`、`DELETE /tabs/:targetId`
- 快照/截图：`GET /snapshot`、`POST /screenshot`
- 操作：`POST /navigate`、`POST /act`
- 钩子：`POST /hooks/file-chooser`、`POST /hooks/dialog`
- 下载：`POST /download`、`POST /wait/download`
- 调试：`GET /console`、`POST /pdf`
- 调试：`GET /errors`、`GET /requests`、`POST /trace/start`、`POST /trace/stop`、`POST /highlight`
- 网络：`POST /response/body`
- 状态：`GET /cookies`、`POST /cookies/set`、`POST /cookies/clear`
- 状态：`GET /storage/:kind`、`POST /storage/:kind/set`、`POST /storage/:kind/clear`
- 设置：`POST /set/offline`、`POST /set/headers`、`POST /set/credentials`、`POST /set/geolocation`、`POST /set/media`、`POST /set/timezone`、`POST /set/locale`、`POST /set/device`

所有端点接受 `?profile=<name>`。

### Playwright 要求

某些功能（navigate/act/AI 快照/角色快照、元素截图、PDF）需要 Playwright。如果未安装 Playwright，这些端点会返回明确的 501 错误。ARIA 快照和基本截图对于 openclaw 托管的 Chrome 仍然有效。对于 Chrome 扩展中继驱动程序，ARIA 快照和截图需要 Playwright。

如果你看到 `Playwright is not available in this gateway build`，请安装完整的 Playwright 包（不是 `playwright-core`）并重启 Gateway 网关，或者重新安装带浏览器支持的 OpenClaw。

#### Docker Playwright 安装

如果你的 Gateway 网关在 Docker 中运行，避免使用 `npx playwright`（npm 覆盖冲突）。改用捆绑的 CLI：

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

要持久化浏览器下载，设置 `PLAYWRIGHT_BROWSERS_PATH`（例如 `/home/node/.cache/ms-playwright`）并确保 `/home/node` 通过 `OPENCLAW_HOME_VOLUME` 或绑定挂载持久化。参见 [Docker](/install/docker)。

## 工作原理（内部）

高层流程：

- 一个小型**控制服务器**接受 HTTP 请求。
- 它通过 **CDP** 连接到基于 Chromium 的浏览器（Chrome/Brave/Edge/Chromium）。
- 对于高级操作（点击/输入/快照/PDF），它在 CDP 之上使用 **Playwright**。
- 当缺少 Playwright 时，仅非 Playwright 操作可用。

这种设计使智能体保持在稳定、确定性的接口上，同时让你可以切换本地/远程浏览器和配置文件。

## CLI 快速参考

所有命令接受 `--browser-profile <name>` 以定位特定配置文件。
所有命令也接受 `--json` 以获得机器可读的输出（稳定的负载）。

基础操作：

- `openclaw browser status`
- `openclaw browser start`
- `openclaw browser stop`
- `openclaw browser tabs`
- `openclaw browser tab`
- `openclaw browser tab new`
- `openclaw browser tab select 2`
- `openclaw browser tab close 2`
- `openclaw browser open https://example.com`
- `openclaw browser focus abcd1234`
- `openclaw browser close abcd1234`

检查：

- `openclaw browser screenshot`
- `openclaw browser screenshot --full-page`
- `openclaw browser screenshot --ref 12`
- `openclaw browser screenshot --ref e12`
- `openclaw browser snapshot`
- `openclaw browser snapshot --format aria --limit 200`
- `openclaw browser snapshot --interactive --compact --depth 6`
- `openclaw browser snapshot --efficient`
- `openclaw browser snapshot --labels`
- `openclaw browser snapshot --selector "#main" --interactive`
- `openclaw browser snapshot --frame "iframe#main" --interactive`
- `openclaw browser console --level error`
- `openclaw browser errors --clear`
- `openclaw browser requests --filter api --clear`
- `openclaw browser pdf`
- `openclaw browser responsebody "**/api" --max-chars 5000`

操作：

- `openclaw browser navigate https://example.com`
- `openclaw browser resize 1280 720`
- `openclaw browser click 12 --double`
- `openclaw browser click e12 --double`
- `openclaw browser type 23 "hello" --submit`
- `openclaw browser press Enter`
- `openclaw browser hover 44`
- `openclaw browser scrollintoview e12`
- `openclaw browser drag 10 11`
- `openclaw browser select 9 OptionA OptionB`
- `openclaw browser download e12 /tmp/report.pdf`
- `openclaw browser waitfordownload /tmp/report.pdf`
- `openclaw browser upload /tmp/file.pdf`
- `openclaw browser fill --fields '[{"ref":"1","type":"text","value":"Ada"}]'`
- `openclaw browser dialog --accept`
- `openclaw browser wait --text "Done"`
- `openclaw browser wait "#main" --url "**/dash" --load networkidle --fn "window.ready===true"`
- `openclaw browser evaluate --fn '(el) => el.textContent' --ref 7`
- `openclaw browser highlight e12`
- `openclaw browser trace start`
- `openclaw browser trace stop`

状态：

- `openclaw browser cookies`
- `openclaw browser cookies set session abc123 --url "https://example.com"`
- `openclaw browser cookies clear`
- `openclaw browser storage local get`
- `openclaw browser storage local set theme dark`
- `openclaw browser storage session clear`
- `openclaw browser set offline on`
- `openclaw browser set headers --json '{"X-Debug":"1"}'`
- `openclaw browser set credentials user pass`
- `openclaw browser set credentials --clear`
- `openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"`
- `openclaw browser set geo --clear`
- `openclaw browser set media dark`
- `openclaw browser set timezone America/New_York`
- `openclaw browser set locale en-US`
- `openclaw browser set device "iPhone 14"`

注意事项：

- `upload` 和 `dialog` 是**预备**调用；在触发选择器/对话框的点击/按键之前运行它们。
- `upload` 也可以通过 `--input-ref` 或 `--element` 直接设置文件输入。
- `snapshot`：
  - `--format ai`（安装 Playwright 时的默认值）：返回带有数字 ref 的 AI 快照（`aria-ref="<n>"`）。
  - `--format aria`：返回无障碍树（无 ref；仅供检查）。
  - `--efficient`（或 `--mode efficient`）：紧凑角色快照预设（interactive + compact + depth + 较低的 maxChars）。
  - 配置默认值（仅限工具/CLI）：设置 `browser.snapshotDefaults.mode: "efficient"` 以在调用者未传递模式时使用高效快照（参见 [Gateway 网关配置](/gateway/configuration#browser-openclaw-managed-browser)）。
  - 角色快照选项（`--interactive`、`--compact`、`--depth`、`--selector`）强制使用带有 `ref=e12` 等 ref 的基于角色的快照。
  - `--frame "<iframe selector>"` 将角色快照范围限定到 iframe（与 `e12` 等角色 ref 配合使用）。
  - `--interactive` 输出一个扁平的、易于选择的交互元素列表（最适合驱动操作）。
  - `--labels` 添加一个带有叠加 ref 标签的视口截图（打印 `MEDIA:<path>`）。
- `click`/`type` 等需要来自 `snapshot` 的 `ref`（数字 `12` 或角色 ref `e12`）。
  操作故意不支持 CSS 选择器。

## 快照和 ref

OpenClaw 支持两种"快照"风格：

- **AI 快照（数字 ref）**：`openclaw browser snapshot`（默认；`--format ai`）
  - 输出：包含数字 ref 的文本快照。
  - 操作：`openclaw browser click 12`、`openclaw browser type 23 "hello"`。
  - 内部通过 Playwright 的 `aria-ref` 解析 ref。

- **角色快照（角色 ref 如 `e12`）**：`openclaw browser snapshot --interactive`（或 `--compact`、`--depth`、`--selector`、`--frame`）
  - 输出：带有 `[ref=e12]`（和可选的 `[nth=1]`）的基于角色的列表/树。
  - 操作：`openclaw browser click e12`、`openclaw browser highlight e12`。
  - 内部通过 `getByRole(...)`（加上重复项的 `nth()`）解析 ref。
  - 添加 `--labels` 可包含带有叠加 `e12` 标签的视口截图。

ref 行为：

- ref 在**导航之间不稳定**；如果出错，重新运行 `snapshot` 并使用新的 ref。
- 如果角色快照是使用 `--frame` 拍摄的，角色 ref 将限定在该 iframe 内，直到下一次角色快照。

## 等待增强功能

你可以等待的不仅仅是时间/文本：

- 等待 URL（Playwright 支持通配符）：
  - `openclaw browser wait --url "**/dash"`
- 等待加载状态：
  - `openclaw browser wait --load networkidle`
- 等待 JS 断言：
  - `openclaw browser wait --fn "window.ready===true"`
- 等待选择器变得可见：
  - `openclaw browser wait "#main"`

这些可以组合使用：

```bash
openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --fn "window.ready===true" \
  --timeout-ms 15000
```

## 调试工作流

当操作失败时（例如"not visible"、"strict mode violation"、"covered"）：

1. `openclaw browser snapshot --interactive`
2. 使用 `click <ref>` / `type <ref>`（在交互模式下优先使用角色 ref）
3. 如果仍然失败：`openclaw browser highlight <ref>` 查看 Playwright 定位的目标
4. 如果页面行为异常：
   - `openclaw browser errors --clear`
   - `openclaw browser requests --filter api --clear`
5. 深度调试：录制 trace：
   - `openclaw browser trace start`
   - 重现问题
   - `openclaw browser trace stop`（打印 `TRACE:<path>`）

## JSON 输出

`--json` 用于脚本和结构化工具。

示例：

```bash
openclaw browser status --json
openclaw browser snapshot --interactive --json
openclaw browser requests --filter api --json
openclaw browser cookies --json
```

JSON 格式的角色快照包含 `refs` 加上一个小的 `stats` 块（lines/chars/refs/interactive），以便工具可以推断负载大小和密度。

## 状态和环境开关

这些对于"让网站表现得像 X"的工作流很有用：

- Cookies：`cookies`、`cookies set`、`cookies clear`
- 存储：`storage local|session get|set|clear`
- 离线：`set offline on|off`
- 请求头：`set headers --json '{"X-Debug":"1"}'`（或 `--clear`）
- HTTP basic 认证：`set credentials user pass`（或 `--clear`）
- 地理位置：`set geo <lat> <lon> --origin "https://example.com"`（或 `--clear`）
- 媒体：`set media dark|light|no-preference|none`
- 时区/语言环境：`set timezone ...`、`set locale ...`
- 设备/视口：
  - `set device "iPhone 14"`（Playwright 设备预设）
  - `set viewport 1280 720`

## 安全与隐私

- openclaw 浏览器配置文件可能包含已登录的会话；请将其视为敏感信息。
- `browser act kind=evaluate` / `openclaw browser evaluate` 和 `wait --fn` 在页面上下文中执行任意 JavaScript。提示注入可能会操纵它。如果不需要，请使用 `browser.evaluateEnabled=false` 禁用它。
- 有关登录和反机器人注意事项（X/Twitter 等），请参阅 [浏览器登录 + X/Twitter 发帖](/tools/browser-login)。
- 保持 Gateway 网关/节点主机私有（仅限 loopback 或 tailnet）。
- 远程 CDP 端点功能强大；请通过隧道保护它们。

## 故障排除

有关 Linux 特定问题（特别是 snap Chromium），请参阅[浏览器故障排除](/tools/browser-linux-troubleshooting)。

## 智能体工具 + 控制工作原理

智能体获得**一个工具**用于浏览器自动化：

- `browser` — status/start/stop/tabs/open/focus/close/snapshot/screenshot/navigate/act

映射方式：

- `browser snapshot` 返回稳定的 UI 树（AI 或 ARIA）。
- `browser act` 使用快照 `ref` ID 来点击/输入/拖动/选择。
- `browser screenshot` 捕获像素（整页或元素）。
- `browser` 接受：
  - `profile` 来选择命名的浏览器配置文件（openclaw、chrome 或远程 CDP）。
  - `target`（`sandbox` | `host` | `node`）来选择浏览器所在位置。
  - 在沙箱会话中，`target: "host"` 需要 `agents.defaults.sandbox.browser.allowHostControl=true`。
  - 如果省略 `target`：沙箱会话默认为 `sandbox`，非沙箱会话默认为 `host`。
  - 如果连接了具有浏览器能力的节点，工具可能会自动路由到该节点，除非你指定 `target="host"` 或 `target="node"`。

这使智能体保持确定性并避免脆弱的选择器。


---
# File: docs/zh-CN/tools/chrome-extension.md

---
read_when:
  - 你希望智能体驱动现有的 Chrome 标签页（工具栏按钮）
  - 你需要通过 Tailscale 实现远程 Gateway 网关 + 本地浏览器自动化
  - 你想了解浏览器接管的安全影响
summary: Chrome 扩展：让 OpenClaw 驱动你现有的 Chrome 标签页
title: Chrome 扩展
x-i18n:
  generated_at: "2026-02-03T07:55:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3b77bdad7d3dab6adb76ff25b144412d6b54b915993b1c1f057f36dea149938b
  source_path: tools/chrome-extension.md
  workflow: 15
---

# Chrome 扩展（浏览器中继）

OpenClaw Chrome 扩展让智能体控制你**现有的 Chrome 标签页**（你的正常 Chrome 窗口），而不是启动一个单独的 openclaw 管理的 Chrome 配置文件。

附加/分离通过一个**单独的 Chrome 工具栏按钮**实现。

## 它是什么（概念）

有三个部分：

- **浏览器控制服务**（Gateway 网关或节点）：智能体/工具调用的 API（通过 Gateway 网关）
- **本地中继服务器**（loopback CDP）：在控制服务器和扩展之间桥接（默认 `http://127.0.0.1:18792`）
- **Chrome MV3 扩展**：使用 `chrome.debugger` 附加到活动标签页，并将 CDP 消息传送到中继

然后 OpenClaw 通过正常的 `browser` 工具界面控制附加的标签页（选择正确的配置文件）。

## 安装/加载（未打包）

1. 将扩展安装到稳定的本地路径：

```bash
openclaw browser extension install
```

2. 打印已安装扩展的目录路径：

```bash
openclaw browser extension path
```

3. Chrome → `chrome://extensions`

- 启用"开发者模式"
- "加载已解压的扩展程序" → 选择上面打印的目录

4. 固定扩展。

## 更新（无构建步骤）

扩展作为静态文件包含在 OpenClaw 发布版（npm 包）中。没有单独的"构建"步骤。

升级 OpenClaw 后：

- 重新运行 `openclaw browser extension install` 以刷新 OpenClaw 状态目录下的已安装文件。
- Chrome → `chrome://extensions` → 点击扩展上的"重新加载"。

## 使用它（无需额外配置）

OpenClaw 附带一个名为 `chrome` 的内置浏览器配置文件，它指向默认端口上的扩展中继。

使用它：

- CLI：`openclaw browser --browser-profile chrome tabs`
- 智能体工具：`browser` 配合 `profile="chrome"`

如果你想要不同的名称或不同的中继端口，创建你自己的配置文件：

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

## 附加/分离（工具栏按钮）

- 打开你希望 OpenClaw 控制的标签页。
- 点击扩展图标。
  - 附加时徽章显示 `ON`。
- 再次点击以分离。

## 它控制哪个标签页？

- 它**不会**自动控制"你正在查看的任何标签页"。
- 它**仅**控制你通过点击工具栏按钮**明确附加的标签页**。
- 要切换：打开另一个标签页并在那里点击扩展图标。

## 徽章 + 常见错误

- `ON`：已附加；OpenClaw 可以驱动该标签页。
- `…`：正在连接到本地中继。
- `!`：中继不可达（最常见：浏览器中继服务器未在此机器上运行）。

如果你看到 `!`：

- 确保 Gateway 网关在本地运行（默认设置），或者如果 Gateway 网关在其他地方运行，在此机器上运行一个节点主机。
- 打开扩展选项页面；它会显示中继是否可达。

## 远程 Gateway 网关（使用节点主机）

### 本地 Gateway 网关（与 Chrome 在同一台机器上）——通常**无需额外步骤**

如果 Gateway 网关运行在与 Chrome 相同的机器上，它会在 loopback 上启动浏览器控制服务并自动启动中继服务器。扩展与本地中继通信；CLI/工具调用发送到 Gateway 网关。

### 远程 Gateway 网关（Gateway 网关运行在其他地方）——**运行节点主机**

如果你的 Gateway 网关运行在另一台机器上，在运行 Chrome 的机器上启动一个节点主机。Gateway 网关将把浏览器操作代理到该节点；扩展 + 中继保持在浏览器机器本地。

如果连接了多个节点，使用 `gateway.nodes.browser.node` 固定一个或设置 `gateway.nodes.browser.mode`。

## 沙箱隔离（工具容器）

如果你的智能体会话在沙箱中（`agents.defaults.sandbox.mode != "off"`），`browser` 工具可能受到限制：

- 默认情况下，沙箱隔离的会话通常指向**沙箱浏览器**（`target="sandbox"`），而不是你的主机 Chrome。
- Chrome 扩展中继接管需要控制**主机**浏览器控制服务器。

选项：

- 最简单：从**非沙箱隔离**的会话/智能体使用扩展。
- 或者为沙箱隔离的会话允许主机浏览器控制：

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

然后确保工具未被工具策略拒绝，并（如果需要）以 `target="host"` 调用 `browser`。

调试：`openclaw sandbox explain`

## 远程访问提示

- 将 Gateway 网关和节点主机保持在同一个 tailnet 上；避免将中继端口暴露到 LAN 或公共 Internet。
- 有意配对节点；如果你不想要远程控制，禁用浏览器代理路由（`gateway.nodes.browser.mode="off"`）。

## "extension path"的工作原理

`openclaw browser extension path` 打印包含扩展文件的**已安装**磁盘目录。

CLI 有意**不**打印 `node_modules` 路径。始终先运行 `openclaw browser extension install` 将扩展复制到 OpenClaw 状态目录下的稳定位置。

如果你移动或删除该安装目录，Chrome 将把扩展标记为损坏，直到你从有效路径重新加载它。

## 安全影响（请阅读此内容）

这是强大且有风险的。将其视为给模型"在你的浏览器上动手"。

- 扩展使用 Chrome 的调试器 API（`chrome.debugger`）。附加时，模型可以：
  - 在该标签页中点击/输入/导航
  - 读取页面内容
  - 访问标签页已登录会话可以访问的任何内容
- **这不像**专用的 openclaw 管理配置文件那样隔离。
  - 如果你附加到你的日常使用配置文件/标签页，你就是在授予对该账户状态的访问权限。

建议：

- 对于扩展中继使用，优先使用专用的 Chrome 配置文件（与你的个人浏览分开）。
- 将 Gateway 网关和任何节点主机保持在仅限 tailnet；依赖 Gateway 网关身份验证 + 节点配对。
- 避免通过 LAN（`0.0.0.0`）暴露中继端口，避免使用 Funnel（公开）。
- 中继阻止非扩展来源，并要求 CDP 客户端提供内部身份验证令牌。

相关：

- 浏览器工具概述：[浏览器](/tools/browser)
- 安全审计：[安全](/gateway/security)
- Tailscale 设置：[Tailscale](/gateway/tailscale)


---
# File: docs/zh-CN/tools/clawhub.md

---
read_when:
  - 向新用户介绍 ClawHub
  - 安装、搜索或发布 Skills
  - 说明 ClawHub CLI 标志和同步行为
summary: ClawHub 指南：公共 Skills 注册中心 + CLI 工作流
title: ClawHub
x-i18n:
  generated_at: "2026-02-01T21:42:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8b7f8fab80a34e409f37fa130a49ff5b487966755a7b0d214dfebf5207c7124c
  source_path: tools/clawhub.md
  workflow: 15
---

# ClawHub

ClawHub 是 **OpenClaw 的公共 Skills 注册中心**。它是一项免费服务：所有 Skills 都是公开的、开放的，所有人都可以查看、共享和复用。Skills 就是一个包含 `SKILL.md` 文件（以及辅助文本文件）的文件夹。你可以在网页应用中浏览 Skills，也可以使用 CLI 来搜索、安装、更新和发布 Skills。

网站：[clawhub.com](https://clawhub.com)

## 适用人群（新手友好）

如果你想为 OpenClaw 智能体添加新功能，ClawHub 是查找和安装 Skills 的最简单方式。你不需要了解后端的工作原理。你可以：

- 使用自然语言搜索 Skills。
- 将 Skills 安装到你的工作区。
- 之后使用一条命令更新 Skills。
- 通过发布 Skills 来备份你自己的 Skills。

## 快速入门（非技术人员）

1. 安装 CLI（参见下一节）。
2. 搜索你需要的内容：
   - `clawhub search "calendar"`
3. 安装一个 Skills：
   - `clawhub install <skill-slug>`
4. 启动一个新的 OpenClaw 会话，以加载新 Skills。

## 安装 CLI

任选其一：

```bash
npm i -g clawhub
```

```bash
pnpm add -g clawhub
```

## 在 OpenClaw 中的定位

默认情况下，CLI 会将 Skills 安装到当前工作目录下的 `./skills`。如果已配置 OpenClaw 工作区，`clawhub` 会回退到该工作区，除非你通过 `--workdir`（或 `CLAWHUB_WORKDIR`）进行覆盖。OpenClaw 从 `<workspace>/skills` 加载工作区 Skills，并会在**下一个**会话中生效。如果你已经在使用 `~/.openclaw/skills` 或内置 Skills，工作区 Skills 优先级更高。

有关 Skills 加载、共享和权限控制的更多详情，请参阅
[Skills](/tools/skills)。

## 服务功能

- **公开浏览**Skills 及其 `SKILL.md` 内容。
- 基于嵌入向量（向量搜索）的**搜索**，而不仅仅是关键词匹配。
- 支持语义化版本号、变更日志和标签（包括 `latest`）的**版本管理**。
- 每个版本以 zip 格式**下载**。
- **星标和评论**，支持社区反馈。
- **审核**钩子，用于审批和审计。
- **CLI 友好的 API**，支持自动化和脚本编写。

## CLI 命令和参数

全局选项（适用于所有命令）：

- `--workdir <dir>`：工作目录（默认：当前目录；回退到 OpenClaw 工作区）。
- `--dir <dir>`：Skills 目录，相对于工作目录（默认：`skills`）。
- `--site <url>`：网站基础 URL（浏览器登录）。
- `--registry <url>`：注册中心 API 基础 URL。
- `--no-input`：禁用提示（非交互模式）。
- `-V, --cli-version`：打印 CLI 版本。

认证：

- `clawhub login`（浏览器流程）或 `clawhub login --token <token>`
- `clawhub logout`
- `clawhub whoami`

选项：

- `--token <token>`：粘贴 API 令牌。
- `--label <label>`：为浏览器登录令牌存储的标签（默认：`CLI token`）。
- `--no-browser`：不打开浏览器（需要 `--token`）。

搜索：

- `clawhub search "query"`
- `--limit <n>`：最大结果数。

安装：

- `clawhub install <slug>`
- `--version <version>`：安装指定版本。
- `--force`：如果文件夹已存在则覆盖。

更新：

- `clawhub update <slug>`
- `clawhub update --all`
- `--version <version>`：更新到指定版本（仅限单个 slug）。
- `--force`：当本地文件与任何已发布版本不匹配时强制覆盖。

列表：

- `clawhub list`（读取 `.clawhub/lock.json`）

发布：

- `clawhub publish <path>`
- `--slug <slug>`：Skills 标识符。
- `--name <name>`：显示名称。
- `--version <version>`：语义化版本号。
- `--changelog <text>`：变更日志文本（可以为空）。
- `--tags <tags>`：逗号分隔的标签（默认：`latest`）。

删除/恢复（仅所有者/管理员）：

- `clawhub delete <slug> --yes`
- `clawhub undelete <slug> --yes`

同步（扫描本地 Skills + 发布新增/更新的 Skills）：

- `clawhub sync`
- `--root <dir...>`：额外的扫描根目录。
- `--all`：无提示上传所有内容。
- `--dry-run`：显示将要上传的内容。
- `--bump <type>`：更新的版本号递增类型 `patch|minor|major`（默认：`patch`）。
- `--changelog <text>`：非交互更新的变更日志。
- `--tags <tags>`：逗号分隔的标签（默认：`latest`）。
- `--concurrency <n>`：注册中心检查并发数（默认：4）。

## 智能体常用工作流

### 搜索 Skills

```bash
clawhub search "postgres backups"
```

### 下载新 Skills

```bash
clawhub install my-skill-pack
```

### 更新已安装的 Skills

```bash
clawhub update --all
```

### 备份你的 Skills（发布或同步）

对于单个 Skills 文件夹：

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

一次扫描并备份多个 Skills：

```bash
clawhub sync --all
```

## 高级详情（技术性）

### 版本管理和标签

- 每次发布都会创建一个新的**语义化版本** `SkillVersion`。
- 标签（如 `latest`）指向某个版本；移动标签可以实现回滚。
- 变更日志附加在每个版本上，在同步或发布更新时可以为空。

### 本地更改与注册中心版本

更新时会使用内容哈希将本地 Skills 内容与注册中心版本进行比较。如果本地文件与任何已发布版本不匹配，CLI 会在覆盖前询问确认（或在非交互模式下需要 `--force`）。

### 同步扫描和回退根目录

`clawhub sync` 首先扫描当前工作目录。如果未找到 Skills，它会回退到已知的旧版位置（例如 `~/openclaw/skills` 和 `~/.openclaw/skills`）。这样设计是为了在不需要额外标志的情况下找到旧版 Skills 安装。

### 存储和锁文件

- 已安装的 Skills 记录在工作目录下的 `.clawhub/lock.json` 中。
- 认证令牌存储在 ClawHub CLI 配置文件中（可通过 `CLAWHUB_CONFIG_PATH` 覆盖）。

### 遥测（安装计数）

当你在登录状态下运行 `clawhub sync` 时，CLI 会发送一个最小快照用于计算安装次数。你可以完全禁用此功能：

```bash
export CLAWHUB_DISABLE_TELEMETRY=1
```

## 环境变量

- `CLAWHUB_SITE`：覆盖网站 URL。
- `CLAWHUB_REGISTRY`：覆盖注册中心 API URL。
- `CLAWHUB_CONFIG_PATH`：覆盖 CLI 存储令牌/配置的位置。
- `CLAWHUB_WORKDIR`：覆盖默认工作目录。
- `CLAWHUB_DISABLE_TELEMETRY=1`：禁用 `sync` 的遥测功能。


---
# File: docs/zh-CN/tools/creating-skills.md

---
title: 创建 Skills
x-i18n:
  generated_at: "2026-02-03T10:10:19Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ad801da34fe361ffa584ded47f775d1c104a471a3f7b7f930652255e98945c3a
  source_path: tools/creating-skills.md
  workflow: 15
---

# 创建自定义 Skills 🛠

OpenClaw 被设计为易于扩展。"Skills"是为你的助手添加新功能的主要方式。

## 什么是 Skill？

Skill 是一个包含 `SKILL.md` 文件（为 LLM 提供指令和工具定义）的目录，可选包含一些脚本或资源。

## 分步指南：你的第一个 Skill

### 1. 创建目录

Skills 位于你的工作区中，通常是 `~/.openclaw/workspace/skills/`。为你的 Skill 创建一个新文件夹：

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

### 2. 定义 `SKILL.md`

在该目录中创建一个 `SKILL.md` 文件。此文件使用 YAML frontmatter 作为元数据，使用 Markdown 作为指令。

```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

### 3. 添加工具（可选）

你可以在 frontmatter 中定义自定义工具，或指示智能体使用现有的系统工具（如 `bash` 或 `browser`）。

### 4. 刷新 OpenClaw

让你的智能体"刷新 skills"或重启 Gateway 网关。OpenClaw 将发现新目录并索引 `SKILL.md`。

## 最佳实践

- **简洁明了**：指示模型*做什么*，而不是如何成为一个 AI。
- **安全第一**：如果你的 Skill 使用 `bash`，确保提示词不允许来自不受信任用户输入的任意命令注入。
- **本地测试**：使用 `openclaw agent --message "use my new skill"` 进行测试。

## 共享 Skills

你也可以在 [ClawHub](https://clawhub.com) 上浏览和贡献 Skills。


---
# File: docs/zh-CN/tools/elevated.md

---
read_when:
  - 调整提升模式默认值、允许列表或斜杠命令行为
summary: 提升的 exec 模式和 /elevated 指令
title: 提升模式
x-i18n:
  generated_at: "2026-02-03T07:55:23Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 83767a01609304026d145feb0aa0b0533e8cf8b16cd200f724d9e3e8cf2920c3
  source_path: tools/elevated.md
  workflow: 15
---

# 提升模式（/elevated 指令）

## 功能说明

- `/elevated on` 在 Gateway 网关主机上运行并保留 exec 审批（与 `/elevated ask` 相同）。
- `/elevated full` 在 Gateway 网关主机上运行**并**自动批准 exec（跳过 exec 审批）。
- `/elevated ask` 在 Gateway 网关主机上运行但保留 exec 审批（与 `/elevated on` 相同）。
- `on`/`ask` **不会**强制 `exec.security=full`；配置的安全/询问策略仍然适用。
- 仅在智能体被**沙箱隔离**时改变行为（否则 exec 已经在主机上运行）。
- 指令形式：`/elevated on|off|ask|full`、`/elev on|off|ask|full`。
- 仅接受 `on|off|ask|full`；其他任何内容返回提示且不改变状态。

## 它控制什么（以及不控制什么）

- **可用性门控**：`tools.elevated` 是全局基线。`agents.list[].tools.elevated` 可以进一步限制每个智能体的提升（两者都必须允许）。
- **每会话状态**：`/elevated on|off|ask|full` 为当前会话键设置提升级别。
- **内联指令**：消息内的 `/elevated on|ask|full` 仅适用于该消息。
- **群组**：在群聊中，仅当智能体被提及时才遵守提升指令。绕过提及要求的纯命令消息被视为已提及。
- **主机执行**：elevated 强制 `exec` 到 Gateway 网关主机；`full` 还设置 `security=full`。
- **审批**：`full` 跳过 exec 审批；`on`/`ask` 在允许列表/询问规则要求时遵守审批。
- **非沙箱隔离智能体**：对位置无影响；仅影响门控、日志和状态。
- **工具策略仍然适用**：如果 `exec` 被工具策略拒绝，则无法使用 elevated。
- **与 `/exec` 分开**：`/exec` 为授权发送者调整每会话默认值，不需要 elevated。

## 解析顺序

1. 消息上的内联指令（仅适用于该消息）。
2. 会话覆盖（通过发送仅含指令的消息设置）。
3. 全局默认值（配置中的 `agents.defaults.elevatedDefault`）。

## 设置会话默认值

- 发送一条**仅**包含指令的消息（允许空白），例如 `/elevated full`。
- 发送确认回复（`Elevated mode set to full...` / `Elevated mode disabled.`）。
- 如果 elevated 访问被禁用或发送者不在批准的允许列表中，指令会回复一个可操作的错误且不改变会话状态。
- 发送不带参数的 `/elevated`（或 `/elevated:`）以查看当前的 elevated 级别。

## 可用性 + 允许列表

- 功能门控：`tools.elevated.enabled`（即使代码支持，也可以通过配置将默认值设为关闭）。
- 发送者允许列表：`tools.elevated.allowFrom`，带有每提供商允许列表（例如 `discord`、`whatsapp`）。
- 每智能体门控：`agents.list[].tools.elevated.enabled`（可选；只能进一步限制）。
- 每智能体允许列表：`agents.list[].tools.elevated.allowFrom`（可选；设置时，发送者必须同时匹配全局 + 每智能体允许列表）。
- Discord 回退：如果省略 `tools.elevated.allowFrom.discord`，则使用 `channels.discord.dm.allowFrom` 列表作为回退。设置 `tools.elevated.allowFrom.discord`（即使是 `[]`）以覆盖。每智能体允许列表**不**使用回退。
- 所有门控都必须通过；否则 elevated 被视为不可用。

## 日志 + 状态

- Elevated exec 调用以 info 级别记录。
- 会话状态包括 elevated 模式（例如 `elevated=ask`、`elevated=full`）。


---
# File: docs/zh-CN/tools/exec-approvals.md

---
read_when:
  - 配置执行审批或允许列表
  - 在 macOS 应用中实现执行审批用户体验
  - 审查沙箱逃逸提示及其影响
summary: 执行审批、允许列表和沙箱逃逸提示
title: 执行审批
x-i18n:
  generated_at: "2026-02-03T08:19:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 97736427752eb905bb5d1f5b54bddbdea38eb5ac5824e2bf99258fcf44ee393c
  source_path: tools/exec-approvals.md
  workflow: 15
---

# 执行审批

执行审批是**配套应用/节点主机的安全护栏**，用于允许沙箱隔离的智能体在真实主机（`gateway` 或 `node`）上运行命令。可以将其理解为安全联锁：只有当策略 + 允许列表 +（可选的）用户审批都同意时，命令才会被允许执行。
执行审批是**附加于**工具策略和提权门控之上的（除非 elevated 设置为 `full`，这会跳过审批）。
生效策略取 `tools.exec.*` 和审批默认值中**更严格**的一方；如果审批字段被省略，则使用 `tools.exec` 的值。

如果配套应用 UI **不可用**，任何需要提示的请求都将由 **ask fallback**（默认：deny）决定。

## 适用范围

执行审批在执行主机上本地强制执行：

- **gateway 主机** → gateway 机器上的 `openclaw` 进程
- **node 主机** → 节点运行器（macOS 配套应用或无头节点主机）

macOS 分工：

- **node 主机服务**通过本地 IPC 将 `system.run` 转发给 **macOS 应用**。
- **macOS 应用**执行审批并在 UI 上下文中执行命令。

## 设置和存储

审批信息存储在执行主机上的本地 JSON 文件中：

`~/.openclaw/exec-approvals.json`

示例结构：

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

## 策略选项

### Security（`exec.security`）

- **deny**：阻止所有主机执行请求。
- **allowlist**：仅允许在允许列表中的命令。
- **full**：允许所有命令（等同于提权模式）。

### Ask（`exec.ask`）

- **off**：从不提示。
- **on-miss**：仅在允许列表未匹配时提示。
- **always**：每次命令都提示。

### Ask fallback（`askFallback`）

如果需要提示但无法访问 UI，fallback 决定：

- **deny**：阻止。
- **allowlist**：仅在允许列表匹配时允许。
- **full**：允许。

## 允许列表（按智能体）

允许列表是**按智能体**配置的。如果存在多个智能体，请在 macOS 应用中切换要编辑的智能体。模式匹配**不区分大小写**。
模式应解析为**二进制路径**（仅包含基本名称的条目会被忽略）。
旧版 `agents.default` 条目在加载时会迁移到 `agents.main`。

示例：

- `~/Projects/**/bin/bird`
- `~/.local/bin/*`
- `/opt/homebrew/bin/rg`

每个允许列表条目会跟踪：

- **id** 用于 UI 标识的稳定 UUID（可选）
- **last used** 时间戳
- **last used command**
- **last resolved path**

## 自动允许 skill CLI

启用 **Auto-allow skill CLIs** 后，已知 Skills 引用的可执行文件在节点（macOS 节点或无头节点主机）上被视为已列入允许列表。这通过 Gateway RPC 的 `skills.bins` 获取 skill 二进制列表。如果你想要严格的手动允许列表，请禁用此选项。

## 安全二进制（仅限标准输入）

`tools.exec.safeBins` 定义了一小组**仅限标准输入**的二进制文件（例如 `jq`），这些文件可以在允许列表模式下运行，**无需**显式的允许列表条目。安全二进制会拒绝位置文件参数和类路径标记，因此它们只能操作传入的流。
在允许列表模式下，shell 链式命令和重定向不会被自动允许。

当每个顶级段都满足允许列表（包括安全二进制或 skill 自动允许）时，允许 shell 链式命令（`&&`、`||`、`;`）。重定向在允许列表模式下仍不受支持。
命令替换（`$()` / 反引号）在允许列表解析期间会被拒绝，包括在双引号内；如果你需要字面的 `$()` 文本，请使用单引号。

默认安全二进制：`jq`、`grep`、`cut`、`sort`、`uniq`、`head`、`tail`、`tr`、`wc`。

## Control UI 编辑

使用 **Control UI → Nodes → Exec approvals** 卡片来编辑默认值、按智能体的覆盖设置和允许列表。选择一个作用域（Defaults 或某个智能体），调整策略，添加/删除允许列表模式，然后点击 **Save**。UI 会显示每个模式的 **last used** 元数据，以便你保持列表整洁。

目标选择器可选择 **Gateway**（本地审批）或 **Node**。节点必须通告 `system.execApprovals.get/set`（macOS 应用或无头节点主机）。
如果节点尚未通告执行审批，请直接编辑其本地的 `~/.openclaw/exec-approvals.json`。

CLI：`openclaw approvals` 支持 gateway 或 node 编辑（参见 [Approvals CLI](/cli/approvals)）。

## 审批流程

当需要提示时，gateway 向操作员客户端广播 `exec.approval.requested`。
Control UI 和 macOS 应用通过 `exec.approval.resolve` 进行处理，然后 gateway 将已批准的请求转发给节点主机。

当需要审批时，exec 工具会立即返回一个审批 id。使用该 id 来关联后续的系统事件（`Exec finished` / `Exec denied`）。如果在超时前没有收到决定，请求将被视为审批超时，并作为拒绝原因显示。

确认对话框包括：

- 命令 + 参数
- cwd
- 智能体 id
- 解析后的可执行文件路径
- 主机 + 策略元数据

操作：

- **Allow once** → 立即运行
- **Always allow** → 添加到允许列表 + 运行
- **Deny** → 阻止

## 审批转发到聊天渠道

你可以将执行审批提示转发到任何聊天渠道（包括插件渠道），并使用 `/approve` 进行批准。这使用正常的出站投递管道。

配置：

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring or regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

在聊天中回复：

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

### macOS IPC 流程

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

安全注意事项：

- Unix socket 模式 `0600`，token 存储在 `exec-approvals.json` 中。
- 同 UID 对端检查。
- 挑战/响应（nonce + HMAC token + 请求哈希）+ 短 TTL。

## 系统事件

执行生命周期以系统消息的形式呈现：

- `Exec running`（仅当命令超过运行通知阈值时）
- `Exec finished`
- `Exec denied`

这些消息在节点报告事件后发布到智能体的会话中。
Gateway 主机执行审批在命令完成时（以及可选地在运行时间超过阈值时）发出相同的生命周期事件。
经过审批门控的执行会复用审批 id 作为这些消息中的 `runId`，以便于关联。

## 影响

- **full** 权限很大；尽可能优先使用允许列表。
- **ask** 让你保持知情，同时仍允许快速审批。
- 按智能体的允许列表可防止一个智能体的审批泄漏到其他智能体。
- 审批仅适用于来自**授权发送者**的主机执行请求。未授权的发送者无法发出 `/exec`。
- `/exec security=full` 是为授权操作员提供的会话级便利功能，设计上会跳过审批。
  要完全阻止主机执行，请将审批 security 设置为 `deny`，或通过工具策略拒绝 `exec` 工具。

相关内容：

- [Exec 工具](/tools/exec)
- [提权模式](/tools/elevated)
- [Skills](/tools/skills)


---
# File: docs/zh-CN/tools/exec.md

---
read_when:
  - 使用或修改 exec 工具
  - 调试 stdin 或 TTY 行为
summary: Exec 工具用法、stdin 模式和 TTY 支持
title: Exec 工具
x-i18n:
  generated_at: "2026-02-03T09:26:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3b32238dd8dce93d4f24100eaa521ce9f8485eff6d8498e2680ce9ed6045d25f
  source_path: tools/exec.md
  workflow: 15
---

# Exec 工具

在工作区中运行 shell 命令。通过 `process` 支持前台和后台执行。
如果 `process` 被禁用，`exec` 将同步运行并忽略 `yieldMs`/`background`。
后台会话按智能体隔离；`process` 只能看到同一智能体的会话。

## 参数

- `command`（必填）
- `workdir`（默认为当前工作目录）
- `env`（键值对覆盖）
- `yieldMs`（默认 10000）：延迟后自动转入后台
- `background`（布尔值）：立即转入后台
- `timeout`（秒，默认 1800）：超时后终止
- `pty`（布尔值）：在可用时使用伪终端运行（仅限 TTY 的 CLI、编程智能体、终端 UI）
- `host`（`sandbox | gateway | node`）：执行位置
- `security`（`deny | allowlist | full`）：`gateway`/`node` 的执行策略
- `ask`（`off | on-miss | always`）：`gateway`/`node` 的审批提示
- `node`（字符串）：`host=node` 时的节点 id/名称
- `elevated`（布尔值）：请求提升模式（gateway 主机）；仅当 elevated 解析为 `full` 时才强制 `security=full`

注意事项：

- `host` 默认为 `sandbox`。
- 当沙箱隔离关闭时，`elevated` 会被忽略（exec 已在主机上运行）。
- `gateway`/`node` 审批由 `~/.openclaw/exec-approvals.json` 控制。
- `node` 需要已配对的节点（配套应用或无头节点主机）。
- 如果有多个可用节点，设置 `exec.node` 或 `tools.exec.node` 来选择一个。
- 在非 Windows 主机上，exec 会使用已设置的 `SHELL`；如果 `SHELL` 是 `fish`，它会优先从 `PATH` 中选择 `bash`（或 `sh`）以避免 fish 不兼容的脚本，如果两者都不存在则回退到 `SHELL`。
- 主机执行（`gateway`/`node`）会拒绝 `env.PATH` 和加载器覆盖（`LD_*`/`DYLD_*`），以防止二进制劫持或代码注入。
- 重要提示：沙箱隔离**默认关闭**。如果沙箱隔离关闭，`host=sandbox` 将直接在 Gateway 网关主机上运行（无容器）且**不需要审批**。如需审批，请使用 `host=gateway` 运行并配置 exec 审批（或启用沙箱隔离）。

## 配置

- `tools.exec.notifyOnExit`（默认：true）：为 true 时，后台 exec 会话在退出时会入队系统事件并请求心跳。
- `tools.exec.approvalRunningNoticeMs`（默认：10000）：当需要审批的 exec 运行时间超过此值时发出单次"运行中"通知（0 表示禁用）。
- `tools.exec.host`（默认：`sandbox`）
- `tools.exec.security`（默认：sandbox 为 `deny`，gateway + node 未设置时为 `allowlist`）
- `tools.exec.ask`（默认：`on-miss`）
- `tools.exec.node`（默认：未设置）
- `tools.exec.pathPrepend`：exec 运行时添加到 `PATH` 前面的目录列表。
- `tools.exec.safeBins`：仅限 stdin 的安全二进制文件，无需显式白名单条目即可运行。

示例：

```json5
{
  tools: {
    exec: {
      pathPrepend: ["~/bin", "/opt/oss/bin"],
    },
  },
}
```

### PATH 处理

- `host=gateway`：将你的登录 shell `PATH` 合并到 exec 环境中。主机执行时会拒绝 `env.PATH` 覆盖。守护进程本身仍使用最小 `PATH` 运行：
  - macOS：`/opt/homebrew/bin`、`/usr/local/bin`、`/usr/bin`、`/bin`
  - Linux：`/usr/local/bin`、`/usr/bin`、`/bin`
- `host=sandbox`：在容器内运行 `sh -lc`（登录 shell），因此 `/etc/profile` 可能会重置 `PATH`。OpenClaw 在 profile 加载后通过内部环境变量将 `env.PATH` 添加到前面（无 shell 插值）；`tools.exec.pathPrepend` 在此也适用。
- `host=node`：只有你传递的未被阻止的 env 覆盖会发送到节点。主机执行时会拒绝 `env.PATH` 覆盖。无头节点主机仅在 `PATH` 添加到节点主机 PATH 前面时才接受（不允许替换）。macOS 节点完全丢弃 `PATH` 覆盖。

按智能体绑定节点（在配置中使用智能体列表索引）：

```bash
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

控制 UI：Nodes 标签页包含一个小的"Exec 节点绑定"面板用于相同的设置。

## 会话覆盖（`/exec`）

使用 `/exec` 为 `host`、`security`、`ask` 和 `node` 设置**每会话**默认值。
不带参数发送 `/exec` 可显示当前值。

示例：

```
/exec host=gateway security=allowlist ask=on-miss node=mac-1
```

## 授权模型

`/exec` 仅对**已授权发送者**（渠道白名单/配对加 `commands.useAccessGroups`）生效。
它仅更新**会话状态**，不写入配置。要彻底禁用 exec，请通过工具策略拒绝它（`tools.deny: ["exec"]` 或按智能体配置）。除非你显式设置 `security=full` 和 `ask=off`，否则主机审批仍然适用。

## Exec 审批（配套应用/节点主机）

沙箱隔离的智能体可以要求在 `exec` 于 Gateway 网关或节点主机上运行前进行逐请求审批。
参阅 [Exec 审批](/tools/exec-approvals) 了解策略、白名单和 UI 流程。

当需要审批时，exec 工具会立即返回 `status: "approval-pending"` 和审批 id。一旦被批准（或拒绝/超时），Gateway 网关会发出系统事件（`Exec finished` / `Exec denied`）。如果命令在 `tools.exec.approvalRunningNoticeMs` 之后仍在运行，会发出单次 `Exec running` 通知。

## 白名单 + 安全二进制文件

白名单执行仅匹配**解析后的二进制路径**（不匹配基本名称）。当 `security=allowlist` 时，仅当每个管道段都在白名单中或是安全二进制文件时，shell 命令才会自动允许。在白名单模式下，链式命令（`;`、`&&`、`||`）和重定向会被拒绝。

## 示例

前台：

```json
{ "tool": "exec", "command": "ls -la" }
```

后台 + 轮询：

```json
{"tool":"exec","command":"npm run build","yieldMs":1000}
{"tool":"process","action":"poll","sessionId":"<id>"}
```

发送按键（tmux 风格）：

```json
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Enter"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["C-c"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Up","Up","Enter"]}
```

提交（仅发送 CR）：

```json
{ "tool": "process", "action": "submit", "sessionId": "<id>" }
```

粘贴（默认带括号）：

```json
{ "tool": "process", "action": "paste", "sessionId": "<id>", "text": "line1\nline2\n" }
```

## apply_patch（实验性）

`apply_patch` 是 `exec` 的子工具，用于结构化多文件编辑。
需显式启用：

```json5
{
  tools: {
    exec: {
      applyPatch: { enabled: true, allowModels: ["gpt-5.2"] },
    },
  },
}
```

注意事项：

- 仅适用于 OpenAI/OpenAI Codex 模型。
- 工具策略仍然适用；`allow: ["exec"]` 隐式允许 `apply_patch`。
- 配置位于 `tools.exec.applyPatch` 下。


---
# File: docs/zh-CN/tools/firecrawl.md

---
read_when:
  - 你想要 Firecrawl 支持的网页提取
  - 你需要 Firecrawl API 密钥
  - 你想要 web_fetch 的反机器人提取
summary: 用于 web_fetch 的 Firecrawl 回退（反机器人 + 缓存提取）
title: Firecrawl
x-i18n:
  generated_at: "2026-02-03T10:10:35Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 08a7ad45b41af41204e44d2b0be0f980b7184d80d2fa3977339e42a47beb2851
  source_path: tools/firecrawl.md
  workflow: 15
---

# Firecrawl

OpenClaw 可以使用 **Firecrawl** 作为 `web_fetch` 的回退提取器。它是一个托管的
内容提取服务，支持机器人规避和缓存，有助于处理
JS 密集型网站或阻止普通 HTTP 请求的页面。

## 获取 API 密钥

1. 创建 Firecrawl 账户并生成 API 密钥。
2. 将其存储在配置中或在 Gateway 网关环境中设置 `FIRECRAWL_API_KEY`。

## 配置 Firecrawl

```json5
{
  tools: {
    web: {
      fetch: {
        firecrawl: {
          apiKey: "FIRECRAWL_API_KEY_HERE",
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 172800000,
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

注意事项：

- 当存在 API 密钥时，`firecrawl.enabled` 默认为 true。
- `maxAgeMs` 控制缓存结果可以保留多久（毫秒）。默认为 2 天。

## 隐身 / 机器人规避

Firecrawl 提供了一个用于机器人规避的**代理模式**参数（`basic`、`stealth` 或 `auto`）。
OpenClaw 对 Firecrawl 请求始终使用 `proxy: "auto"` 加 `storeInCache: true`。
如果省略 proxy，Firecrawl 默认使用 `auto`。`auto` 在基本尝试失败时会使用隐身代理重试，这可能比
仅使用基本抓取消耗更多积分。

## `web_fetch` 如何使用 Firecrawl

`web_fetch` 提取顺序：

1. Readability（本地）
2. Firecrawl（如果已配置）
3. 基本 HTML 清理（最后回退）

参见 [Web 工具](/tools/web) 了解完整的 Web 工具设置。


---
# File: docs/zh-CN/tools/index.md

---
read_when:
  - 添加或修改智能体工具
  - 停用或更改 `openclaw-*` Skills
summary: OpenClaw 的智能体工具接口（browser、canvas、nodes、message、cron），替代旧版 `openclaw-*` Skills
title: 工具
x-i18n:
  generated_at: "2026-02-03T10:12:41Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a1ec62a9c9bea4c1d2cebfb88509739a3b48b451ab3e378193c620832e2aa07b
  source_path: tools/index.md
  workflow: 15
---

# 工具（OpenClaw）

OpenClaw 为 browser、canvas、nodes 和 cron 暴露**一流的智能体工具**。
这些工具取代了旧的 `openclaw-*` Skills：工具是类型化的，无需调用 shell，
智能体应该直接依赖它们。

## 禁用工具

你可以通过 `openclaw.json` 中的 `tools.allow` / `tools.deny` 全局允许/拒绝工具
（deny 优先）。这会阻止不允许的工具被发送到模型提供商。

```json5
{
  tools: { deny: ["browser"] },
}
```

注意：

- 匹配不区分大小写。
- 支持 `*` 通配符（`"*"` 表示所有工具）。
- 如果 `tools.allow` 仅引用未知或未加载的插件工具名称，OpenClaw 会记录警告并忽略允许列表，以确保核心工具保持可用。

## 工具配置文件（基础允许列表）

`tools.profile` 在 `tools.allow`/`tools.deny` 之前设置**基础工具允许列表**。
按智能体覆盖：`agents.list[].tools.profile`。

配置文件：

- `minimal`：仅 `session_status`
- `coding`：`group:fs`、`group:runtime`、`group:sessions`、`group:memory`、`image`
- `messaging`：`group:messaging`、`sessions_list`、`sessions_history`、`sessions_send`、`session_status`
- `full`：无限制（与未设置相同）

示例（默认仅消息，同时允许 Slack + Discord 工具）：

```json5
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

示例（coding 配置文件，但在所有地方拒绝 exec/process）：

```json5
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

示例（全局 coding 配置文件，仅消息的支持智能体）：

```json5
{
  tools: { profile: "coding" },
  agents: {
    list: [
      {
        id: "support",
        tools: { profile: "messaging", allow: ["slack"] },
      },
    ],
  },
}
```

## 特定提供商的工具策略

使用 `tools.byProvider` 为特定提供商（或单个 `provider/model`）**进一步限制**工具，
而不更改你的全局默认值。
按智能体覆盖：`agents.list[].tools.byProvider`。

这在基础工具配置文件**之后**和允许/拒绝列表**之前**应用，
因此它只能缩小工具集。
提供商键接受 `provider`（例如 `google-antigravity`）或
`provider/model`（例如 `openai/gpt-5.2`）。

示例（保持全局 coding 配置文件，但 Google Antigravity 使用最小工具）：

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

示例（针对不稳定端点的 provider/model 特定允许列表）：

```json5
{
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

示例（针对单个提供商的智能体特定覆盖）：

```json5
{
  agents: {
    list: [
      {
        id: "support",
        tools: {
          byProvider: {
            "google-antigravity": { allow: ["message", "sessions_list"] },
          },
        },
      },
    ],
  },
}
```

## 工具组（简写）

工具策略（全局、智能体、沙箱）支持 `group:*` 条目，它们会展开为多个工具。
在 `tools.allow` / `tools.deny` 中使用这些。

可用的组：

- `group:runtime`：`exec`、`bash`、`process`
- `group:fs`：`read`、`write`、`edit`、`apply_patch`
- `group:sessions`：`sessions_list`、`sessions_history`、`sessions_send`、`sessions_spawn`、`session_status`
- `group:memory`：`memory_search`、`memory_get`
- `group:web`：`web_search`、`web_fetch`
- `group:ui`：`browser`、`canvas`
- `group:automation`：`cron`、`gateway`
- `group:messaging`：`message`
- `group:nodes`：`nodes`
- `group:openclaw`：所有内置 OpenClaw 工具（不包括提供商插件）

示例（仅允许文件工具 + browser）：

```json5
{
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

## 插件 + 工具

插件可以在核心集之外注册**额外的工具**（和 CLI 命令）。
参见[插件](/tools/plugin)了解安装 + 配置，以及 [Skills](/tools/skills) 了解
工具使用指导如何被注入到提示中。一些插件随工具一起提供自己的 Skills
（例如，voice-call 插件）。

可选的插件工具：

- [Lobster](/tools/lobster)：带有可恢复审批的类型化工作流运行时（需要 Gateway 网关主机上的 Lobster CLI）。
- [LLM Task](/tools/llm-task)：用于结构化工作流输出的 JSON-only LLM 步骤（可选 schema 验证）。

## 工具清单

### `apply_patch`

跨一个或多个文件应用结构化补丁。用于多块编辑。
实验性：通过 `tools.exec.applyPatch.enabled` 启用（仅 OpenAI 模型）。

### `exec`

在工作区中运行 shell 命令。

核心参数：

- `command`（必需）
- `yieldMs`（超时后自动后台运行，默认 10000）
- `background`（立即后台运行）
- `timeout`（秒；超过则终止进程，默认 1800）
- `elevated`（布尔值；如果启用/允许提升模式，则在主机上运行；仅在智能体被沙箱隔离时改变行为）
- `host`（`sandbox | gateway | node`）
- `security`（`deny | allowlist | full`）
- `ask`（`off | on-miss | always`）
- `node`（`host=node` 时的节点 id/名称）
- 需要真正的 TTY？设置 `pty: true`。

注意：

- 后台运行时返回带有 `sessionId` 的 `status: "running"`。
- 使用 `process` 来轮询/日志/写入/终止/清除后台会话。
- 如果不允许 `process`，`exec` 会同步运行并忽略 `yieldMs`/`background`。
- `elevated` 受 `tools.elevated` 加上任何 `agents.list[].tools.elevated` 覆盖的门控（两者都必须允许），是 `host=gateway` + `security=full` 的别名。
- `elevated` 仅在智能体被沙箱隔离时改变行为（否则是空操作）。
- `host=node` 可以针对 macOS 配套应用或无头节点主机（`openclaw node run`）。
- Gateway 网关/节点审批和允许列表：[执行审批](/tools/exec-approvals)。

### `process`

管理后台 exec 会话。

核心操作：

- `list`、`poll`、`log`、`write`、`kill`、`clear`、`remove`

注意：

- `poll` 返回新输出，完成时返回退出状态。
- `log` 支持基于行的 `offset`/`limit`（省略 `offset` 以获取最后 N 行）。
- `process` 按智能体作用域；来自其他智能体的会话不可见。

### `web_search`

使用 Brave Search API 搜索网络。

核心参数：

- `query`（必需）
- `count`（1-10；默认来自 `tools.web.search.maxResults`）

注意：

- 需要 Brave API 密钥（推荐：`openclaw configure --section web`，或设置 `BRAVE_API_KEY`）。
- 通过 `tools.web.search.enabled` 启用。
- 响应被缓存（默认 15 分钟）。
- 参见 [Web 工具](/tools/web) 了解设置。

### `web_fetch`

从 URL 获取并提取可读内容（HTML → markdown/text）。

核心参数：

- `url`（必需）
- `extractMode`（`markdown` | `text`）
- `maxChars`（截断长页面）

注意：

- 通过 `tools.web.fetch.enabled` 启用。
- 响应被缓存（默认 15 分钟）。
- 对于 JS 密集型网站，优先使用 browser 工具。
- 参见 [Web 工具](/tools/web) 了解设置。
- 参见 [Firecrawl](/tools/firecrawl) 了解可选的反机器人回退。

### `browser`

控制专用的 OpenClaw 管理的浏览器。

核心操作：

- `status`、`start`、`stop`、`tabs`、`open`、`focus`、`close`
- `snapshot`（aria/ai）
- `screenshot`（返回图像块 + `MEDIA:<path>`）
- `act`（UI 操作：click/type/press/hover/drag/select/fill/resize/wait/evaluate）
- `navigate`、`console`、`pdf`、`upload`、`dialog`

配置文件管理：

- `profiles` — 列出所有浏览器配置文件及其状态
- `create-profile` — 使用自动分配的端口（或 `cdpUrl`）创建新配置文件
- `delete-profile` — 停止浏览器，删除用户数据，从配置中移除（仅本地）
- `reset-profile` — 终止配置文件端口上的孤儿进程（仅本地）

常用参数：

- `profile`（可选；默认为 `browser.defaultProfile`）
- `target`（`sandbox` | `host` | `node`）
- `node`（可选；选择特定的节点 id/名称）
  注意：
- 需要 `browser.enabled=true`（默认为 `true`；设置为 `false` 以禁用）。
- 所有操作接受可选的 `profile` 参数以支持多实例。
- 当省略 `profile` 时，使用 `browser.defaultProfile`（默认为"chrome"）。
- 配置文件名称：仅小写字母数字 + 连字符（最多 64 字符）。
- 端口范围：18800-18899（最多约 100 个配置文件）。
- 远程配置文件仅支持附加（无 start/stop/reset）。
- 如果连接了支持浏览器的节点，工具可能会自动路由到它（除非你固定了 `target`）。
- 安装 Playwright 时 `snapshot` 默认为 `ai`；使用 `aria` 获取无障碍树。
- `snapshot` 还支持角色快照选项（`interactive`、`compact`、`depth`、`selector`），返回像 `e12` 这样的引用。
- `act` 需要来自 `snapshot` 的 `ref`（AI 快照中的数字 `12`，或角色快照中的 `e12`）；对于罕见的 CSS 选择器需求使用 `evaluate`。
- 默认避免 `act` → `wait`；仅在特殊情况下使用（没有可靠的 UI 状态可等待）。
- `upload` 可以选择性地传递 `ref` 以在准备后自动点击。
- `upload` 还支持 `inputRef`（aria 引用）或 `element`（CSS 选择器）以直接设置 `<input type="file">`。

### `canvas`

驱动节点 Canvas（present、eval、snapshot、A2UI）。

核心操作：

- `present`、`hide`、`navigate`、`eval`
- `snapshot`（返回图像块 + `MEDIA:<path>`）
- `a2ui_push`、`a2ui_reset`

注意：

- 底层使用 Gateway 网关 `node.invoke`。
- 如果未提供 `node`，工具会选择默认值（单个连接的节点或本地 mac 节点）。
- A2UI 仅限 v0.8（无 `createSurface`）；CLI 会拒绝 v0.9 JSONL 并显示行错误。
- 快速冒烟测试：`openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`。

### `nodes`

发现和定位配对的节点；发送通知；捕获摄像头/屏幕。

核心操作：

- `status`、`describe`
- `pending`、`approve`、`reject`（配对）
- `notify`（macOS `system.notify`）
- `run`（macOS `system.run`）
- `camera_snap`、`camera_clip`、`screen_record`
- `location_get`

注意：

- 摄像头/屏幕命令需要节点应用在前台。
- 图像返回图像块 + `MEDIA:<path>`。
- 视频返回 `FILE:<path>`（mp4）。
- 位置返回 JSON 负载（lat/lon/accuracy/timestamp）。
- `run` 参数：`command` argv 数组；可选的 `cwd`、`env`（`KEY=VAL`）、`commandTimeoutMs`、`invokeTimeoutMs`、`needsScreenRecording`。

示例（`run`）：

```json
{
  "action": "run",
  "node": "office-mac",
  "command": ["echo", "Hello"],
  "env": ["FOO=bar"],
  "commandTimeoutMs": 12000,
  "invokeTimeoutMs": 45000,
  "needsScreenRecording": false
}
```

### `image`

使用配置的图像模型分析图像。

核心参数：

- `image`（必需的路径或 URL）
- `prompt`（可选；默认为"Describe the image."）
- `model`（可选覆盖）
- `maxBytesMb`（可选大小上限）

注意：

- 仅在配置了 `agents.defaults.imageModel`（主要或回退）时可用，或者当可以从你的默认模型 + 配置的认证推断出隐式图像模型时（尽力配对）。
- 直接使用图像模型（独立于主聊天模型）。

### `message`

跨 Discord/Google Chat/Slack/Telegram/WhatsApp/Signal/iMessage/MS Teams 发送消息和渠道操作。

核心操作：

- `send`（文本 + 可选媒体；MS Teams 还支持用于 Adaptive Cards 的 `card`）
- `poll`（WhatsApp/Discord/MS Teams 投票）
- `react` / `reactions` / `read` / `edit` / `delete`
- `pin` / `unpin` / `list-pins`
- `permissions`
- `thread-create` / `thread-list` / `thread-reply`
- `search`
- `sticker`
- `member-info` / `role-info`
- `emoji-list` / `emoji-upload` / `sticker-upload`
- `role-add` / `role-remove`
- `channel-info` / `channel-list`
- `voice-status`
- `event-list` / `event-create`
- `timeout` / `kick` / `ban`

注意：

- `send` 通过 Gateway 网关路由 WhatsApp；其他渠道直接发送。
- `poll` 对 WhatsApp 和 MS Teams 使用 Gateway 网关；Discord 投票直接发送。
- 当消息工具调用绑定到活动聊天会话时，发送被限制到该会话的目标以避免跨上下文泄露。

### `cron`

管理 Gateway 网关定时任务和唤醒。

核心操作：

- `status`、`list`
- `add`、`update`、`remove`、`run`、`runs`
- `wake`（入队系统事件 + 可选的立即心跳）

注意：

- `add` 期望完整的定时任务对象（与 `cron.add` RPC 相同的 schema）。
- `update` 使用 `{ id, patch }`。

### `gateway`

重启或对运行中的 Gateway 网关进程应用更新（就地）。

核心操作：

- `restart`（授权 + 发送 `SIGUSR1` 进行进程内重启；`openclaw gateway` 就地重启）
- `config.get` / `config.schema`
- `config.apply`（验证 + 写入配置 + 重启 + 唤醒）
- `config.patch`（合并部分更新 + 重启 + 唤醒）
- `update.run`（运行更新 + 重启 + 唤醒）

注意：

- 使用 `delayMs`（默认 2000）以避免中断进行中的回复。
- `restart` 默认禁用；使用 `commands.restart: true` 启用。

### `sessions_list` / `sessions_history` / `sessions_send` / `sessions_spawn` / `session_status`

列出会话，检查转录历史，或发送到另一个会话。

核心参数：

- `sessions_list`：`kinds?`、`limit?`、`activeMinutes?`、`messageLimit?`（0 = 无）
- `sessions_history`：`sessionKey`（或 `sessionId`）、`limit?`、`includeTools?`
- `sessions_send`：`sessionKey`（或 `sessionId`）、`message`、`timeoutSeconds?`（0 = fire-and-forget）
- `sessions_spawn`：`task`、`label?`、`agentId?`、`model?`、`runTimeoutSeconds?`、`cleanup?`
- `session_status`：`sessionKey?`（默认当前；接受 `sessionId`）、`model?`（`default` 清除覆盖）

注意：

- `main` 是规范的私聊键；global/unknown 是隐藏的。
- `messageLimit > 0` 获取每个会话的最后 N 条消息（工具消息被过滤）。
- 当 `timeoutSeconds > 0` 时，`sessions_send` 等待最终完成。
- 递送/宣告发生在完成后，是尽力而为的；`status: "ok"` 确认智能体运行完成，而不是宣告已递送。
- `sessions_spawn` 启动子智能体运行并将宣告回复发送回请求者聊天。
- `sessions_spawn` 是非阻塞的，立即返回 `status: "accepted"`。
- `sessions_send` 运行回复往返乒乓（回复 `REPLY_SKIP` 以停止；最大轮次通过 `session.agentToAgent.maxPingPongTurns`，0-5）。
- 乒乓之后，目标智能体运行一个**宣告步骤**；回复 `ANNOUNCE_SKIP` 以抑制宣告。

### `agents_list`

列出当前会话可以用 `sessions_spawn` 定位的智能体 id。

注意：

- 结果受每智能体允许列表限制（`agents.list[].subagents.allowAgents`）。
- 当配置为 `["*"]` 时，工具包含所有已配置的智能体并标记 `allowAny: true`。

## 参数（通用）

Gateway 网关支持的工具（`canvas`、`nodes`、`cron`）：

- `gatewayUrl`（默认 `ws://127.0.0.1:18789`）
- `gatewayToken`（如果启用了认证）
- `timeoutMs`

Browser 工具：

- `profile`（可选；默认为 `browser.defaultProfile`）
- `target`（`sandbox` | `host` | `node`）
- `node`（可选；固定特定的节点 id/名称）

## 推荐的智能体流程

浏览器自动化：

1. `browser` → `status` / `start`
2. `snapshot`（ai 或 aria）
3. `act`（click/type/press）
4. `screenshot` 如果你需要视觉确认

Canvas 渲染：

1. `canvas` → `present`
2. `a2ui_push`（可选）
3. `snapshot`

节点定位：

1. `nodes` → `status`
2. 在选定的节点上 `describe`
3. `notify` / `run` / `camera_snap` / `screen_record`

## 安全性

- 避免直接 `system.run`；仅在用户明确同意时使用 `nodes` → `run`。
- 尊重用户对摄像头/屏幕捕获的同意。
- 在调用媒体命令前使用 `status/describe` 确保权限。

## 工具如何呈现给智能体

工具通过两个并行渠道暴露：

1. **系统提示文本**：人类可读的列表 + 指导。
2. **工具 schema**：发送到模型 API 的结构化函数定义。

这意味着智能体同时看到"存在哪些工具"和"如何调用它们"。如果工具
没有出现在系统提示或 schema 中，模型就无法调用它。


---
# File: docs/zh-CN/tools/llm-task.md

---
read_when:
  - 你需要在工作流中添加纯 JSON 的 LLM 步骤
  - 你需要经过 Schema 验证的 LLM 输出用于自动化
summary: 用于工作流的纯 JSON LLM 任务（可选插件工具）
title: LLM 任务
x-i18n:
  generated_at: "2026-02-01T21:42:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d81b74fcfd5491a9edb4bfadb47d404067020990b1f6d6d8fed652fbc860f646
  source_path: tools/llm-task.md
  workflow: 15
---

# LLM 任务

`llm-task` 是一个**可选插件工具**，用于运行纯 JSON 的 LLM 任务并返回结构化输出（可选择根据 JSON Schema 进行验证）。

这非常适合像 Lobster 这样的工作流引擎：你可以添加单个 LLM 步骤，而无需为每个工作流编写自定义 OpenClaw 代码。

## 启用插件

1. 启用插件：

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  }
}
```

2. 将工具加入允许列表（它以 `optional: true` 注册）：

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

## 配置（可选）

```json
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.2",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.2"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```

`allowedModels` 是 `provider/model` 字符串的允许列表。如果设置了该项，任何不在列表中的请求都会被拒绝。

## 工具参数

- `prompt`（字符串，必填）
- `input`（任意类型，可选）
- `schema`（对象，可选 JSON Schema）
- `provider`（字符串，可选）
- `model`（字符串，可选）
- `authProfileId`（字符串，可选）
- `temperature`（数字，可选）
- `maxTokens`（数字，可选）
- `timeoutMs`（数字，可选）

## 输出

返回 `details.json`，包含解析后的 JSON（如果提供了 `schema`，则会进行验证）。

## 示例：Lobster 工作流步骤

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

## 安全注意事项

- 该工具为**纯 JSON 模式**，指示模型仅输出 JSON（无代码围栏、无注释说明）。
- 此次运行不会向模型暴露任何工具。
- 除非使用 `schema` 进行验证，否则应将输出视为不可信。
- 在任何有副作用的步骤（发送、发布、执行）之前设置审批流程。


---
# File: docs/zh-CN/tools/lobster.md

---
description: Typed workflow runtime for OpenClaw — composable pipelines with approval gates.
read_when:
  - 你想要具有显式审批的确定性多步骤工作流
  - 你需要恢复工作流而不重新运行早期步骤
summary: OpenClaw 的类型化工作流运行时，支持可恢复的审批关卡。
title: Lobster
x-i18n:
  generated_at: "2026-02-03T10:11:30Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ff84e65f4be162ad98f16ddf0882f23b3198f05b4d9e8dc03d07e9b2bf0fd5ad
  source_path: tools/lobster.md
  workflow: 15
---

# Lobster

Lobster 是一个工作流外壳，让 OpenClaw 能够将多步骤工具序列作为单个确定性操作运行，并带有显式审批检查点。

## 亮点

你的助手可以构建管理自身的工具。请求一个工作流，30 分钟后你就有了一个 CLI 和作为单次调用运行的管道。Lobster 是缺失的那一块：确定性管道、显式审批和可恢复状态。

## 为什么

如今，复杂的工作流需要多次来回的工具调用。每次调用都消耗 token，LLM 必须编排每一步。Lobster 将这种编排移入类型化运行时：

- **一次调用代替多次**：OpenClaw 运行一次 Lobster 工具调用并获得结构化结果。
- **内置审批**：副作用（发送邮件、发布评论）会暂停工作流，直到明确批准。
- **可恢复**：暂停的工作流返回一个令牌；批准并恢复而无需重新运行所有内容。

## 为什么用 DSL 而不是普通程序？

Lobster 故意很小。目标不是"一种新语言"，而是一个可预测的、AI 友好的管道规范，具有一流的审批和恢复令牌。

- **内置批准/恢复**：普通程序可以提示人类，但它无法*暂停和恢复*并带有持久令牌，除非你自己发明那个运行时。
- **确定性 + 可审计性**：管道是数据，所以它们易于记录、比较、重放和审查。
- **AI 的受限表面**：微小的语法 + JSON 管道减少了"创造性"代码路径，使验证变得现实可行。
- **内置安全策略**：超时、输出上限、沙箱检查和白名单由运行时强制执行，而不是每个脚本。
- **仍然可编程**：每个步骤都可以调用任何 CLI 或脚本。如果你想要 JS/TS，可以从代码生成 `.lobster` 文件。

## 工作原理

OpenClaw 以**工具模式**启动本地 `lobster` CLI，并从 stdout 解析 JSON 信封。
如果管道暂停等待审批，工具会返回一个 `resumeToken`，以便你稍后继续。

## 模式：小型 CLI + JSON 管道 + 审批

构建输出 JSON 的小命令，然后将它们链接成单个 Lobster 调用。（下面是示例命令名称——替换成你自己的。）

```bash
inbox list --json
inbox categorize --json
inbox apply --json
```

```json
{
  "action": "run",
  "pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",
  "timeoutMs": 30000
}
```

如果管道请求审批，使用令牌恢复：

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

AI 触发工作流；Lobster 执行步骤。审批关卡使副作用显式且可审计。

示例：将输入项映射到工具调用：

```bash
gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

## 纯 JSON 的 LLM 步骤（llm-task）

对于需要**结构化 LLM 步骤**的工作流，启用可选的
`llm-task` 插件工具并从 Lobster 调用它。这保持了工作流的
确定性，同时仍然允许你使用模型进行分类/摘要/起草。

启用工具：

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

在管道中使用它：

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": { "subject": "Hello", "body": "Can you help?" },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

参见 [LLM Task](/tools/llm-task) 了解详情和配置选项。

## 工作流文件（.lobster）

Lobster 可以运行包含 `name`、`args`、`steps`、`env`、`condition` 和 `approval` 字段的 YAML/JSON 工作流文件。在 OpenClaw 工具调用中，将 `pipeline` 设置为文件路径。

```yaml
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

注意事项：

- `stdin: $step.stdout` 和 `stdin: $step.json` 传递前一步骤的输出。
- `condition`（或 `when`）可以根据 `$step.approved` 控制步骤。

## 安装 Lobster

在运行 OpenClaw Gateway 网关的**同一主机**上安装 Lobster CLI（参见 [Lobster 仓库](https://github.com/openclaw/lobster)），并确保 `lobster` 在 `PATH` 中。
如果你想使用自定义二进制位置，在工具调用中传递**绝对**路径 `lobsterPath`。

## 启用工具

Lobster 是一个**可选**的插件工具（默认未启用）。

推荐（附加，安全）：

```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

或每个智能体：

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["lobster"]
        }
      }
    ]
  }
}
```

避免使用 `tools.allow: ["lobster"]`，除非你打算在限制性白名单模式下运行。

注意：白名单对于可选插件是自愿加入的。如果你的白名单只包含
插件工具（如 `lobster`），OpenClaw 会保持核心工具启用。要限制核心
工具，也要在白名单中包含你想要的核心工具或组。

## 示例：邮件分类

不使用 Lobster：

```
用户："检查我的邮件并起草回复"
→ openclaw 调用 gmail.list
→ LLM 总结
→ 用户："给 #2 和 #5 起草回复"
→ LLM 起草
→ 用户："发送 #2"
→ openclaw 调用 gmail.send
（每天重复，不记得已分类的内容）
```

使用 Lobster：

```json
{
  "action": "run",
  "pipeline": "email.triage --limit 20",
  "timeoutMs": 30000
}
```

返回一个 JSON 信封（已截断）：

```json
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

用户批准 → 恢复：

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

一个工作流。确定性。安全。

## 工具参数

### `run`

以工具模式运行管道。

```json
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "/path/to/workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

使用参数运行工作流文件：

```json
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

### `resume`

在审批后继续暂停的工作流。

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### 可选输入

- `lobsterPath`：Lobster 二进制文件的绝对路径（省略则使用 `PATH`）。
- `cwd`：管道的工作目录（默认为当前进程工作目录）。
- `timeoutMs`：如果子进程超过此持续时间则终止（默认：20000）。
- `maxStdoutBytes`：如果 stdout 超过此大小则终止子进程（默认：512000）。
- `argsJson`：传递给 `lobster run --args-json` 的 JSON 字符串（仅限工作流文件）。

## 输出信封

Lobster 返回一个具有三种状态之一的 JSON 信封：

- `ok` → 成功完成
- `needs_approval` → 已暂停；需要 `requiresApproval.resumeToken` 才能恢复
- `cancelled` → 明确拒绝或取消

工具在 `content`（格式化 JSON）和 `details`（原始对象）中都显示信封。

## 审批

如果存在 `requiresApproval`，检查提示并决定：

- `approve: true` → 恢复并继续副作用
- `approve: false` → 取消并终结工作流

使用 `approve --preview-from-stdin --limit N` 将 JSON 预览附加到审批请求，无需自定义 jq/heredoc 粘合代码。恢复令牌现在很紧凑：Lobster 在其状态目录下存储工作流恢复状态，并返回一个小令牌键。

## OpenProse

OpenProse 与 Lobster 配合良好：使用 `/prose` 编排多智能体准备，然后运行 Lobster 管道进行确定性审批。如果 Prose 程序需要 Lobster，通过 `tools.subagents.tools` 为子智能体允许 `lobster` 工具。参见 [OpenProse](/prose)。

## 安全

- **仅限本地子进程** — 插件本身不进行网络调用。
- **无密钥** — Lobster 不管理 OAuth；它调用管理 OAuth 的 OpenClaw 工具。
- **沙箱感知** — 当工具上下文处于沙箱隔离状态时禁用。
- **加固** — 如果指定，`lobsterPath` 必须是绝对路径；强制执行超时和输出上限。

## 故障排除

- **`lobster subprocess timed out`** → 增加 `timeoutMs`，或拆分长管道。
- **`lobster output exceeded maxStdoutBytes`** → 提高 `maxStdoutBytes` 或减少输出大小。
- **`lobster returned invalid JSON`** → 确保管道以工具模式运行并只打印 JSON。
- **`lobster failed (code …)`** → 在终端中运行相同的管道以检查 stderr。

## 了解更多

- [插件](/tools/plugin)
- [插件工具开发](/plugins/agent-tools)

## 案例研究：社区工作流

一个公开示例：一个"第二大脑" CLI + Lobster 管道，管理三个 Markdown 库（个人、伴侣、共享）。CLI 为统计、收件箱列表和过时扫描输出 JSON；Lobster 将这些命令链接成 `weekly-review`、`inbox-triage`、`memory-consolidation` 和 `shared-task-sync` 等工作流，每个都有审批关卡。AI 在可用时处理判断（分类），不可用时回退到确定性规则。

- 帖子：https://x.com/plattenschieber/status/2014508656335770033
- 仓库：https://github.com/bloomedai/brain-cli


---
# File: docs/zh-CN/tools/multi-agent-sandbox-tools.md

---
read_when: You want per-agent sandboxing or per-agent tool allow/deny policies in a multi-agent gateway.
status: active
summary: 按智能体的沙箱 + 工具限制、优先级和示例
title: 多智能体沙箱与工具
x-i18n:
  generated_at: "2026-02-03T07:50:39Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f602cb6192b84b404cd7b6336562888a239d0fe79514edd51bd73c5b090131ef
  source_path: tools/multi-agent-sandbox-tools.md
  workflow: 15
---

# 多智能体沙箱与工具配置

## 概述

多智能体设置中的每个智能体现在可以拥有自己的：

- **沙箱配置**（`agents.list[].sandbox` 覆盖 `agents.defaults.sandbox`）
- **工具限制**（`tools.allow` / `tools.deny`，以及 `agents.list[].tools`）

这允许你运行具有不同安全配置文件的多个智能体：

- 具有完全访问权限的个人助手
- 具有受限工具的家庭/工作智能体
- 在沙箱中运行的面向公众的智能体

`setupCommand` 属于 `sandbox.docker` 下（全局或按智能体），在容器创建时运行一次。

认证是按智能体的：每个智能体从其自己的 `agentDir` 认证存储读取：

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

凭证**不会**在智能体之间共享。切勿在智能体之间重用 `agentDir`。
如果你想共享凭证，请将 `auth-profiles.json` 复制到其他智能体的 `agentDir` 中。

有关沙箱隔离在运行时的行为，请参见[沙箱隔离](/gateway/sandboxing)。
有关调试"为什么这被阻止了？"，请参见[沙箱 vs 工具策略 vs 提权](/gateway/sandbox-vs-tool-policy-vs-elevated) 和 `openclaw sandbox explain`。

---

## 配置示例

### 示例 1：个人 + 受限家庭智能体

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "name": "Family Bot",
        "workspace": "~/.openclaw/workspace-family",
        "sandbox": {
          "mode": "all",
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch", "process", "browser"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "family",
      "match": {
        "provider": "whatsapp",
        "accountId": "*",
        "peer": {
          "kind": "group",
          "id": "120363424282127706@g.us"
        }
      }
    }
  ]
}
```

**结果：**

- `main` 智能体：在主机上运行，完全工具访问
- `family` 智能体：在 Docker 中运行（每个智能体一个容器），仅有 `read` 工具

---

### 示例 2：具有共享沙箱的工作智能体

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "shared",
          "workspaceRoot": "/tmp/work-sandboxes"
        },
        "tools": {
          "allow": ["read", "write", "apply_patch", "exec"],
          "deny": ["browser", "gateway", "discord"]
        }
      }
    ]
  }
}
```

---

### 示例 2b：全局编码配置文件 + 仅消息智能体

```json
{
  "tools": { "profile": "coding" },
  "agents": {
    "list": [
      {
        "id": "support",
        "tools": { "profile": "messaging", "allow": ["slack"] }
      }
    ]
  }
}
```

**结果：**

- 默认智能体获得编码工具
- `support` 智能体仅用于消息（+ Slack 工具）

---

### 示例 3：每个智能体不同的沙箱模式

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main", // 全局默认
        "scope": "session"
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "sandbox": {
          "mode": "off" // 覆盖：main 永不沙箱隔离
        }
      },
      {
        "id": "public",
        "workspace": "~/.openclaw/workspace-public",
        "sandbox": {
          "mode": "all", // 覆盖：public 始终沙箱隔离
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch"]
        }
      }
    ]
  }
}
```

---

## 配置优先级

当全局（`agents.defaults.*`）和智能体特定（`agents.list[].*`）配置同时存在时：

### 沙箱配置

智能体特定设置覆盖全局：

```
agents.list[].sandbox.mode > agents.defaults.sandbox.mode
agents.list[].sandbox.scope > agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot > agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess > agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* > agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* > agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* > agents.defaults.sandbox.prune.*
```

**注意事项：**

- `agents.list[].sandbox.{docker,browser,prune}.*` 为该智能体覆盖 `agents.defaults.sandbox.{docker,browser,prune}.*`（当沙箱 scope 解析为 `"shared"` 时忽略）。

### 工具限制

过滤顺序是：

1. **工具配置文件**（`tools.profile` 或 `agents.list[].tools.profile`）
2. **提供商工具配置文件**（`tools.byProvider[provider].profile` 或 `agents.list[].tools.byProvider[provider].profile`）
3. **全局工具策略**（`tools.allow` / `tools.deny`）
4. **提供商工具策略**（`tools.byProvider[provider].allow/deny`）
5. **智能体特定工具策略**（`agents.list[].tools.allow/deny`）
6. **智能体提供商策略**（`agents.list[].tools.byProvider[provider].allow/deny`）
7. **沙箱工具策略**（`tools.sandbox.tools` 或 `agents.list[].tools.sandbox.tools`）
8. **子智能体工具策略**（`tools.subagents.tools`，如适用）

每个级别可以进一步限制工具，但不能恢复之前级别拒绝的工具。
如果设置了 `agents.list[].tools.sandbox.tools`，它将替换该智能体的 `tools.sandbox.tools`。
如果设置了 `agents.list[].tools.profile`，它将覆盖该智能体的 `tools.profile`。
提供商工具键接受 `provider`（例如 `google-antigravity`）或 `provider/model`（例如 `openai/gpt-5.2`）。

### 工具组（简写）

工具策略（全局、智能体、沙箱）支持 `group:*` 条目，可扩展为多个具体工具：

- `group:runtime`：`exec`、`bash`、`process`
- `group:fs`：`read`、`write`、`edit`、`apply_patch`
- `group:sessions`：`sessions_list`、`sessions_history`、`sessions_send`、`sessions_spawn`、`session_status`
- `group:memory`：`memory_search`、`memory_get`
- `group:ui`：`browser`、`canvas`
- `group:automation`：`cron`、`gateway`
- `group:messaging`：`message`
- `group:nodes`：`nodes`
- `group:openclaw`：所有内置 OpenClaw 工具（不包括提供商插件）

### 提权模式

`tools.elevated` 是全局基线（基于发送者的允许列表）。`agents.list[].tools.elevated` 可以为特定智能体进一步限制提权（两者都必须允许）。

缓解模式：

- 为不受信任的智能体拒绝 `exec`（`agents.list[].tools.deny: ["exec"]`）
- 避免将发送者加入允许列表后路由到受限智能体
- 如果你只想要沙箱隔离执行，全局禁用提权（`tools.elevated.enabled: false`）
- 为敏感配置文件按智能体禁用提权（`agents.list[].tools.elevated.enabled: false`）

---

## 从单智能体迁移

**之前（单智能体）：**

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["read", "write", "apply_patch", "exec"],
        "deny": []
      }
    }
  }
}
```

**之后（具有不同配置文件的多智能体）：**

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    ]
  }
}
```

旧版 `agent.*` 配置由 `openclaw doctor` 迁移；今后请优先使用 `agents.defaults` + `agents.list`。

---

## 工具限制示例

### 只读智能体

```json
{
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "apply_patch", "process"]
  }
}
```

### 安全执行智能体（无文件修改）

```json
{
  "tools": {
    "allow": ["read", "exec", "process"],
    "deny": ["write", "edit", "apply_patch", "browser", "gateway"]
  }
}
```

### 仅通信智能体

```json
{
  "tools": {
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

---

## 常见陷阱："non-main"

`agents.defaults.sandbox.mode: "non-main"` 基于 `session.mainKey`（默认 `"main"`），
而不是智能体 id。群组/渠道会话始终获得自己的键，因此它们
被视为非 main 并将被沙箱隔离。如果你希望智能体永不
沙箱隔离，请设置 `agents.list[].sandbox.mode: "off"`。

---

## 测试

配置多智能体沙箱和工具后：

1. **检查智能体解析：**

   ```exec
   openclaw agents list --bindings
   ```

2. **验证沙箱容器：**

   ```exec
   docker ps --filter "name=openclaw-sbx-"
   ```

3. **测试工具限制：**
   - 发送需要受限工具的消息
   - 验证智能体无法使用被拒绝的工具

4. **监控日志：**
   ```exec
   tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"
   ```

---

## 故障排除

### 尽管设置了 `mode: "all"` 但智能体未被沙箱隔离

- 检查是否有全局 `agents.defaults.sandbox.mode` 覆盖它
- 智能体特定配置优先，因此设置 `agents.list[].sandbox.mode: "all"`

### 尽管有拒绝列表但工具仍然可用

- 检查工具过滤顺序：全局 → 智能体 → 沙箱 → 子智能体
- 每个级别只能进一步限制，不能恢复
- 通过日志验证：`[tools] filtering tools for agent:${agentId}`

### 容器未按智能体隔离

- 在智能体特定沙箱配置中设置 `scope: "agent"`
- 默认是 `"session"`，每个会话创建一个容器

---

## 另请参阅

- [多智能体路由](/concepts/multi-agent)
- [沙箱配置](/gateway/configuration#agentsdefaults-sandbox)
- [会话管理](/concepts/session)


---
# File: docs/zh-CN/tools/plugin.md

---
read_when:
  - 添加或修改插件/扩展
  - 记录插件安装或加载规则
summary: OpenClaw 插件/扩展：发现、配置和安全
title: 插件
x-i18n:
  generated_at: "2026-02-03T07:55:25Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b36ca6b90ca03eaae25c00f9b12f2717fcd17ac540ba616ee03b398b234c2308
  source_path: tools/plugin.md
  workflow: 15
---

# 插件（扩展）

## 快速开始（插件新手？）

插件只是一个**小型代码模块**，用额外功能（命令、工具和 Gateway 网关 RPC）扩展 OpenClaw。

大多数时候，当你想要一个尚未内置到核心 OpenClaw 的功能（或你想将可选功能排除在主安装之外）时，你会使用插件。

快速路径：

1. 查看已加载的内容：

```bash
openclaw plugins list
```

2. 安装官方插件（例如：Voice Call）：

```bash
openclaw plugins install @openclaw/voice-call
```

3. 重启 Gateway 网关，然后在 `plugins.entries.<id>.config` 下配置。

参见 [Voice Call](/plugins/voice-call) 了解具体的插件示例。

## 可用插件（官方）

- 从 2026.1.15 起 Microsoft Teams 仅作为插件提供；如果使用 Teams，请安装 `@openclaw/msteams`。
- Memory (Core) — 捆绑的记忆搜索插件（通过 `plugins.slots.memory` 默认启用）
- Memory (LanceDB) — 捆绑的长期记忆插件（自动召回/捕获；设置 `plugins.slots.memory = "memory-lancedb"`）
- [Voice Call](/plugins/voice-call) — `@openclaw/voice-call`
- [Zalo Personal](/plugins/zalouser) — `@openclaw/zalouser`
- [Matrix](/channels/matrix) — `@openclaw/matrix`
- [Nostr](/channels/nostr) — `@openclaw/nostr`
- [Zalo](/channels/zalo) — `@openclaw/zalo`
- [Microsoft Teams](/channels/msteams) — `@openclaw/msteams`
- Google Antigravity OAuth（提供商认证）— 作为 `google-antigravity-auth` 捆绑（默认禁用）
- Gemini CLI OAuth（提供商认证）— 作为 `google-gemini-cli-auth` 捆绑（默认禁用）
- Qwen OAuth（提供商认证）— 作为 `qwen-portal-auth` 捆绑（默认禁用）
- Copilot Proxy（提供商认证）— 本地 VS Code Copilot Proxy 桥接；与内置 `github-copilot` 设备登录不同（捆绑，默认禁用）

OpenClaw 插件是通过 jiti 在运行时加载的 **TypeScript 模块**。**配置验证不会执行插件代码**；它使用插件清单和 JSON Schema。参见 [插件清单](/plugins/manifest)。

插件可以注册：

- Gateway 网关 RPC 方法
- Gateway 网关 HTTP 处理程序
- 智能体工具
- CLI 命令
- 后台服务
- 可选的配置验证
- **Skills**（通过在插件清单中列出 `skills` 目录）
- **自动回复命令**（不调用 AI 智能体即可执行）

插件与 Gateway 网关**在同一进程中**运行，因此将它们视为受信任的代码。
工具编写指南：[插件智能体工具](/plugins/agent-tools)。

## 运行时辅助工具

插件可以通过 `api.runtime` 访问选定的核心辅助工具。对于电话 TTS：

```ts
const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
```

注意事项：

- 使用核心 `messages.tts` 配置（OpenAI 或 ElevenLabs）。
- 返回 PCM 音频缓冲区 + 采样率。插件必须为提供商重新采样/编码。
- Edge TTS 不支持电话。

## 发现和优先级

OpenClaw 按顺序扫描：

1. 配置路径

- `plugins.load.paths`（文件或目录）

2. 工作区扩展

- `<workspace>/.openclaw/extensions/*.ts`
- `<workspace>/.openclaw/extensions/*/index.ts`

3. 全局扩展

- `~/.openclaw/extensions/*.ts`
- `~/.openclaw/extensions/*/index.ts`

4. 捆绑扩展（随 OpenClaw 一起发布，**默认禁用**）

- `<openclaw>/extensions/*`

捆绑插件必须通过 `plugins.entries.<id>.enabled` 或 `openclaw plugins enable <id>` 显式启用。已安装的插件默认启用，但可以用相同方式禁用。

每个插件必须在其根目录中包含 `openclaw.plugin.json` 文件。如果路径指向文件，则插件根目录是文件的目录，必须包含清单。

如果多个插件解析到相同的 id，上述顺序中的第一个匹配项获胜，较低优先级的副本被忽略。

### 包集合

插件目录可以包含带有 `openclaw.extensions` 的 `package.json`：

```json
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"]
  }
}
```

每个条目成为一个插件。如果包列出多个扩展，插件 id 变为 `name/<fileBase>`。

如果你的插件导入 npm 依赖，请在该目录中安装它们以便 `node_modules` 可用（`npm install` / `pnpm install`）。

### 渠道目录元数据

渠道插件可以通过 `openclaw.channel` 广播新手引导元数据，通过 `openclaw.install` 广播安装提示。这使核心目录保持无数据。

示例：

```json
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "extensions": ["./index.ts"],
    "channel": {
      "id": "nextcloud-talk",
      "label": "Nextcloud Talk",
      "selectionLabel": "Nextcloud Talk (self-hosted)",
      "docsPath": "/channels/nextcloud-talk",
      "docsLabel": "nextcloud-talk",
      "blurb": "Self-hosted chat via Nextcloud Talk webhook bots.",
      "order": 65,
      "aliases": ["nc-talk", "nc"]
    },
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "extensions/nextcloud-talk",
      "defaultChoice": "npm"
    }
  }
}
```

OpenClaw 还可以合并**外部渠道目录**（例如，MPM 注册表导出）。将 JSON 文件放在以下位置之一：

- `~/.openclaw/mpm/plugins.json`
- `~/.openclaw/mpm/catalog.json`
- `~/.openclaw/plugins/catalog.json`

或将 `OPENCLAW_PLUGIN_CATALOG_PATHS`（或 `OPENCLAW_MPM_CATALOG_PATHS`）指向一个或多个 JSON 文件（逗号/分号/`PATH` 分隔）。每个文件应包含 `{ "entries": [ { "name": "@scope/pkg", "openclaw": { "channel": {...}, "install": {...} } } ] }`。

## 插件 ID

默认插件 id：

- 包集合：`package.json` 的 `name`
- 独立文件：文件基本名称（`~/.../voice-call.ts` → `voice-call`）

如果插件导出 `id`，OpenClaw 会使用它，但当它与配置的 id 不匹配时会发出警告。

## 配置

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-extension"] },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } },
    },
  },
}
```

字段：

- `enabled`：主开关（默认：true）
- `allow`：允许列表（可选）
- `deny`：拒绝列表（可选；deny 优先）
- `load.paths`：额外的插件文件/目录
- `entries.<id>`：每个插件的开关 + 配置

配置更改**需要重启 Gateway 网关**。

验证规则（严格）：

- `entries`、`allow`、`deny` 或 `slots` 中的未知插件 id 是**错误**。
- 未知的 `channels.<id>` 键是**错误**，除非插件清单声明了渠道 id。
- 插件配置使用嵌入在 `openclaw.plugin.json`（`configSchema`）中的 JSON Schema 进行验证。
- 如果插件被禁用，其配置会保留并发出**警告**。

## 插件槽位（独占类别）

某些插件类别是**独占的**（一次只有一个活跃）。使用 `plugins.slots` 选择哪个插件拥有该槽位：

```json5
{
  plugins: {
    slots: {
      memory: "memory-core", // or "none" to disable memory plugins
    },
  },
}
```

如果多个插件声明 `kind: "memory"`，只有选定的那个加载。其他的被禁用并带有诊断信息。

## 控制界面（schema + 标签）

控制界面使用 `config.schema`（JSON Schema + `uiHints`）来渲染更好的表单。

OpenClaw 在运行时根据发现的插件增强 `uiHints`：

- 为 `plugins.entries.<id>` / `.enabled` / `.config` 添加每插件标签
- 在以下位置合并可选的插件提供的配置字段提示：
  `plugins.entries.<id>.config.<field>`

如果你希望插件配置字段显示良好的标签/占位符（并将密钥标记为敏感），请在插件清单中提供 `uiHints` 和 JSON Schema。

示例：

```json
{
  "id": "my-plugin",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" },
      "region": { "type": "string" }
    }
  },
  "uiHints": {
    "apiKey": { "label": "API Key", "sensitive": true },
    "region": { "label": "Region", "placeholder": "us-east-1" }
  }
}
```

## CLI

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins install <path>                 # copy a local file/dir into ~/.openclaw/extensions/<id>
openclaw plugins install ./extensions/voice-call # relative path ok
openclaw plugins install ./plugin.tgz           # install from a local tarball
openclaw plugins install ./plugin.zip           # install from a local zip
openclaw plugins install -l ./extensions/voice-call # link (no copy) for dev
openclaw plugins install @openclaw/voice-call # install from npm
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

`plugins update` 仅适用于在 `plugins.installs` 下跟踪的 npm 安装。

插件也可以注册自己的顶级命令（例如：`openclaw voicecall`）。

## 插件 API（概述）

插件导出以下之一：

- 函数：`(api) => { ... }`
- 对象：`{ id, name, configSchema, register(api) { ... } }`

## 插件钩子

插件可以附带钩子并在运行时注册它们。这让插件可以捆绑事件驱动的自动化，而无需单独安装钩子包。

### 示例

```
import { registerPluginHooksFromDir } from "openclaw/plugin-sdk";

export default function register(api) {
  registerPluginHooksFromDir(api, "./hooks");
}
```

注意事项：

- 钩子目录遵循正常的钩子结构（`HOOK.md` + `handler.ts`）。
- 钩子资格规则仍然适用（操作系统/二进制文件/环境/配置要求）。
- 插件管理的钩子在 `openclaw hooks list` 中显示为 `plugin:<id>`。
- 你不能通过 `openclaw hooks` 启用/禁用插件管理的钩子；而是启用/禁用插件。

## 提供商插件（模型认证）

插件可以注册**模型提供商认证**流程，以便用户可以在 OpenClaw 内运行 OAuth 或 API 密钥设置（无需外部脚本）。

通过 `api.registerProvider(...)` 注册提供商。每个提供商暴露一个或多个认证方法（OAuth、API 密钥、设备码等）。这些方法驱动：

- `openclaw models auth login --provider <id> [--method <id>]`

示例：

```ts
api.registerProvider({
  id: "acme",
  label: "AcmeAI",
  auth: [
    {
      id: "oauth",
      label: "OAuth",
      kind: "oauth",
      run: async (ctx) => {
        // Run OAuth flow and return auth profiles.
        return {
          profiles: [
            {
              profileId: "acme:default",
              credential: {
                type: "oauth",
                provider: "acme",
                access: "...",
                refresh: "...",
                expires: Date.now() + 3600 * 1000,
              },
            },
          ],
          defaultModel: "acme/opus-1",
        };
      },
    },
  ],
});
```

注意事项：

- `run` 接收带有 `prompter`、`runtime`、`openUrl` 和 `oauth.createVpsAwareHandlers` 辅助工具的 `ProviderAuthContext`。
- 当需要添加默认模型或提供商配置时返回 `configPatch`。
- 返回 `defaultModel` 以便 `--set-default` 可以更新智能体默认值。

### 注册消息渠道

插件可以注册**渠道插件**，其行为类似于内置渠道（WhatsApp、Telegram 等）。渠道配置位于 `channels.<id>` 下，由你的渠道插件代码验证。

```ts
const myChannel = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "demo channel plugin.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async () => ({ ok: true }),
  },
};

export default function (api) {
  api.registerChannel({ plugin: myChannel });
}
```

注意事项：

- 将配置放在 `channels.<id>` 下（而不是 `plugins.entries`）。
- `meta.label` 用于 CLI/UI 列表中的标签。
- `meta.aliases` 添加用于规范化和 CLI 输入的备用 id。
- `meta.preferOver` 列出当两者都配置时要跳过自动启用的渠道 id。
- `meta.detailLabel` 和 `meta.systemImage` 让 UI 显示更丰富的渠道标签/图标。

### 编写新的消息渠道（分步指南）

当你想要一个**新的聊天界面**（"消息渠道"）而不是模型提供商时使用此方法。
模型提供商文档位于 `/providers/*` 下。

1. 选择 id + 配置结构

- 所有渠道配置位于 `channels.<id>` 下。
- 对于多账户设置，优先使用 `channels.<id>.accounts.<accountId>`。

2. 定义渠道元数据

- `meta.label`、`meta.selectionLabel`、`meta.docsPath`、`meta.blurb` 控制 CLI/UI 列表。
- `meta.docsPath` 应指向像 `/channels/<id>` 这样的文档页面。
- `meta.preferOver` 让插件替换另一个渠道（自动启用优先选择它）。
- `meta.detailLabel` 和 `meta.systemImage` 被 UI 用于详细文本/图标。

3. 实现必需的适配器

- `config.listAccountIds` + `config.resolveAccount`
- `capabilities`（聊天类型、媒体、线程等）
- `outbound.deliveryMode` + `outbound.sendText`（用于基本发送）

4. 根据需要添加可选适配器

- `setup`（向导）、`security`（私信策略）、`status`（健康/诊断）
- `gateway`（启动/停止/登录）、`mentions`、`threading`、`streaming`
- `actions`（消息操作）、`commands`（原生命令行为）

5. 在插件中注册渠道

- `api.registerChannel({ plugin })`

最小配置示例：

```json5
{
  channels: {
    acmechat: {
      accounts: {
        default: { token: "ACME_TOKEN", enabled: true },
      },
    },
  },
}
```

最小渠道插件（仅出站）：

```ts
const plugin = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "AcmeChat messaging channel.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async ({ text }) => {
      // deliver `text` to your channel here
      return { ok: true };
    },
  },
};

export default function (api) {
  api.registerChannel({ plugin });
}
```

加载插件（扩展目录或 `plugins.load.paths`），重启 Gateway 网关，然后在配置中配置 `channels.<id>`。

### 智能体工具

参见专门指南：[插件智能体工具](/plugins/agent-tools)。

### 注册 Gateway 网关 RPC 方法

```ts
export default function (api) {
  api.registerGatewayMethod("myplugin.status", ({ respond }) => {
    respond(true, { ok: true });
  });
}
```

### 注册 CLI 命令

```ts
export default function (api) {
  api.registerCli(
    ({ program }) => {
      program.command("mycmd").action(() => {
        console.log("Hello");
      });
    },
    { commands: ["mycmd"] },
  );
}
```

### 注册自动回复命令

插件可以注册自定义斜杠命令，**无需调用 AI 智能体**即可执行。这对于切换命令、状态检查或不需要 LLM 处理的快速操作很有用。

```ts
export default function (api) {
  api.registerCommand({
    name: "mystatus",
    description: "Show plugin status",
    handler: (ctx) => ({
      text: `Plugin is running! Channel: ${ctx.channel}`,
    }),
  });
}
```

命令处理程序上下文：

- `senderId`：发送者的 ID（如可用）
- `channel`：发送命令的渠道
- `isAuthorizedSender`：发送者是否是授权用户
- `args`：命令后传递的参数（如果 `acceptsArgs: true`）
- `commandBody`：完整的命令文本
- `config`：当前 OpenClaw 配置

命令选项：

- `name`：命令名称（不带前导 `/`）
- `description`：命令列表中显示的帮助文本
- `acceptsArgs`：命令是否接受参数（默认：false）。如果为 false 且提供了参数，命令不会匹配，消息会传递给其他处理程序
- `requireAuth`：是否需要授权发送者（默认：true）
- `handler`：返回 `{ text: string }` 的函数（可以是异步的）

带授权和参数的示例：

```ts
api.registerCommand({
  name: "setmode",
  description: "Set plugin mode",
  acceptsArgs: true,
  requireAuth: true,
  handler: async (ctx) => {
    const mode = ctx.args?.trim() || "default";
    await saveMode(mode);
    return { text: `Mode set to: ${mode}` };
  },
});
```

注意事项：

- 插件命令在内置命令和 AI 智能体**之前**处理
- 命令全局注册，适用于所有渠道
- 命令名称不区分大小写（`/MyStatus` 匹配 `/mystatus`）
- 命令名称必须以字母开头，只能包含字母、数字、连字符和下划线
- 保留的命令名称（如 `help`、`status`、`reset` 等）不能被插件覆盖
- 跨插件的重复命令注册将失败并显示诊断错误

### 注册后台服务

```ts
export default function (api) {
  api.registerService({
    id: "my-service",
    start: () => api.logger.info("ready"),
    stop: () => api.logger.info("bye"),
  });
}
```

## 命名约定

- Gateway 网关方法：`pluginId.action`（例如：`voicecall.status`）
- 工具：`snake_case`（例如：`voice_call`）
- CLI 命令：kebab 或 camel，但避免与核心命令冲突

## Skills

插件可以在仓库中附带 Skills（`skills/<name>/SKILL.md`）。
使用 `plugins.entries.<id>.enabled`（或其他配置门控）启用它，并确保它存在于你的工作区/托管 Skills 位置。

## 分发（npm）

推荐的打包方式：

- 主包：`openclaw`（本仓库）
- 插件：`@openclaw/*` 下的独立 npm 包（例如：`@openclaw/voice-call`）

发布契约：

- 插件 `package.json` 必须包含带有一个或多个入口文件的 `openclaw.extensions`。
- 入口文件可以是 `.js` 或 `.ts`（jiti 在运行时加载 TS）。
- `openclaw plugins install <npm-spec>` 使用 `npm pack`，提取到 `~/.openclaw/extensions/<id>/`，并在配置中启用它。
- 配置键稳定性：作用域包被规范化为 `plugins.entries.*` 的**无作用域** id。

## 示例插件：Voice Call

本仓库包含一个语音通话插件（Twilio 或 log 回退）：

- 源码：`extensions/voice-call`
- Skills：`skills/voice-call`
- CLI：`openclaw voicecall start|status`
- 工具：`voice_call`
- RPC：`voicecall.start`、`voicecall.status`
- 配置（twilio）：`provider: "twilio"` + `twilio.accountSid/authToken/from`（可选 `statusCallbackUrl`、`twimlUrl`）
- 配置（dev）：`provider: "log"`（无网络）

参见 [Voice Call](/plugins/voice-call) 和 `extensions/voice-call/README.md` 了解设置和用法。

## 安全注意事项

插件与 Gateway 网关在同一进程中运行。将它们视为受信任的代码：

- 只安装你信任的插件。
- 优先使用 `plugins.allow` 允许列表。
- 更改后重启 Gateway 网关。

## 测试插件

插件可以（也应该）附带测试：

- 仓库内插件可以在 `src/**` 下保留 Vitest 测试（例如：`src/plugins/voice-call.plugin.test.ts`）。
- 单独发布的插件应运行自己的 CI（lint/构建/测试）并验证 `openclaw.extensions` 指向构建的入口点（`dist/index.js`）。


---
# File: docs/zh-CN/tools/reactions.md

---
read_when:
  - 在任何渠道中处理表情回应相关工作
summary: 跨渠道共享的表情回应语义
title: 表情回应
x-i18n:
  generated_at: "2026-02-01T21:42:41Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0f11bff9adb4bd02604f96ebe2573a623702796732b6e17dfeda399cb7be0fa6
  source_path: tools/reactions.md
  workflow: 15
---

# 表情回应工具

跨渠道共享的表情回应语义：

- 添加表情回应时，`emoji` 为必填项。
- `emoji=""` 在支持的情况下移除机器人的表情回应。
- `remove: true` 在支持的情况下移除指定的表情（需要提供 `emoji`）。

渠道说明：

- **Discord/Slack**：空 `emoji` 移除机器人在该消息上的所有表情回应；`remove: true` 仅移除指定的表情。
- **Google Chat**：空 `emoji` 移除应用在该消息上的表情回应；`remove: true` 仅移除指定的表情。
- **Telegram**：空 `emoji` 移除机器人的表情回应；`remove: true` 同样移除表情回应，但工具验证仍要求 `emoji` 为非空值。
- **WhatsApp**：空 `emoji` 移除机器人的表情回应；`remove: true` 映射为空 emoji（仍需提供 `emoji`）。
- **Signal**：当启用 `channels.signal.reactionNotifications` 时，收到的表情回应通知会触发系统事件。


---
# File: docs/zh-CN/tools/skills-config.md

---
read_when:
  - 添加或修改 Skills 配置
  - 调整内置白名单或安装行为
summary: Skills 配置 schema 和示例
title: Skills 配置
x-i18n:
  generated_at: "2026-02-03T10:10:59Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e265c93da7856887c11abd92b379349181549e1a02164184d61a8d1f6b2feed5
  source_path: tools/skills-config.md
  workflow: 15
---

# Skills 配置

所有 Skills 相关配置都位于 `~/.openclaw/openclaw.json` 中的 `skills` 下。

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun（Gateway 网关运行时仍为 Node；不推荐 bun）
    },
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

## 字段

- `allowBundled`：可选的仅用于**内置** Skills 的白名单。设置后，只有列表中的内置 Skills 才有资格（托管/工作区 Skills 不受影响）。
- `load.extraDirs`：要扫描的附加 Skills 目录（最低优先级）。
- `load.watch`：监视 Skills 文件夹并刷新 Skills 快照（默认：true）。
- `load.watchDebounceMs`：Skills 监视器事件的防抖时间（毫秒）（默认：250）。
- `install.preferBrew`：在可用时优先使用 brew 安装器（默认：true）。
- `install.nodeManager`：node 安装器偏好（`npm` | `pnpm` | `yarn` | `bun`，默认：npm）。这仅影响 **Skills 安装**；Gateway 网关运行时应仍为 Node（不推荐 Bun 用于 WhatsApp/Telegram）。
- `entries.<skillKey>`：单 Skills 覆盖。

单 Skills 字段：

- `enabled`：设置为 `false` 以禁用某个 Skills，即使它是内置/已安装的。
- `env`：为智能体运行注入的环境变量（仅在尚未设置时）。
- `apiKey`：可选的便捷字段，用于声明主环境变量的 Skills。

## 注意事项

- `entries` 下的键默认映射到 Skills 名称。如果 Skills 定义了 `metadata.openclaw.skillKey`，则使用该键。
- 启用监视器后，Skills 的更改会在下一个智能体轮次被获取。

### 沙箱隔离的 Skills + 环境变量

当会话处于**沙箱隔离**状态时，Skills 进程在 Docker 内运行。沙箱**不会**继承宿主机的 `process.env`。

使用以下方式之一：

- `agents.defaults.sandbox.docker.env`（或单智能体的 `agents.list[].sandbox.docker.env`）
- 将环境变量烘焙到你的自定义沙箱镜像中

全局 `env` 和 `skills.entries.<skill>.env/apiKey` 仅适用于**宿主机**运行。


---
# File: docs/zh-CN/tools/skills.md

---
read_when:
  - 添加或修改 Skills
  - 更改 Skills 门控或加载规则
summary: Skills：托管与工作区、门控规则以及配置/环境变量连接
title: Skills
x-i18n:
  generated_at: "2026-02-03T10:12:27Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 54685da5885600b367ccdad6342497199fcb168ce33f8cdc00391d993f3bab7e
  source_path: tools/skills.md
  workflow: 15
---

# Skills（OpenClaw）

OpenClaw 使用**兼容 [AgentSkills](https://agentskills.io)** 的 Skills 文件夹来教智能体如何使用工具。每个 Skills 是一个包含带有 YAML frontmatter 和说明的 `SKILL.md` 的目录。OpenClaw 加载**内置 Skills** 以及可选的本地覆盖，并在加载时根据环境、配置和二进制文件存在情况进行过滤。

## 位置和优先级

Skills 从**三个**位置加载：

1. **内置 Skills**：随安装包一起发布（npm 包或 OpenClaw.app）
2. **托管/本地 Skills**：`~/.openclaw/skills`
3. **工作区 Skills**：`<workspace>/skills`

如果 Skills 名称冲突，优先级为：

`<workspace>/skills`（最高）→ `~/.openclaw/skills` → 内置 Skills（最低）

此外，你可以通过 `~/.openclaw/openclaw.json` 中的 `skills.load.extraDirs` 配置额外的 Skills 文件夹（最低优先级）。

## 单智能体 vs 共享 Skills

在**多智能体**设置中，每个智能体有自己的工作区。这意味着：

- **单智能体 Skills** 位于 `<workspace>/skills` 中，仅供该智能体使用。
- **共享 Skills** 位于 `~/.openclaw/skills`（托管/本地），对同一机器上的**所有智能体**可见。
- 如果你想要多个智能体使用一个通用的 Skills 包，也可以通过 `skills.load.extraDirs`（最低优先级）添加**共享文件夹**。

如果同一个 Skills 名称存在于多个位置，将应用通常的优先级规则：工作区优先，然后是托管/本地，最后是内置。

## 插件 + Skills

插件可以通过在 `openclaw.plugin.json` 中列出 `skills` 目录（相对于插件根目录的路径）来发布自己的 Skills。插件 Skills 在插件启用时加载，并参与正常的 Skills 优先级规则。你可以通过插件配置条目上的 `metadata.openclaw.requires.config` 对它们进行门控。参见[插件](/tools/plugin)了解发现/配置，以及[工具](/tools)了解这些 Skills 所教授的工具接口。

## ClawHub（安装 + 同步）

ClawHub 是 OpenClaw 的公共 Skills 注册表。浏览 https://clawhub.com。使用它来发现、安装、更新和备份 Skills。完整指南：[ClawHub](/tools/clawhub)。

常见流程：

- 将 Skills 安装到你的工作区：
  - `clawhub install <skill-slug>`
- 更新所有已安装的 Skills：
  - `clawhub update --all`
- 同步（扫描 + 发布更新）：
  - `clawhub sync --all`

默认情况下，`clawhub` 安装到当前工作目录下的 `./skills`（或回退到配置的 OpenClaw 工作区）。OpenClaw 在下一个会话中将其识别为 `<workspace>/skills`。

## 安全注意事项

- 将第三方 Skills 视为**不受信任的代码**。启用前请阅读它们。
- 对于不受信任的输入和高风险工具，优先使用沙箱隔离运行。参见[沙箱隔离](/gateway/sandboxing)。
- `skills.entries.*.env` 和 `skills.entries.*.apiKey` 为该智能体轮次将秘密注入到**宿主机**进程中（而非沙箱）。将秘密保持在提示词和日志之外。
- 有关更广泛的威胁模型和检查清单，参见[安全性](/gateway/security)。

## 格式（AgentSkills + Pi 兼容）

`SKILL.md` 必须至少包含：

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
---
```

注意事项：

- 我们遵循 AgentSkills 规范的布局/意图。
- 内嵌智能体使用的解析器仅支持**单行** frontmatter 键。
- `metadata` 应该是**单行 JSON 对象**。
- 在说明中使用 `{baseDir}` 来引用 Skills 文件夹路径。
- 可选的 frontmatter 键：
  - `homepage` — 在 macOS Skills UI 中显示为"Website"的 URL（也支持通过 `metadata.openclaw.homepage`）。
  - `user-invocable` — `true|false`（默认：`true`）。当为 `true` 时，Skills 作为用户斜杠命令暴露。
  - `disable-model-invocation` — `true|false`（默认：`false`）。当为 `true` 时，Skills 从模型提示词中排除（仍可通过用户调用使用）。
  - `command-dispatch` — `tool`（可选）。当设置为 `tool` 时，斜杠命令绕过模型直接调度到工具。
  - `command-tool` — 当设置 `command-dispatch: tool` 时要调用的工具名称。
  - `command-arg-mode` — `raw`（默认）。对于工具调度，将原始参数字符串转发到工具（无核心解析）。

    工具使用以下参数调用：
    `{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`。

## 门控（加载时过滤）

OpenClaw 使用 `metadata`（单行 JSON）**在加载时过滤 Skills**：

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
      },
  }
---
```

`metadata.openclaw` 下的字段：

- `always: true` — 始终包含该 Skills（跳过其他门控）。
- `emoji` — macOS Skills UI 使用的可选表情符号。
- `homepage` — 在 macOS Skills UI 中显示为"Website"的可选 URL。
- `os` — 可选的平台列表（`darwin`、`linux`、`win32`）。如果设置，该 Skills 仅在这些操作系统上有资格。
- `requires.bins` — 列表；每个都必须存在于 `PATH` 中。
- `requires.anyBins` — 列表；至少一个必须存在于 `PATH` 中。
- `requires.env` — 列表；环境变量必须存在**或**在配置中提供。
- `requires.config` — `openclaw.json` 路径列表，必须为真值。
- `primaryEnv` — 与 `skills.entries.<name>.apiKey` 关联的环境变量名称。
- `install` — macOS Skills UI 使用的可选安装器规格数组（brew/node/go/uv/download）。

沙箱隔离注意事项：

- `requires.bins` 在 Skills 加载时在**宿主机**上检查。
- 如果智能体处于沙箱隔离状态，二进制文件也必须存在于**容器内部**。通过 `agents.defaults.sandbox.docker.setupCommand`（或自定义镜像）安装它。`setupCommand` 在容器创建后运行一次。包安装还需要网络出口、可写的根文件系统和沙箱中的 root 用户。示例：`summarize` Skills（`skills/summarize/SKILL.md`）需要 `summarize` CLI 在沙箱容器中才能运行。

安装器示例：

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

注意事项：

- 如果列出了多个安装器，Gateway 网关会选择**单个**首选选项（可用时选择 brew，否则选择 node）。
- 如果所有安装器都是 `download`，OpenClaw 会列出每个条目，以便你查看可用的构件。
- 安装器规格可以包含 `os: ["darwin"|"linux"|"win32"]` 按平台过滤选项。
- Node 安装遵循 `openclaw.json` 中的 `skills.install.nodeManager`（默认：npm；选项：npm/pnpm/yarn/bun）。这仅影响 **Skills 安装**；Gateway 网关运行时应仍为 Node（不推荐 Bun 用于 WhatsApp/Telegram）。
- Go 安装：如果缺少 `go` 且 `brew` 可用，Gateway 网关会首先通过 Homebrew 安装 Go，并在可能时将 `GOBIN` 设置为 Homebrew 的 `bin`。
- Download 安装：`url`（必填）、`archive`（`tar.gz` | `tar.bz2` | `zip`）、`extract`（默认：检测到归档时自动）、`stripComponents`、`targetDir`（默认：`~/.openclaw/tools/<skillKey>`）。

如果没有 `metadata.openclaw`，该 Skills 始终有资格（除非在配置中禁用或被 `skills.allowBundled` 阻止用于内置 Skills）。

## 配置覆盖（`~/.openclaw/openclaw.json`）

内置/托管 Skills 可以被切换并提供环境变量值：

```json5
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
        config: {
          endpoint: "https://example.invalid",
          model: "nano-pro",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

注意：如果 Skills 名称包含连字符，请用引号括起键名（JSON5 允许带引号的键名）。

配置键默认匹配 **Skills 名称**。如果 Skills 定义了 `metadata.openclaw.skillKey`，请在 `skills.entries` 下使用该键。

规则：

- `enabled: false` 禁用该 Skills，即使它是内置/已安装的。
- `env`：**仅在**变量在进程中尚未设置时注入。
- `apiKey`：为声明 `metadata.openclaw.primaryEnv` 的 Skills 提供的便捷字段。
- `config`：用于自定义单 Skills 字段的可选容器；自定义键必须放在这里。
- `allowBundled`：可选的仅用于**内置** Skills 的白名单。如果设置，只有列表中的内置 Skills 才有资格（托管/工作区 Skills 不受影响）。

## 环境变量注入（每次智能体运行）

当智能体运行开始时，OpenClaw：

1. 读取 Skills 元数据。
2. 将任何 `skills.entries.<key>.env` 或 `skills.entries.<key>.apiKey` 应用到 `process.env`。
3. 使用**有资格的** Skills 构建系统提示词。
4. 在运行结束后恢复原始环境。

这是**限定于智能体运行范围内的**，不是全局 shell 环境。

## 会话快照（性能）

OpenClaw 在**会话开始时**对有资格的 Skills 进行快照，并在同一会话的后续轮次中重用该列表。对 Skills 或配置的更改在下一个新会话中生效。

当 Skills 监视器启用或出现新的有资格的远程节点时，Skills 也可以在会话中刷新（见下文）。将此视为**热重载**：刷新后的列表会在下一个智能体轮次被获取。

## 远程 macOS 节点（Linux Gateway 网关）

如果 Gateway 网关运行在 Linux 上但连接了一个**允许 `system.run` 的 macOS 节点**（Exec 批准安全设置未设为 `deny`），当所需的二进制文件存在于该节点上时，OpenClaw 可以将仅限 macOS 的 Skills 视为有资格。智能体应通过 `nodes` 工具（通常是 `nodes.run`）执行这些 Skills。

这依赖于节点报告其命令支持以及通过 `system.run` 进行的二进制文件探测。如果 macOS 节点稍后离线，Skills 仍然可见；调用可能会失败，直到节点重新连接。

## Skills 监视器（自动刷新）

默认情况下，OpenClaw 监视 Skills 文件夹，并在 `SKILL.md` 文件更改时更新 Skills 快照。在 `skills.load` 下配置：

```json5
{
  skills: {
    load: {
      watch: true,
      watchDebounceMs: 250,
    },
  },
}
```

## Token 影响（Skills 列表）

当 Skills 有资格时，OpenClaw 将可用 Skills 的紧凑 XML 列表注入到系统提示词中（通过 `pi-coding-agent` 中的 `formatSkillsForPrompt`）。成本是确定性的：

- **基础开销（仅当 ≥1 个 Skills 时）：** 195 字符。
- **每个 Skills：** 97 字符 + XML 转义的 `<name>`、`<description>` 和 `<location>` 值的长度。

公式（字符）：

```
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

注意事项：

- XML 转义将 `& < > " '` 扩展为实体（`&amp;`、`&lt;` 等），增加长度。
- Token 数量因模型分词器而异。粗略的 OpenAI 风格估计是 ~4 字符/token，所以**每个 Skills 97 字符 ≈ 24 token** 加上你的实际字段长度。

## 托管 Skills 生命周期

OpenClaw 作为安装的一部分（npm 包或 OpenClaw.app）发布一组基线 Skills 作为**内置 Skills**。`~/.openclaw/skills` 用于本地覆盖（例如，在不更改内置副本的情况下固定/修补 Skills）。工作区 Skills 由用户拥有，在名称冲突时覆盖两者。

## 配置参考

参见 [Skills 配置](/tools/skills-config)了解完整的配置 schema。

## 寻找更多 Skills？

浏览 https://clawhub.com。

---


---
# File: docs/zh-CN/tools/slash-commands.md

---
read_when:
  - 使用或配置聊天命令
  - 调试命令路由或权限
summary: 斜杠命令：文本 vs 原生、配置和支持的命令
title: 斜杠命令
x-i18n:
  generated_at: "2026-02-03T10:12:40Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ca0deebf89518e8c62828fbb9bf4621c5fff8ab86ccb22e37da61a28f9a7886a
  source_path: tools/slash-commands.md
  workflow: 15
---

# 斜杠命令

命令由 Gateway 网关处理。大多数命令必须作为以 `/` 开头的**独立**消息发送。
仅主机的 bash 聊天命令使用 `! <cmd>`（`/bash <cmd>` 是别名）。

有两个相关系统：

- **命令**：独立的 `/...` 消息。
- **指令**：`/think`、`/verbose`、`/reasoning`、`/elevated`、`/exec`、`/model`、`/queue`。
  - 指令在模型看到消息之前被剥离。
  - 在普通聊天消息中（不是仅指令消息），它们被视为"内联提示"，**不会**持久化会话设置。
  - 在仅指令消息中（消息只包含指令），它们会持久化到会话并回复确认。
  - 指令仅对**授权发送者**生效（渠道白名单/配对加上 `commands.useAccessGroups`）。
    未授权发送者的指令被视为纯文本。

还有一些**内联快捷方式**（仅限白名单/授权发送者）：`/help`、`/commands`、`/status`、`/whoami`（`/id`）。
它们立即运行，在模型看到消息之前被剥离，剩余文本继续通过正常流程。

## 配置

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    debug: false,
    restart: false,
    useAccessGroups: true,
  },
}
```

- `commands.text`（默认 `true`）启用解析聊天消息中的 `/...`。
  - 在没有原生命令的平台上（WhatsApp/WebChat/Signal/iMessage/Google Chat/MS Teams），即使你将此设置为 `false`，文本命令仍然有效。
- `commands.native`（默认 `"auto"`）注册原生命令。
  - Auto：在 Discord/Telegram 上启用；在 Slack 上禁用（直到你添加斜杠命令）；在不支持原生命令的提供商上忽略。
  - 设置 `channels.discord.commands.native`、`channels.telegram.commands.native` 或 `channels.slack.commands.native` 以按提供商覆盖（布尔值或 `"auto"`）。
  - `false` 在启动时清除 Discord/Telegram 上之前注册的命令。Slack 命令在 Slack 应用中管理，不会自动删除。
- `commands.nativeSkills`（默认 `"auto"`）在支持时原生注册 **Skill** 命令。
  - Auto：在 Discord/Telegram 上启用；在 Slack 上禁用（Slack 需要为每个 Skill 创建一个斜杠命令）。
  - 设置 `channels.discord.commands.nativeSkills`、`channels.telegram.commands.nativeSkills` 或 `channels.slack.commands.nativeSkills` 以按提供商覆盖（布尔值或 `"auto"`）。
- `commands.bash`（默认 `false`）启用 `! <cmd>` 来运行主机 shell 命令（`/bash <cmd>` 是别名；需要 `tools.elevated` 白名单）。
- `commands.bashForegroundMs`（默认 `2000`）控制 bash 切换到后台模式之前等待多长时间（`0` 立即后台运行）。
- `commands.config`（默认 `false`）启用 `/config`（读写 `openclaw.json`）。
- `commands.debug`（默认 `false`）启用 `/debug`（仅运行时覆盖）。
- `commands.useAccessGroups`（默认 `true`）对命令强制执行白名单/策略。

## 命令列表

文本 + 原生（启用时）：

- `/help`
- `/commands`
- `/skill <name> [input]`（按名称运行 Skill）
- `/status`（显示当前状态；在可用时包含当前模型提供商的提供商使用量/配额）
- `/allowlist`（列出/添加/删除白名单条目）
- `/approve <id> allow-once|allow-always|deny`（解决 exec 审批提示）
- `/context [list|detail|json]`（解释"上下文"；`detail` 显示每个文件 + 每个工具 + 每个 Skill + 系统提示词大小）
- `/whoami`（显示你的发送者 ID；别名：`/id`）
- `/subagents list|kill|log|info|send|steer|spawn`（检查、控制或创建当前会话的子智能体运行）
- `/config show|get|set|unset`（将配置持久化到磁盘，仅所有者；需要 `commands.config: true`）
- `/debug show|set|unset|reset`（运行时覆盖，仅所有者；需要 `commands.debug: true`）
- `/usage off|tokens|full|cost`（每响应使用量页脚或本地成本摘要）
- `/tts off|always|inbound|tagged|status|provider|limit|summary|audio`（控制 TTS；参见 [/tts](/tts)）
  - Discord：原生命令是 `/voice`（Discord 保留了 `/tts`）；文本 `/tts` 仍然有效。
- `/stop`
- `/restart`
- `/dock-telegram`（别名：`/dock_telegram`）（将回复切换到 Telegram）
- `/dock-discord`（别名：`/dock_discord`）（将回复切换到 Discord）
- `/dock-slack`（别名：`/dock_slack`）（将回复切换到 Slack）
- `/activation mention|always`（仅限群组）
- `/send on|off|inherit`（仅所有者）
- `/reset` 或 `/new [model]`（可选模型提示；其余部分传递）
- `/think <off|minimal|low|medium|high|xhigh>`（按模型/提供商动态选择；别名：`/thinking`、`/t`）
- `/verbose on|full|off`（别名：`/v`）
- `/reasoning on|off|stream`（别名：`/reason`；启用时，发送带有 `Reasoning:` 前缀的单独消息；`stream` = 仅 Telegram 草稿）
- `/elevated on|off|ask|full`（别名：`/elev`；`full` 跳过 exec 审批）
- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>`（发送 `/exec` 显示当前设置）
- `/model <name>`（别名：`/models`；或 `agents.defaults.models.*.alias` 中的 `/<alias>`）
- `/queue <mode>`（加上选项如 `debounce:2s cap:25 drop:summarize`；发送 `/queue` 查看当前设置）
- `/bash <command>`（仅主机；`! <command>` 的别名；需要 `commands.bash: true` + `tools.elevated` 白名单）

仅文本：

- `/compact [instructions]`（参见 [/concepts/compaction](/concepts/compaction)）
- `! <command>`（仅主机；一次一个；对长时间运行的任务使用 `!poll` + `!stop`）
- `!poll`（检查输出/状态；接受可选的 `sessionId`；`/bash poll` 也可用）
- `!stop`（停止正在运行的 bash 任务；接受可选的 `sessionId`；`/bash stop` 也可用）

注意事项：

- 命令接受命令和参数之间的可选 `:`（例如 `/think: high`、`/send: on`、`/help:`）。
- `/new <model>` 接受模型别名、`provider/model` 或提供商名称（模糊匹配）；如果没有匹配，文本被视为消息正文。
- 要获取完整的提供商使用量分解，使用 `openclaw status --usage`。
- `/allowlist add|remove` 需要 `commands.config=true` 并遵循渠道 `configWrites`。
- `/usage` 控制每响应使用量页脚；`/usage cost` 从 OpenClaw 会话日志打印本地成本摘要。
- `/restart` 默认禁用；设置 `commands.restart: true` 启用它。
- `/verbose` 用于调试和额外可见性；在正常使用中保持**关闭**。
- `/reasoning`（和 `/verbose`）在群组设置中有风险：它们可能会暴露你不打算公开的内部推理或工具输出。最好保持关闭，尤其是在群聊中。
- **快速路径：** 来自白名单发送者的仅命令消息会立即处理（绕过队列 + 模型）。
- **群组提及门控：** 来自白名单发送者的仅命令消息绕过提及要求。
- **内联快捷方式（仅限白名单发送者）：** 某些命令在嵌入普通消息时也能工作，并在模型看到剩余文本之前被剥离。
  - 示例：`hey /status` 触发状态回复，剩余文本继续通过正常流程。
- 目前：`/help`、`/commands`、`/status`、`/whoami`（`/id`）。
- 未授权的仅命令消息被静默忽略，内联 `/...` 令牌被视为纯文本。
- **Skill 命令：** `user-invocable` Skills 作为斜杠命令公开。名称被清理为 `a-z0-9_`（最多 32 个字符）；冲突获得数字后缀（例如 `_2`）。
  - `/skill <name> [input]` 按名称运行 Skill（当原生命令限制阻止每个 Skill 命令时有用）。
  - 默认情况下，Skill 命令作为普通请求转发给模型。
  - Skills 可以选择声明 `command-dispatch: tool` 将命令直接路由到工具（确定性，无模型）。
  - 示例：`/prose`（OpenProse 插件）— 参见 [OpenProse](/prose)。
- **原生命令参数：** Discord 使用自动完成进行动态选项（以及当你省略必需参数时的按钮菜单）。当命令支持选择且你省略参数时，Telegram 和 Slack 显示按钮菜单。

## 使用量显示（什么显示在哪里）

- **提供商使用量/配额**（示例："Claude 80% left"）在启用使用量跟踪时显示在 `/status` 中，针对当前模型提供商。
- **每响应令牌/成本**由 `/usage off|tokens|full` 控制（附加到普通回复）。
- `/model status` 是关于**模型/认证/端点**的，不是使用量。

## 模型选择（`/model`）

`/model` 作为指令实现。

示例：

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model opus@anthropic:default
/model status
```

注意事项：

- `/model` 和 `/model list` 显示紧凑的编号选择器（模型系列 + 可用提供商）。
- `/model <#>` 从该选择器中选择（并在可能时优先选择当前提供商）。
- `/model status` 显示详细视图，包括在可用时配置的提供商端点（`baseUrl`）和 API 模式（`api`）。

## 调试覆盖

`/debug` 让你设置**仅运行时**的配置覆盖（内存，不写磁盘）。仅所有者。默认禁用；使用 `commands.debug: true` 启用。

示例：

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug set channels.whatsapp.allowFrom=["+1555","+4477"]
/debug unset messages.responsePrefix
/debug reset
```

注意事项：

- 覆盖立即应用于新的配置读取，但**不会**写入 `openclaw.json`。
- 使用 `/debug reset` 清除所有覆盖并返回到磁盘上的配置。

## 配置更新

`/config` 写入你的磁盘配置（`openclaw.json`）。仅所有者。默认禁用；使用 `commands.config: true` 启用。

示例：

```
/config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix="[openclaw]"
/config unset messages.responsePrefix
```

注意事项：

- 配置在写入前会验证；无效更改会被拒绝。
- `/config` 更新在重启后持久化。

## 平台注意事项

- **文本命令**在普通聊天会话中运行（私信共享 `main`，群组有自己的会话）。
- **原生命令**使用隔离的会话：
  - Discord：`agent:<agentId>:discord:slash:<userId>`
  - Slack：`agent:<agentId>:slack:slash:<userId>`（前缀可通过 `channels.slack.slashCommand.sessionPrefix` 配置）
  - Telegram：`telegram:slash:<userId>`（通过 `CommandTargetSessionKey` 定向到聊天会话）
- **`/stop`** 定向到活动聊天会话，因此可以中止当前运行。
- **Slack：** `channels.slack.slashCommand` 仍然支持单个 `/openclaw` 风格的命令。如果你启用 `commands.native`，你必须为每个内置命令创建一个 Slack 斜杠命令（与 `/help` 相同的名称）。Slack 的命令参数菜单以临时 Block Kit 按钮形式发送。


---
# File: docs/zh-CN/tools/subagents.md

---
read_when:
  - 你想通过智能体执行后台/并行工作
  - 你正在更改 sessions_spawn 或子智能体工具策略
summary: 子智能体：生成隔离的智能体运行，并将结果通告回请求者聊天
title: 子智能体
x-i18n:
  generated_at: "2026-02-03T10:12:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3c83eeed69a65dbbb6b21a386f3ac363d3ef8f077f0e03b834c3f0a9911dca7c
  source_path: tools/subagents.md
  workflow: 15
---

# 子智能体

子智能体是从现有智能体运行中生成的后台智能体运行。它们在自己的会话中运行（`agent:<agentId>:subagent:<uuid>`），完成后将结果**通告**回请求者的聊天渠道。

## 斜杠命令

使用 `/subagents` 检查或控制**当前会话**的子智能体运行：

- `/subagents list`
- `/subagents kill <id|#|all>`
- `/subagents log <id|#> [limit] [tools]`
- `/subagents info <id|#>`
- `/subagents send <id|#> <message>`
- `/subagents steer <id|#> <message>`
- `/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]`

`/subagents info` 显示运行元数据（状态、时间戳、会话 id、转录路径、清理）。

### 启动行为

`/subagents spawn` 以用户命令方式启动后台子智能体，任务完成后会向请求者聊天频道回发一条最终完成消息。

- 该命令非阻塞，先返回 `runId`。
- 完成后，子智能体会将汇总/结果消息发布到请求者聊天渠道。
- `--model` 与 `--thinking` 可仅对本次运行做覆盖设置。
- 可在完成后通过 `info`/`log` 查看详细信息和输出。

主要目标：

- 并行化"研究 / 长任务 / 慢工具"工作，而不阻塞主运行。
- 默认保持子智能体隔离（会话分离 + 可选沙箱隔离）。
- 保持工具接口难以滥用：子智能体默认**不**获得会话工具。
- 避免嵌套扇出：子智能体不能生成子智能体。

成本说明：每个子智能体都有**自己的**上下文和 token 使用量。对于繁重或重复的任务，为子智能体设置更便宜的模型，而让主智能体使用更高质量的模型。你可以通过 `agents.defaults.subagents.model` 或每智能体覆盖来配置。

## 工具

使用 `sessions_spawn`：

- 启动子智能体运行（`deliver: false`，全局队列：`subagent`）
- 然后运行通告步骤，并将通告回复发布到请求者的聊天渠道
- 默认模型：继承调用者，除非你设置了 `agents.defaults.subagents.model`（或每智能体的 `agents.list[].subagents.model`）；显式的 `sessions_spawn.model` 仍然优先。
- 默认思考：继承调用者，除非你设置了 `agents.defaults.subagents.thinking`（或每智能体的 `agents.list[].subagents.thinking`）；显式的 `sessions_spawn.thinking` 仍然优先。

工具参数：

- `task`（必需）
- `label?`（可选）
- `agentId?`（可选；如果允许，在另一个智能体 id 下生成）
- `model?`（可选；覆盖子智能体模型；无效值会被跳过，子智能体将使用默认模型运行并在工具结果中显示警告）
- `thinking?`（可选；覆盖子智能体运行的思考级别）
- `runTimeoutSeconds?`（默认 `0`；设置后，子智能体运行在 N 秒后中止）
- `cleanup?`（`delete|keep`，默认 `keep`）

允许列表：

- `agents.list[].subagents.allowAgents`：可以通过 `agentId` 指定的智能体 id 列表（`["*"]` 允许任意）。默认：仅限请求者智能体。

发现：

- 使用 `agents_list` 查看当前允许用于 `sessions_spawn` 的智能体 id。

自动归档：

- 子智能体会话在 `agents.defaults.subagents.archiveAfterMinutes` 后自动归档（默认：60）。
- 归档使用 `sessions.delete` 并将转录重命名为 `*.deleted.<timestamp>`（同一文件夹）。
- `cleanup: "delete"` 在通告后立即归档（仍通过重命名保留转录）。
- 自动归档是尽力而为的；如果 Gateway 网关重启，待处理的定时器会丢失。
- `runTimeoutSeconds` **不会**自动归档；它只停止运行。会话会保留直到自动归档。

## 认证

子智能体认证按**智能体 id** 解析，而不是按会话类型：

- 子智能体会话键是 `agent:<agentId>:subagent:<uuid>`。
- 认证存储从该智能体的 `agentDir` 加载。
- 主智能体的认证配置文件作为**回退**合并；智能体配置文件在冲突时覆盖主配置文件。

注意：合并是累加的，所以主配置文件始终可用作回退。目前尚不支持每智能体完全隔离的认证。

## 通告

子智能体通过通告步骤报告：

- 通告步骤在子智能体会话中运行（不是请求者会话）。
- 如果子智能体精确回复 `ANNOUNCE_SKIP`，则不发布任何内容。
- 否则，通告回复通过后续的 `agent` 调用（`deliver=true`）发布到请求者的聊天渠道。
- 通告回复在可用时保留线程/话题路由（Slack 线程、Telegram 话题、Matrix 线程）。
- 通告消息被规范化为稳定模板：
  - `Status:` 从运行结果派生（`success`、`error`、`timeout` 或 `unknown`）。
  - `Result:` 通告步骤的摘要内容（如果缺失则为 `(not available)`）。
  - `Notes:` 错误详情和其他有用的上下文。
- `Status` 不是从模型输出推断的；它来自运行时结果信号。

通告负载在末尾包含统计行（即使被包装）：

- 运行时间（例如 `runtime 5m12s`）
- Token 使用量（输入/输出/总计）
- 配置模型定价时的估计成本（`models.providers.*.models[].cost`）
- `sessionKey`、`sessionId` 和转录路径（以便主智能体可以通过 `sessions_history` 获取历史记录或检查磁盘上的文件）

## 工具策略（子智能体工具）

默认情况下，子智能体获得**除会话工具外的所有工具**：

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`

通过配置覆盖：

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 1,
      },
    },
  },
  tools: {
    subagents: {
      tools: {
        // deny 优先
        deny: ["gateway", "cron"],
        // 如果设置了 allow，则变为仅允许模式（deny 仍然优先）
        // allow: ["read", "exec", "process"]
      },
    },
  },
}
```

## 并发

子智能体使用专用的进程内队列通道：

- 通道名称：`subagent`
- 并发数：`agents.defaults.subagents.maxConcurrent`（默认 `8`）

## 停止

- 在请求者聊天中发送 `/stop` 会中止请求者会话并停止从中生成的任何活动子智能体运行。

## 限制

- 子智能体通告是**尽力而为**的。如果 Gateway 网关重启，待处理的"通告回复"工作会丢失。
- 子智能体仍然共享相同的 Gateway 网关进程资源；将 `maxConcurrent` 视为安全阀。
- `sessions_spawn` 始终是非阻塞的：它立即返回 `{ status: "accepted", runId, childSessionKey }`。
- 子智能体上下文仅注入 `AGENTS.md` + `TOOLS.md`（无 `SOUL.md`、`IDENTITY.md`、`USER.md`、`HEARTBEAT.md` 或 `BOOTSTRAP.md`）。


---
# File: docs/zh-CN/tools/thinking.md

---
read_when:
  - 调整思考或详细模式指令解析或默认值时
summary: "`/think` + `/verbose` 的指令语法及其对模型推理的影响"
title: 思考级别
x-i18n:
  generated_at: "2026-02-01T21:43:37Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1a611474c2781c9a8e9dac0e084e7ee4ef58aebece181fdc877392fc27442746
  source_path: tools/thinking.md
  workflow: 15
---

# 思考级别（/think 指令）

## 功能说明

- 在任何入站消息正文中使用内联指令：`/t <level>`、`/think:<level>` 或 `/thinking <level>`。
- 级别（别名）：`off | minimal | low | medium | high | xhigh`（仅 GPT-5.2 + Codex 模型）
  - minimal → "think"
  - low → "think hard"
  - medium → "think harder"
  - high → "ultrathink"（最大预算）
  - xhigh → "ultrathink+"（仅 GPT-5.2 + Codex 模型）
  - `highest`、`max` 映射为 `high`。
- 提供商说明：
  - Z.AI（`zai/*`）仅支持二元思考（`on`/`off`）。任何非 `off` 级别均视为 `on`（映射为 `low`）。

## 解析优先顺序

1. 消息上的内联指令（仅适用于该条消息）。
2. 会话覆盖（通过发送仅包含指令的消息设置）。
3. 全局默认值（配置中的 `agents.defaults.thinkingDefault`）。
4. 回退：具备推理能力的模型为 low；否则为 off。

## 设置会话默认值

- 发送一条**仅包含**指令的消息（允许空白），例如 `/think:medium` 或 `/t high`。
- 该设置在当前会话中持续生效（默认按发送者）；通过 `/think:off` 或会话空闲重置来清除。
- 会发送确认回复（`Thinking level set to high.` / `Thinking disabled.`）。如果级别无效（例如 `/thinking big`），命令将被拒绝并给出提示，会话状态保持不变。
- 不带参数发送 `/think`（或 `/think:`）可查看当前思考级别。

## 按智能体应用

- **内嵌 Pi**：解析后的级别传递给进程内的 Pi 智能体运行时。

## 详细模式指令（/verbose 或 /v）

- 级别：`on`（最小）| `full` | `off`（默认）。
- 仅包含指令的消息切换会话详细模式并回复 `Verbose logging enabled.` / `Verbose logging disabled.`；无效级别返回提示且不改变状态。
- `/verbose off` 存储一个显式的会话覆盖；通过会话 UI 选择 `inherit` 来清除。
- 内联指令仅影响该条消息；否则应用会话/全局默认值。
- 不带参数发送 `/verbose`（或 `/verbose:`）可查看当前详细模式级别。
- 启用详细模式后，发出结构化工具结果的智能体（Pi 及其他 JSON 智能体）会将每个工具调用作为独立的元数据消息发回，可用时以 `<emoji> <tool-name>: <arg>` 为前缀（路径/命令）。这些工具摘要在每个工具启动时立即发送（独立气泡），而非作为流式增量。
- 当详细模式为 `full` 时，工具输出也会在完成后转发（独立气泡，截断至安全长度）。如果在运行过程中切换 `/verbose on|full|off`，后续的工具气泡会遵循新设置。

## 推理可见性（/reasoning）

- 级别：`on|off|stream`。
- 仅包含指令的消息切换回复中是否显示思考块。
- 启用时，推理内容作为**独立消息**发送，以 `Reasoning:` 为前缀。
- `stream`（仅 Telegram）：在回复生成期间将推理内容流式输出到 Telegram 草稿气泡中，然后发送不包含推理的最终回答。
- 别名：`/reason`。
- 不带参数发送 `/reasoning`（或 `/reasoning:`）可查看当前推理级别。

## 相关内容

- 提权模式文档位于[提权模式](/tools/elevated)。

## 心跳

- 心跳探测正文为配置的心跳提示词（默认：`Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`）。心跳消息中的内联指令照常生效（但避免从心跳中更改会话默认值）。
- 心跳投递默认仅包含最终负载。要同时发送单独的 `Reasoning:` 消息（如果可用），请设置 `agents.defaults.heartbeat.includeReasoning: true` 或按智能体 `agents.list[].heartbeat.includeReasoning: true`。

## Web 聊天 UI

- Web 聊天的思考选择器在页面加载时从入站会话存储/配置中读取并反映会话的已存储级别。
- 选择另一个级别仅应用于下一条消息（`thinkingOnce`）；发送后，选择器会回到已存储的会话级别。
- 要更改会话默认值，请发送 `/think:<level>` 指令（和之前一样）；选择器将在下次刷新后反映该设置。


---
# File: docs/zh-CN/tools/web.md

---
read_when:
  - 你想启用 web_search 或 web_fetch
  - 你需要设置 Brave Search API 密钥
  - 你想使用 Perplexity Sonar 进行网络搜索
summary: Web 搜索 + 获取工具（Brave Search API、Perplexity 直连/OpenRouter）
title: Web 工具
x-i18n:
  generated_at: "2026-02-03T10:12:43Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 760b706cc966cb421e370f10f8e76047f8ca9fe0a106d90c05d979976789465a
  source_path: tools/web.md
  workflow: 15
---

# Web 工具

OpenClaw 提供两个轻量级 Web 工具：

- `web_search` — 通过 Brave Search API（默认）或 Perplexity Sonar（直连或通过 OpenRouter）搜索网络。
- `web_fetch` — HTTP 获取 + 可读性提取（HTML → markdown/文本）。

这些**不是**浏览器自动化。对于 JS 密集型网站或需要登录的情况，请使用[浏览器工具](/tools/browser)。

## 工作原理

- `web_search` 调用你配置的提供商并返回结果。
  - **Brave**（默认）：返回结构化结果（标题、URL、摘要）。
  - **Perplexity**：返回带有实时网络搜索引用的 AI 综合答案。
- 结果按查询缓存 15 分钟（可配置）。
- `web_fetch` 执行普通 HTTP GET 并提取可读内容（HTML → markdown/文本）。它**不**执行 JavaScript。
- `web_fetch` 默认启用（除非显式禁用）。

## 选择搜索提供商

| 提供商            | 优点                     | 缺点                               | API 密钥                                     |
| ----------------- | ------------------------ | ---------------------------------- | -------------------------------------------- |
| **Brave**（默认） | 快速、结构化结果、免费层 | 传统搜索结果                       | `BRAVE_API_KEY`                              |
| **Perplexity**    | AI 综合答案、引用、实时  | 需要 Perplexity 或 OpenRouter 访问 | `OPENROUTER_API_KEY` 或 `PERPLEXITY_API_KEY` |

参见 [Brave Search 设置](/brave-search) 和 [Perplexity Sonar](/perplexity) 了解提供商特定详情。

在配置中设置提供商：

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave", // 或 "perplexity"
      },
    },
  },
}
```

示例：切换到 Perplexity Sonar（直连 API）：

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## 获取 Brave API 密钥

1. 在 https://brave.com/search/api/ 创建 Brave Search API 账户
2. 在控制面板中，选择 **Data for Search** 计划（不是"Data for AI"）并生成 API 密钥。
3. 运行 `openclaw configure --section web` 将密钥存储在配置中（推荐），或在环境中设置 `BRAVE_API_KEY`。

Brave 提供免费层和付费计划；查看 Brave API 门户了解当前限制和定价。

### 在哪里设置密钥（推荐）

**推荐：** 运行 `openclaw configure --section web`。它将密钥存储在 `~/.openclaw/openclaw.json` 的 `tools.web.search.apiKey` 下。

**环境变量替代方案：** 在 Gateway 网关进程环境中设置 `BRAVE_API_KEY`。对于 Gateway 网关安装，将其放在 `~/.openclaw/.env`（或你的服务环境）中。参见[环境变量](/help/faq#how-does-openclaw-load-environment-variables)。

## 使用 Perplexity（直连或通过 OpenRouter）

Perplexity Sonar 模型具有内置的网络搜索功能，并返回带有引用的 AI 综合答案。你可以通过 OpenRouter 使用它们（无需信用卡 - 支持加密货币/预付费）。

### 获取 OpenRouter API 密钥

1. 在 https://openrouter.ai/ 创建账户
2. 添加额度（支持加密货币、预付费或信用卡）
3. 在账户设置中生成 API 密钥

### 设置 Perplexity 搜索

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          // API 密钥（如果设置了 OPENROUTER_API_KEY 或 PERPLEXITY_API_KEY 则可选）
          apiKey: "sk-or-v1-...",
          // 基础 URL（如果省略则根据密钥感知默认值）
          baseUrl: "https://openrouter.ai/api/v1",
          // 模型（默认为 perplexity/sonar-pro）
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

**环境变量替代方案：** 在 Gateway 网关环境中设置 `OPENROUTER_API_KEY` 或 `PERPLEXITY_API_KEY`。对于 Gateway 网关安装，将其放在 `~/.openclaw/.env` 中。

如果未设置基础 URL，OpenClaw 会根据 API 密钥来源选择默认值：

- `PERPLEXITY_API_KEY` 或 `pplx-...` → `https://api.perplexity.ai`
- `OPENROUTER_API_KEY` 或 `sk-or-...` → `https://openrouter.ai/api/v1`
- 未知密钥格式 → OpenRouter（安全回退）

### 可用的 Perplexity 模型

| 模型                             | 描述                 | 最适合   |
| -------------------------------- | -------------------- | -------- |
| `perplexity/sonar`               | 带网络搜索的快速问答 | 快速查询 |
| `perplexity/sonar-pro`（默认）   | 带网络搜索的多步推理 | 复杂问题 |
| `perplexity/sonar-reasoning-pro` | 思维链分析           | 深度研究 |

## web_search

使用配置的提供商搜索网络。

### 要求

- `tools.web.search.enabled` 不能为 `false`（默认：启用）
- 所选提供商的 API 密钥：
  - **Brave**：`BRAVE_API_KEY` 或 `tools.web.search.apiKey`
  - **Perplexity**：`OPENROUTER_API_KEY`、`PERPLEXITY_API_KEY` 或 `tools.web.search.perplexity.apiKey`

### 配置

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE", // 如果设置了 BRAVE_API_KEY 则可选
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

### 工具参数

- `query`（必需）
- `count`（1–10；默认来自配置）
- `country`（可选）：用于特定地区结果的 2 字母国家代码（例如"DE"、"US"、"ALL"）。如果省略，Brave 选择其默认地区。
- `search_lang`（可选）：搜索结果的 ISO 语言代码（例如"de"、"en"、"fr"）
- `ui_lang`（可选）：UI 元素的 ISO 语言代码
- `freshness`（可选，仅限 Brave）：按发现时间过滤（`pd`、`pw`、`pm`、`py` 或 `YYYY-MM-DDtoYYYY-MM-DD`）

**示例：**

```javascript
// 德国特定搜索
await web_search({
  query: "TV online schauen",
  count: 10,
  country: "DE",
  search_lang: "de",
});

// 带法语 UI 的法语搜索
await web_search({
  query: "actualités",
  country: "FR",
  search_lang: "fr",
  ui_lang: "fr",
});

// 最近结果（过去一周）
await web_search({
  query: "TMBG interview",
  freshness: "pw",
});
```

## web_fetch

获取 URL 并提取可读内容。

### 要求

- `tools.web.fetch.enabled` 不能为 `false`（默认：启用）
- 可选的 Firecrawl 回退：设置 `tools.web.fetch.firecrawl.apiKey` 或 `FIRECRAWL_API_KEY`。

### 配置

```json5
{
  tools: {
    web: {
      fetch: {
        enabled: true,
        maxChars: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        readability: true,
        firecrawl: {
          enabled: true,
          apiKey: "FIRECRAWL_API_KEY_HERE", // 如果设置了 FIRECRAWL_API_KEY 则可选
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 86400000, // 毫秒（1 天）
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

### 工具参数

- `url`（必需，仅限 http/https）
- `extractMode`（`markdown` | `text`）
- `maxChars`（截断长页面）

注意：

- `web_fetch` 首先使用 Readability（主要内容提取），然后使用 Firecrawl（如果已配置）。如果两者都失败，工具返回错误。
- Firecrawl 请求使用机器人规避模式并默认缓存结果。
- `web_fetch` 默认发送类 Chrome 的 User-Agent 和 `Accept-Language`；如需要可覆盖 `userAgent`。
- `web_fetch` 阻止私有/内部主机名并重新检查重定向（用 `maxRedirects` 限制）。
- `web_fetch` 是尽力提取；某些网站需要浏览器工具。
- 参见 [Firecrawl](/tools/firecrawl) 了解密钥设置和服务详情。
- 响应会被缓存（默认 15 分钟）以减少重复获取。
- 如果你使用工具配置文件/允许列表，添加 `web_search`/`web_fetch` 或 `group:web`。
- 如果缺少 Brave 密钥，`web_search` 返回一个简短的设置提示和文档链接。


---
# File: docs/zh-CN/tts.md

---
read_when:
  - 为回复启用文本转语音
  - 配置 TTS 提供商或限制
  - 使用 /tts 命令
summary: 出站回复的文本转语音（TTS）
title: 文本转语音
x-i18n:
  generated_at: "2026-02-03T10:13:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 070ff0cc8592f64c6c9e4ddaddc7e8fba82f0692ceded6fe833ec9ba5b61e6fb
  source_path: tts.md
  workflow: 15
---

# 文本转语音（TTS）

OpenClaw 可以使用 ElevenLabs、OpenAI 或 Edge TTS 将出站回复转换为音频。它可以在任何 OpenClaw 能发送音频的地方工作；Telegram 会显示圆形语音消息气泡。

## 支持的服务

- **ElevenLabs**（主要或备用提供商）
- **OpenAI**（主要或备用提供商；也用于摘要）
- **Edge TTS**（主要或备用提供商；使用 `node-edge-tts`，无 API 密钥时为默认）

### Edge TTS 注意事项

Edge TTS 通过 `node-edge-tts` 库使用 Microsoft Edge 的在线神经网络 TTS 服务。它是托管服务（非本地），使用 Microsoft 的端点，不需要 API 密钥。`node-edge-tts` 公开了语音配置选项和输出格式，但并非所有选项都被 Edge 服务支持。citeturn2search0

由于 Edge TTS 是一个没有公布 SLA 或配额的公共 Web 服务，请将其视为尽力而为。如果你需要有保证的限制和支持，请使用 OpenAI 或 ElevenLabs。Microsoft 的语音 REST API 记录了每个请求 10 分钟的音频限制；Edge TTS 没有公布限制，所以假设类似或更低的限制。citeturn0search3

## 可选密钥

如果你想使用 OpenAI 或 ElevenLabs：

- `ELEVENLABS_API_KEY`（或 `XI_API_KEY`）
- `OPENAI_API_KEY`

Edge TTS **不**需要 API 密钥。如果没有找到 API 密钥，OpenClaw 默认使用 Edge TTS（除非通过 `messages.tts.edge.enabled=false` 禁用）。

如果配置了多个提供商，首先使用选定的提供商，其他作为备用选项。自动摘要使用配置的 `summaryModel`（或 `agents.defaults.model.primary`），所以如果你启用摘要，该提供商也必须经过认证。

## 服务链接

- [OpenAI 文本转语音指南](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI 音频 API 参考](https://platform.openai.com/docs/api-reference/audio)
- [ElevenLabs 文本转语音](https://elevenlabs.io/docs/api-reference/text-to-speech)
- [ElevenLabs 认证](https://elevenlabs.io/docs/api-reference/authentication)
- [node-edge-tts](https://github.com/SchneeHertz/node-edge-tts)
- [Microsoft 语音输出格式](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech#audio-outputs)

## 默认启用吗？

不是。自动 TTS 默认**关闭**。在配置中使用 `messages.tts.auto` 或在每个会话中使用 `/tts always`（别名：`/tts on`）启用它。

一旦 TTS 开启，Edge TTS **是**默认启用的，并在没有 OpenAI 或 ElevenLabs API 密钥时自动使用。

## 配置

TTS 配置位于 `openclaw.json` 中的 `messages.tts` 下。完整 schema 在 [Gateway 网关配置](/gateway/configuration)中。

### 最小配置（启用 + 提供商）

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

### OpenAI 主要，ElevenLabs 备用

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
    },
  },
}
```

### Edge TTS 主要（无 API 密钥）

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "edge",
      edge: {
        enabled: true,
        voice: "en-US-MichelleNeural",
        lang: "en-US",
        outputFormat: "audio-24khz-48kbitrate-mono-mp3",
        rate: "+10%",
        pitch: "-5%",
      },
    },
  },
}
```

### 禁用 Edge TTS

```json5
{
  messages: {
    tts: {
      edge: {
        enabled: false,
      },
    },
  },
}
```

### 自定义限制 + 偏好路径

```json5
{
  messages: {
    tts: {
      auto: "always",
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
    },
  },
}
```

### 仅在收到语音消息后用音频回复

```json5
{
  messages: {
    tts: {
      auto: "inbound",
    },
  },
}
```

### 禁用长回复的自动摘要

```json5
{
  messages: {
    tts: {
      auto: "always",
    },
  },
}
```

然后运行：

```
/tts summary off
```

### 字段说明

- `auto`：自动 TTS 模式（`off`、`always`、`inbound`、`tagged`）。
  - `inbound` 仅在收到语音消息后发送音频。
  - `tagged` 仅在回复包含 `[[tts]]` 标签时发送音频。
- `enabled`：旧版开关（doctor 将其迁移到 `auto`）。
- `mode`：`"final"`（默认）或 `"all"`（包括工具/分块回复）。
- `provider`：`"elevenlabs"`、`"openai"` 或 `"edge"`（自动备用）。
- 如果 `provider` **未设置**，OpenClaw 优先选择 `openai`（如果有密钥），然后是 `elevenlabs`（如果有密钥），否则是 `edge`。
- `summaryModel`：用于自动摘要的可选廉价模型；默认为 `agents.defaults.model.primary`。
  - 接受 `provider/model` 或配置的模型别名。
- `modelOverrides`：允许模型发出 TTS 指令（默认开启）。
- `maxTextLength`：TTS 输入的硬性上限（字符）。超出时 `/tts audio` 会失败。
- `timeoutMs`：请求超时（毫秒）。
- `prefsPath`：覆盖本地偏好 JSON 路径（提供商/限制/摘要）。
- `apiKey` 值回退到环境变量（`ELEVENLABS_API_KEY`/`XI_API_KEY`、`OPENAI_API_KEY`）。
- `elevenlabs.baseUrl`：覆盖 ElevenLabs API 基础 URL。
- `elevenlabs.voiceSettings`：
  - `stability`、`similarityBoost`、`style`：`0..1`
  - `useSpeakerBoost`：`true|false`
  - `speed`：`0.5..2.0`（1.0 = 正常）
- `elevenlabs.applyTextNormalization`：`auto|on|off`
- `elevenlabs.languageCode`：2 字母 ISO 639-1（例如 `en`、`de`）
- `elevenlabs.seed`：整数 `0..4294967295`（尽力确定性）
- `edge.enabled`：允许 Edge TTS 使用（默认 `true`；无 API 密钥）。
- `edge.voice`：Edge 神经网络语音名称（例如 `en-US-MichelleNeural`）。
- `edge.lang`：语言代码（例如 `en-US`）。
- `edge.outputFormat`：Edge 输出格式（例如 `audio-24khz-48kbitrate-mono-mp3`）。
  - 有效值参见 Microsoft 语音输出格式；并非所有格式都被 Edge 支持。
- `edge.rate` / `edge.pitch` / `edge.volume`：百分比字符串（例如 `+10%`、`-5%`）。
- `edge.saveSubtitles`：在音频文件旁边写入 JSON 字幕。
- `edge.proxy`：Edge TTS 请求的代理 URL。
- `edge.timeoutMs`：请求超时覆盖（毫秒）。

## 模型驱动覆盖（默认开启）

默认情况下，模型**可以**为单个回复发出 TTS 指令。当 `messages.tts.auto` 为 `tagged` 时，需要这些指令来触发音频。

启用后，模型可以发出 `[[tts:...]]` 指令来覆盖单个回复的语音，加上可选的 `[[tts:text]]...[[/tts:text]]` 块来提供表达性标签（笑声、唱歌提示等），这些仅应出现在音频中。

示例回复负载：

```
Here you go.

[[tts:provider=elevenlabs voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

可用指令键（启用时）：

- `provider`（`openai` | `elevenlabs` | `edge`）
- `voice`（OpenAI 语音）或 `voiceId`（ElevenLabs）
- `model`（OpenAI TTS 模型或 ElevenLabs 模型 ID）
- `stability`、`similarityBoost`、`style`、`speed`、`useSpeakerBoost`
- `applyTextNormalization`（`auto|on|off`）
- `languageCode`（ISO 639-1）
- `seed`

禁用所有模型覆盖：

```json5
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: false,
      },
    },
  },
}
```

可选白名单（禁用特定覆盖同时保持标签启用）：

```json5
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: true,
        allowProvider: false,
        allowSeed: false,
      },
    },
  },
}
```

## 单用户偏好

斜杠命令将本地覆盖写入 `prefsPath`（默认：`~/.openclaw/settings/tts.json`，可通过 `OPENCLAW_TTS_PREFS` 或 `messages.tts.prefsPath` 覆盖）。

存储的字段：

- `enabled`
- `provider`
- `maxLength`（摘要阈值；默认 1500 字符）
- `summarize`（默认 `true`）

这些为该主机覆盖 `messages.tts.*`。

## 输出格式（固定）

- **Telegram**：Opus 语音消息（ElevenLabs 的 `opus_48000_64`，OpenAI 的 `opus`）。
  - 48kHz / 64kbps 是语音消息的良好权衡，圆形气泡所必需。
- **其他渠道**：MP3（ElevenLabs 的 `mp3_44100_128`，OpenAI 的 `mp3`）。
  - 44.1kHz / 128kbps 是语音清晰度的默认平衡。
- **Edge TTS**：使用 `edge.outputFormat`（默认 `audio-24khz-48kbitrate-mono-mp3`）。
  - `node-edge-tts` 接受 `outputFormat`，但并非所有格式都可从 Edge 服务获得。citeturn2search0
  - 输出格式值遵循 Microsoft 语音输出格式（包括 Ogg/WebM Opus）。citeturn1search0
  - Telegram `sendVoice` 接受 OGG/MP3/M4A；如果你需要有保证的 Opus 语音消息，请使用 OpenAI/ElevenLabs。citeturn1search1
  - 如果配置的 Edge 输出格式失败，OpenClaw 会使用 MP3 重试。

OpenAI/ElevenLabs 格式是固定的；Telegram 期望 Opus 以获得语音消息用户体验。

## 自动 TTS 行为

启用后，OpenClaw：

- 如果回复已包含媒体或 `MEDIA:` 指令，则跳过 TTS。
- 跳过非常短的回复（< 10 字符）。
- 启用时使用 `agents.defaults.model.primary`（或 `summaryModel`）对长回复进行摘要。
- 将生成的音频附加到回复中。

如果回复超过 `maxLength` 且摘要关闭（或没有摘要模型的 API 密钥），则跳过音频并发送正常的文本回复。

## 流程图

```
回复 -> TTS 启用？
  否  -> 发送文本
  是  -> 有媒体 / MEDIA: / 太短？
          是 -> 发送文本
          否 -> 长度 > 限制？
                   否  -> TTS -> 附加音频
                   是  -> 摘要启用？
                            否  -> 发送文本
                            是  -> 摘要（summaryModel 或 agents.defaults.model.primary）
                                      -> TTS -> 附加音频
```

## 斜杠命令用法

只有一个命令：`/tts`。参见[斜杠命令](/tools/slash-commands)了解启用详情。

Discord 注意：`/tts` 是 Discord 的内置命令，所以 OpenClaw 在那里注册 `/voice` 作为原生命令。文本 `/tts ...` 仍然有效。

```
/tts off
/tts always
/tts inbound
/tts tagged
/tts status
/tts provider openai
/tts limit 2000
/tts summary off
/tts audio Hello from OpenClaw
```

注意事项：

- 命令需要授权发送者（白名单/所有者规则仍然适用）。
- 必须启用 `commands.text` 或原生命令注册。
- `off|always|inbound|tagged` 是单会话开关（`/tts on` 是 `/tts always` 的别名）。
- `limit` 和 `summary` 存储在本地偏好中，不在主配置中。
- `/tts audio` 生成一次性音频回复（不会开启 TTS）。

## 智能体工具

`tts` 工具将文本转换为语音并返回 `MEDIA:` 路径。当结果与 Telegram 兼容时，工具包含 `[[audio_as_voice]]`，以便 Telegram 发送语音气泡。

## Gateway 网关 RPC

Gateway 网关方法：

- `tts.status`
- `tts.enable`
- `tts.disable`
- `tts.convert`
- `tts.setProvider`
- `tts.providers`


---
# File: docs/zh-CN/vps.md

---
read_when:
  - 你想在云端运行 Gateway 网关
  - 你需要 VPS/托管指南的快速索引
summary: OpenClaw 的 VPS 托管中心（Oracle/Fly/Hetzner/GCP/exe.dev）
title: VPS 托管
x-i18n:
  generated_at: "2026-02-03T10:12:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 7749b479b333aa5541e7ad8b0ff84e9f8f6bd10d7188285121975cb893acc037
  source_path: vps.md
  workflow: 15
---

# VPS 托管

本中心链接到支持的 VPS/托管指南，并在高层次上解释云部署的工作原理。

## 选择提供商

- **Railway**（一键 + 浏览器设置）：[Railway](/install/railway)
- **Northflank**（一键 + 浏览器设置）：[Northflank](/install/northflank)
- **Oracle Cloud（永久免费）**：[Oracle](/platforms/oracle) — $0/月（永久免费，ARM；容量/注册可能不太稳定）
- **Fly.io**：[Fly.io](/install/fly)
- **Hetzner（Docker）**：[Hetzner](/install/hetzner)
- **GCP（Compute Engine）**：[GCP](/install/gcp)
- **exe.dev**（VM + HTTPS 代理）：[exe.dev](/install/exe-dev)
- **AWS（EC2/Lightsail/免费套餐）**：也运行良好。视频指南：
  https://x.com/techfrenAJ/status/2014934471095812547

## 云设置的工作原理

- **Gateway 网关运行在 VPS 上**并拥有状态 + 工作区。
- 你通过**控制 UI** 或 **Tailscale/SSH** 从笔记本电脑/手机连接。
- 将 VPS 视为数据源并**备份**状态 + 工作区。
- 安全默认：将 Gateway 网关保持在 loopback 上，通过 SSH 隧道或 Tailscale Serve 访问。
  如果你绑定到 `lan`/`tailnet`，需要 `gateway.auth.token` 或 `gateway.auth.password`。

远程访问：[Gateway 网关远程访问](/gateway/remote)
平台中心：[平台](/platforms)

## 在 VPS 上使用节点

你可以将 Gateway 网关保持在云端，并在本地设备（Mac/iOS/Android/无头）上配对**节点**。节点提供本地屏幕/摄像头/canvas 和 `system.run` 功能，而 Gateway 网关保持在云端。

文档：[节点](/nodes)，[节点 CLI](/cli/nodes)


---
# File: docs/zh-CN/web/control-ui.md

---
read_when:
  - 你想从浏览器操作 Gateway 网关
  - 你想要无需 SSH 隧道的 Tailnet 访问
summary: Gateway 网关的浏览器控制 UI（聊天、节点、配置）
title: 控制 UI
x-i18n:
  generated_at: "2026-02-03T10:13:20Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bef105a376fc1a1df44e3e4fb625db1cbcafe2f41e718181c36877b8cbc08816
  source_path: web/control-ui.md
  workflow: 15
---

# 控制 UI（浏览器）

控制 UI 是一个由 Gateway 网关提供服务的小型 **Vite + Lit** 单页应用：

- 默认：`http://<host>:18789/`
- 可选前缀：设置 `gateway.controlUi.basePath`（例如 `/openclaw`）

它**直接与同一端口上的 Gateway 网关 WebSocket** 通信。

## 快速打开（本地）

如果 Gateway 网关在同一台计算机上运行，打开：

- http://127.0.0.1:18789/（或 http://localhost:18789/）

如果页面加载失败，请先启动 Gateway 网关：`openclaw gateway`。

认证在 WebSocket 握手期间通过以下方式提供：

- `connect.params.auth.token`
- `connect.params.auth.password`
  仪表板设置面板允许你存储 token；密码不会被持久化。
  新手引导向导默认生成一个 Gateway 网关 token，所以在首次连接时将其粘贴到这里。

## 设备配对（首次连接）

当你从新浏览器或设备连接到控制 UI 时，Gateway 网关需要**一次性配对批准** — 即使你在同一个 Tailnet 上且 `gateway.auth.allowTailscale: true`。这是防止未授权访问的安全措施。

**你会看到：** "disconnected (1008): pairing required"

**批准设备：**

```bash
# 列出待处理的请求
openclaw devices list

# 按请求 ID 批准
openclaw devices approve <requestId>
```

一旦批准，设备会被记住，除非你使用 `openclaw devices revoke --device <id> --role <role>` 撤销它，否则不需要重新批准。参见 [Devices CLI](/cli/devices) 了解 token 轮换和撤销。

**注意：**

- 本地连接（`127.0.0.1`）会自动批准。
- 远程连接（LAN、Tailnet 等）需要显式批准。
- 每个浏览器配置文件生成唯一的设备 ID，因此切换浏览器或清除浏览器数据将需要重新配对。

## 目前可以做什么

- 通过 Gateway 网关 WS 与模型聊天（`chat.history`、`chat.send`、`chat.abort`、`chat.inject`）
- 在聊天中流式传输工具调用 + 实时工具输出卡片（智能体事件）
- 渠道：WhatsApp/Telegram/Discord/Slack + 插件渠道（Mattermost 等）状态 + QR 登录 + 每渠道配置（`channels.status`、`web.login.*`、`config.patch`）
- 实例：在线列表 + 刷新（`system-presence`）
- 会话：列表 + 每会话思考/详细覆盖（`sessions.list`、`sessions.patch`）
- 定时任务：列出/添加/运行/启用/禁用 + 运行历史（`cron.*`）
- Skills：状态、启用/禁用、安装、API 密钥更新（`skills.*`）
- 节点：列表 + 能力（`node.list`）
- 执行批准：编辑 Gateway 网关或节点允许列表 + `exec host=gateway/node` 的询问策略（`exec.approvals.*`）
- 配置：查看/编辑 `~/.openclaw/openclaw.json`（`config.get`、`config.set`）
- 配置：应用 + 带验证的重启（`config.apply`）并唤醒上次活动的会话
- 配置写入包含基础哈希保护，以防止覆盖并发编辑
- 配置 schema + 表单渲染（`config.schema`，包括插件 + 渠道 schema）；原始 JSON 编辑器仍然可用
- 调试：状态/健康/模型快照 + 事件日志 + 手动 RPC 调用（`status`、`health`、`models.list`）
- 日志：Gateway 网关文件日志的实时尾部跟踪，带过滤/导出（`logs.tail`）
- 更新：运行包/git 更新 + 重启（`update.run`）并显示重启报告

## 聊天行为

- `chat.send` 是**非阻塞的**：它立即以 `{ runId, status: "started" }` 确认，响应通过 `chat` 事件流式传输。
- 使用相同的 `idempotencyKey` 重新发送在运行时返回 `{ status: "in_flight" }`，完成后返回 `{ status: "ok" }`。
- `chat.inject` 将助手备注附加到会话转录，并为仅 UI 更新广播 `chat` 事件（无智能体运行，无渠道投递）。
- 停止：
  - 点击**停止**（调用 `chat.abort`）
  - 输入 `/stop`（或 `stop|esc|abort|wait|exit|interrupt`）以带外中止
  - `chat.abort` 支持 `{ sessionKey }`（无 `runId`）以中止该会话的所有活动运行

## Tailnet 访问（推荐）

### 集成 Tailscale Serve（首选）

保持 Gateway 网关在 loopback 上，让 Tailscale Serve 用 HTTPS 代理它：

```bash
openclaw gateway --tailscale serve
```

打开：

- `https://<magicdns>/`（或你配置的 `gateway.controlUi.basePath`）

默认情况下，当 `gateway.auth.allowTailscale` 为 `true` 时，Serve 请求可以通过 Tailscale 身份头（`tailscale-user-login`）进行认证。OpenClaw 通过使用 `tailscale whois` 解析 `x-forwarded-for` 地址并与头匹配来验证身份，并且只在请求通过 Tailscale 的 `x-forwarded-*` 头到达 loopback 时接受这些。如果你想即使对于 Serve 流量也要求 token/密码，请设置 `gateway.auth.allowTailscale: false`（或强制 `gateway.auth.mode: "password"`）。

### 绑定到 tailnet + token

```bash
openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"
```

然后打开：

- `http://<tailscale-ip>:18789/`（或你配置的 `gateway.controlUi.basePath`）

将 token 粘贴到 UI 设置中（作为 `connect.params.auth.token` 发送）。

## 不安全的 HTTP

如果你通过普通 HTTP 打开仪表板（`http://<lan-ip>` 或 `http://<tailscale-ip>`），浏览器在**非安全上下文**中运行并阻止 WebCrypto。默认情况下，OpenClaw **阻止**没有设备身份的控制 UI 连接。

**推荐修复：** 使用 HTTPS（Tailscale Serve）或在本地打开 UI：

- `https://<magicdns>/`（Serve）
- `http://127.0.0.1:18789/`（在 Gateway 网关主机上）

**降级示例（仅通过 HTTP 使用 token）：**

```json5
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

这会为控制 UI 禁用设备身份 + 配对（即使在 HTTPS 上）。仅在你信任网络时使用。

参见 [Tailscale](/gateway/tailscale) 了解 HTTPS 设置指南。

## 构建 UI

Gateway 网关从 `dist/control-ui` 提供静态文件。使用以下命令构建：

```bash
pnpm ui:build # 首次运行时自动安装 UI 依赖
```

可选的绝对基础路径（当你想要固定的资源 URL 时）：

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

用于本地开发（单独的开发服务器）：

```bash
pnpm ui:dev # 首次运行时自动安装 UI 依赖
```

然后将 UI 指向你的 Gateway 网关 WS URL（例如 `ws://127.0.0.1:18789`）。

## 调试/测试：开发服务器 + 远程 Gateway 网关

控制 UI 是静态文件；WebSocket 目标是可配置的，可以与 HTTP 源不同。当你想要在本地使用 Vite 开发服务器但 Gateway 网关在其他地方运行时，这很方便。

1. 启动 UI 开发服务器：`pnpm ui:dev`
2. 打开类似以下的 URL：

```text
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

可选的一次性认证（如需要）：

```text
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789&token=<gateway-token>
```

注意：

- `gatewayUrl` 在加载后存储在 localStorage 中并从 URL 中移除。
- `token` 存储在 localStorage 中；`password` 仅保留在内存中。
- 当 Gateway 网关在 TLS 后面时（Tailscale Serve、HTTPS 代理等），使用 `wss://`。

远程访问设置详情：[远程访问](/gateway/remote)。


---
# File: docs/zh-CN/web/dashboard.md

---
read_when:
  - 更改仪表板认证或暴露模式
summary: Gateway 网关仪表板（控制 UI）访问和认证
title: 仪表板
x-i18n:
  generated_at: "2026-02-03T10:13:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e6876d50e17d3dd741471ed78bef6ac175b2fdbdc1c45dd52d9d2bd013e17f31
  source_path: web/dashboard.md
  workflow: 15
---

# 仪表板（控制 UI）

Gateway 网关仪表板是默认在 `/` 提供的浏览器控制 UI
（通过 `gateway.controlUi.basePath` 覆盖）。

快速打开（本地 Gateway 网关）：

- http://127.0.0.1:18789/（或 http://localhost:18789/）

关键参考：

- [控制 UI](/web/control-ui) 了解使用方法和 UI 功能。
- [Tailscale](/gateway/tailscale) 了解 Serve/Funnel 自动化。
- [Web 界面](/web) 了解绑定模式和安全注意事项。

认证通过 `connect.params.auth`（token 或密码）在 WebSocket 握手时强制执行。
参见 [Gateway 网关配置](/gateway/configuration) 中的 `gateway.auth`。

安全注意事项：控制 UI 是一个**管理界面**（聊天、配置、执行审批）。
不要公开暴露它。UI 在首次加载后将 token 存储在 `localStorage` 中。
优先使用 localhost、Tailscale Serve 或 SSH 隧道。

## 快速路径（推荐）

- 新手引导后，CLI 现在会自动打开带有你的 token 的仪表板，并打印相同的带 token 链接。
- 随时重新打开：`openclaw dashboard`（复制链接，如果可能则打开浏览器，如果是无头环境则显示 SSH 提示）。
- token 保持本地（仅查询参数）；UI 在首次加载后移除它并保存到 localStorage。

## Token 基础（本地 vs 远程）

- **Localhost**：打开 `http://127.0.0.1:18789/`。如果你看到"unauthorized"，运行 `openclaw dashboard` 并使用带 token 的链接（`?token=...`）。
- **Token 来源**：`gateway.auth.token`（或 `OPENCLAW_GATEWAY_TOKEN`）；UI 在首次加载后存储它。
- **非 localhost**：使用 Tailscale Serve（如果 `gateway.auth.allowTailscale: true` 则无需 token）、带 token 的 tailnet 绑定，或 SSH 隧道。参见 [Web 界面](/web)。

## 如果你看到"unauthorized" / 1008

- 运行 `openclaw dashboard` 获取新的带 token 链接。
- 确保 Gateway 网关可达（本地：`openclaw status`；远程：SSH 隧道 `ssh -N -L 18789:127.0.0.1:18789 user@host` 然后打开 `http://127.0.0.1:18789/?token=...`）。
- 在仪表板设置中，粘贴你在 `gateway.auth.token`（或 `OPENCLAW_GATEWAY_TOKEN`）中配置的相同 token。


---
# File: docs/zh-CN/web/index.md

---
read_when:
  - 你想通过 Tailscale 访问 Gateway 网关
  - 你想使用浏览器 Control UI 和配置编辑
summary: Gateway 网关 Web 界面：Control UI、绑定模式和安全
title: Web
x-i18n:
  generated_at: "2026-02-03T10:13:29Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4da8bc9831018c482ac918a759b9739f75ca130f70993f81911818bc60a685d1
  source_path: web/index.md
  workflow: 15
---

# Web（Gateway 网关）

Gateway 网关从与 Gateway 网关 WebSocket 相同的端口提供一个小型**浏览器 Control UI**（Vite + Lit）：

- 默认：`http://<host>:18789/`
- 可选前缀：设置 `gateway.controlUi.basePath`（例如 `/openclaw`）

功能详见 [Control UI](/web/control-ui)。
本页重点介绍绑定模式、安全和面向 Web 的界面。

## Webhooks

当 `hooks.enabled=true` 时，Gateway 网关还在同一 HTTP 服务器上公开一个小型 webhook 端点。
参见 [Gateway 网关配置](/gateway/configuration) → `hooks` 了解认证 + 载荷。

## 配置（默认开启）

当资源存在时（`dist/control-ui`），Control UI **默认启用**。
你可以通过配置控制它：

```json5
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath 可选
  },
}
```

## Tailscale 访问

### 集成 Serve（推荐）

保持 Gateway 网关在本地回环上，让 Tailscale Serve 代理它：

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

然后启动 Gateway 网关：

```bash
openclaw gateway
```

打开：

- `https://<magicdns>/`（或你配置的 `gateway.controlUi.basePath`）

### Tailnet 绑定 + 令牌

```json5
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}
```

然后启动 Gateway 网关（非本地回环绑定需要令牌）：

```bash
openclaw gateway
```

打开：

- `http://<tailscale-ip>:18789/`（或你配置的 `gateway.controlUi.basePath`）

### 公共互联网（Funnel）

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password" }, // 或 OPENCLAW_GATEWAY_PASSWORD
  },
}
```

## 安全注意事项

- Gateway 网关认证默认是必需的（令牌/密码或 Tailscale 身份头）。
- 非本地回环绑定仍然**需要**共享令牌/密码（`gateway.auth` 或环境变量）。
- 向导默认生成 Gateway 网关令牌（即使在本地回环上）。
- UI 发送 `connect.params.auth.token` 或 `connect.params.auth.password`。
- 使用 Serve 时，当 `gateway.auth.allowTailscale` 为 `true` 时，Tailscale 身份头可以满足认证（无需令牌/密码）。设置 `gateway.auth.allowTailscale: false` 以要求显式凭证。参见 [Tailscale](/gateway/tailscale) 和 [安全](/gateway/security)。
- `gateway.tailscale.mode: "funnel"` 需要 `gateway.auth.mode: "password"`（共享密码）。

## 构建 UI

Gateway 网关从 `dist/control-ui` 提供静态文件。使用以下命令构建：

```bash
pnpm ui:build # 首次运行时自动安装 UI 依赖
```


---
# File: docs/zh-CN/web/tui.md

---
read_when:
  - 你想要 TUI 的新手友好演练
  - 你需要 TUI 功能、命令和快捷键的完整列表
summary: 终端 UI（TUI）：从任何机器连接到 Gateway 网关
title: TUI
x-i18n:
  generated_at: "2026-02-03T10:13:10Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4bf5b0037bbb3a166289f2f0a9399489637d4cf26335ae3577af9ea83eee747e
  source_path: web/tui.md
  workflow: 15
---

# TUI（终端 UI）

## 快速开始

1. 启动 Gateway 网关。

```bash
openclaw gateway
```

2. 打开 TUI。

```bash
openclaw tui
```

3. 输入消息并按 Enter。

远程 Gateway 网关：

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

如果你的 Gateway 网关使用密码认证，请使用 `--password`。

## 你看到的内容

- 标题栏：连接 URL、当前智能体、当前会话。
- 聊天日志：用户消息、助手回复、系统通知、工具卡片。
- 状态行：连接/运行状态（连接中、运行中、流式传输中、空闲、错误）。
- 页脚：连接状态 + 智能体 + 会话 + 模型 + think/verbose/reasoning + token 计数 + 投递状态。
- 输入：带自动完成的文本编辑器。

## 心智模型：智能体 + 会话

- 智能体是唯一的标识符（例如 `main`、`research`）。Gateway 网关公开列表。
- 会话属于当前智能体。
- 会话键存储为 `agent:<agentId>:<sessionKey>`。
  - 如果你输入 `/session main`，TUI 会将其扩展为 `agent:<currentAgent>:main`。
  - 如果你输入 `/session agent:other:main`，你会显式切换到该智能体会话。
- 会话范围：
  - `per-sender`（默认）：每个智能体有多个会话。
  - `global`：TUI 始终使用 `global` 会话（选择器可能为空）。
- 当前智能体 + 会话始终在页脚中可见。

## 发送 + 投递

- 消息发送到 Gateway 网关；默认情况下不投递到提供商。
- 开启投递：
  - `/deliver on`
  - 或设置面板
  - 或使用 `openclaw tui --deliver` 启动

## 选择器 + 覆盖层

- 模型选择器：列出可用模型并设置会话覆盖。
- 智能体选择器：选择不同的智能体。
- 会话选择器：仅显示当前智能体的会话。
- 设置：切换投递、工具输出展开和思考可见性。

## 键盘快捷键

- Enter：发送消息
- Esc：中止活动运行
- Ctrl+C：清除输入（按两次退出）
- Ctrl+D：退出
- Ctrl+L：模型选择器
- Ctrl+G：智能体选择器
- Ctrl+P：会话选择器
- Ctrl+O：切换工具输出展开
- Ctrl+T：切换思考可见性（重新加载历史）

## 斜杠命令

核心：

- `/help`
- `/status`
- `/agent <id>`（或 `/agents`）
- `/session <key>`（或 `/sessions`）
- `/model <provider/model>`（或 `/models`）

会话控制：

- `/think <off|minimal|low|medium|high>`
- `/verbose <on|full|off>`
- `/reasoning <on|off|stream>`
- `/usage <off|tokens|full>`
- `/elevated <on|off|ask|full>`（别名：`/elev`）
- `/activation <mention|always>`
- `/deliver <on|off>`

会话生命周期：

- `/new` 或 `/reset`（重置会话）
- `/abort`（中止活动运行）
- `/settings`
- `/exit`

其他 Gateway 网关斜杠命令（例如 `/context`）会转发到 Gateway 网关并显示为系统输出。参见[斜杠命令](/tools/slash-commands)。

## 本地 shell 命令

- 以 `!` 为前缀的行会在 TUI 主机上运行本地 shell 命令。
- TUI 每个会话会提示一次以允许本地执行；拒绝会在该会话中禁用 `!`。
- 命令在 TUI 工作目录中以全新的非交互式 shell 运行（无持久化 `cd`/环境变量）。
- 单独的 `!` 会作为普通消息发送；前导空格不会触发本地执行。

## 工具输出

- 工具调用显示为带有参数 + 结果的卡片。
- Ctrl+O 在折叠/展开视图之间切换。
- 工具运行时，部分更新会流式传输到同一张卡片。

## 历史 + 流式传输

- 连接时，TUI 加载最新历史（默认 200 条消息）。
- 流式响应原地更新直到完成。
- TUI 还监听智能体工具事件以获得更丰富的工具卡片。

## 连接详情

- TUI 以 `mode: "tui"` 向 Gateway 网关注册。
- 重新连接会显示系统消息；事件间隙会在日志中显示。

## 选项

- `--url <url>`：Gateway 网关 WebSocket URL（默认为配置或 `ws://127.0.0.1:<port>`）
- `--token <token>`：Gateway 网关令牌（如果需要）
- `--password <password>`：Gateway 网关密码（如果需要）
- `--session <key>`：会话键（默认：`main`，或范围为全局时为 `global`）
- `--deliver`：将助手回复投递到提供商（默认关闭）
- `--thinking <level>`：覆盖发送的思考级别
- `--timeout-ms <ms>`：智能体超时（毫秒）（默认为 `agents.defaults.timeoutSeconds`）

## 故障排除

发送消息后没有输出：

- 在 TUI 中运行 `/status` 以确认 Gateway 网关已连接且处于空闲/忙碌状态。
- 检查 Gateway 网关日志：`openclaw logs --follow`。
- 确认智能体可以运行：`openclaw status` 和 `openclaw models status`。
- 如果你期望消息出现在聊天渠道中，请启用投递（`/deliver on` 或 `--deliver`）。
- `--history-limit <n>`：要加载的历史条目数（默认 200）

## 故障排除

- `disconnected`：确保 Gateway 网关正在运行且你的 `--url/--token/--password` 正确。
- 选择器中没有智能体：检查 `openclaw agents list` 和你的路由配置。
- 会话选择器为空：你可能处于全局范围或还没有会话。


---
# File: docs/zh-CN/web/webchat.md

---
read_when:
  - 调试或配置 WebChat 访问
summary: 用于聊天 UI 的 loopback WebChat 静态主机和 Gateway 网关 WS 使用
title: WebChat
x-i18n:
  generated_at: "2026-02-03T10:13:28Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b5ee2b462c8c979ac27f80dea0cf12cf62b3c799cf8fd0a7721901e26efeb1a0
  source_path: web/webchat.md
  workflow: 15
---

# WebChat（Gateway 网关 WebSocket UI）

状态：macOS/iOS SwiftUI 聊天 UI 直接与 Gateway 网关 WebSocket 通信。

## 它是什么

- Gateway 网关的原生聊天 UI（无嵌入式浏览器，无本地静态服务器）。
- 使用与其他渠道相同的会话和路由规则。
- 确定性路由：回复始终返回到 WebChat。

## 快速开始

1. 启动 Gateway 网关。
2. 打开 WebChat UI（macOS/iOS 应用）或控制 UI 聊天标签页。
3. 确保已配置 Gateway 网关认证（默认需要，即使在 loopback 上）。

## 工作原理（行为）

- UI 连接到 Gateway 网关 WebSocket 并使用 `chat.history`、`chat.send` 和 `chat.inject`。
- `chat.inject` 直接将助手注释追加到转录并广播到 UI（无智能体运行）。
- 历史记录始终从 Gateway 网关获取（无本地文件监听）。
- 如果 Gateway 网关不可达，WebChat 为只读模式。

## 远程使用

- 远程模式通过 SSH/Tailscale 隧道传输 Gateway 网关 WebSocket。
- 你不需要运行单独的 WebChat 服务器。

## 配置参考（WebChat）

完整配置：[配置](/gateway/configuration)

渠道选项：

- 没有专用的 `webchat.*` 块。WebChat 使用下面的 Gateway 网关端点 + 认证设置。

相关的全局选项：

- `gateway.port`、`gateway.bind`：WebSocket 主机/端口。
- `gateway.auth.mode`、`gateway.auth.token`、`gateway.auth.password`：WebSocket 认证。
- `gateway.remote.url`、`gateway.remote.token`、`gateway.remote.password`：远程 Gateway 网关目标。
- `session.*`：会话存储和主键默认值。

