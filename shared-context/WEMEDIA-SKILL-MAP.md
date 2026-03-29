# WEMEDIA-SKILL-MAP.md

> 自媒体 skill 体系调用关系图。

---

## 三层结构

```text
wemedia（运营层 / 编排层）
  ├── 选题 → 宪法 → 创作 → 配图 → 平台适配 → 发布包
  │
  ├── 调用 → xiaohongshu（小红书执行层）
  │     └── scripts/publish_pipeline.py
  │     └── scripts/publish_with_guard.py
  │     └── scripts/cdp_publish.py
  │     └── scripts/feed_explorer.py（竞品搜索）
  │     └── scripts/chrome_launcher.py（Chrome 管理）
  │
  └── 调用 → douyin（抖音执行层）
        └── scripts/publish_douyin.py
        └── scripts/cdp_client.py（CDP 通信）
```

## 共享基础层

```text
shared/cdp-utils/
  ├── cdp_client.py     — 统一 CDP 连接 / 导航 / 截图 / 填写
  └── run_lock.py       — 进程级执行锁
```

---

## 调用时机

### wemedia → xiaohongshu
- **Step 7.5**：晨星确认后，main 通知 wemedia 执行发布
- wemedia 校验发布包 → 调用 `xiaohongshu/scripts/publish_pipeline.py` 或 `publish_with_guard.py`
- 发布包位置：见 `XIAOHONGSHU-PUBLISH-PACK-SCHEMA.md`

### wemedia → douyin
- **Step 7.5**：同上
- wemedia 校验发布包 → 调用 `douyin/scripts/publish_douyin.py --pack <path>`
- 发布包位置：见 `DOUYIN-PUBLISH-PACK-SCHEMA.md`

---

## 发布包 Schema

| 平台 | Schema 文件 |
|------|------------|
| 小红书 | `shared-context/XIAOHONGSHU-PUBLISH-PACK-SCHEMA.md` |
| 抖音 | `shared-context/DOUYIN-PUBLISH-PACK-SCHEMA.md` |

---

## 路径约定

| 内容 | 路径 | 写入者 | 读取者 |
|------|------|--------|--------|
| 小红书发布包 | `intel/collaboration/media/wemedia/xiaohongshu/{content_id}.md` | wemedia | wemedia / xiaohongshu |
| 抖音发布包 | `intel/collaboration/media/wemedia/douyin/{content_id}.md` | wemedia | wemedia / douyin |
| 内容草稿 | `intel/collaboration/media/wemedia/drafts/{A|B|C}/{标识}.txt` | wemedia | wemedia / main |
| 配图 | `intel/collaboration/media/images/{A|B|C}/{标识}_sq.jpg` | wemedia | wemedia / xiaohongshu |

---

## 职责边界

| 归属 | 职责 |
|------|------|
| **wemedia** | 选题、创作、宪法、配图生成、平台适配、发布包产出、Step 7.5 调用执行 |
| **xiaohongshu** | CDP 脚本执行、竞品搜索、数据看板、评论回复、登录管理 |
| **douyin** | CDP 脚本执行、视频上传、封面处理、审核等待 |
| **main** | 编排 + 监控 + Step 7 确认门控 + 可靠通知 |

---

## 硬规则

- Step 7 之前，wemedia 只产出发布包，**不得擅自发布**
- Step 7 确认后，由 main 通知 wemedia 执行 Step 7.5
- main 不直接越位替代平台执行细节
- 正式发布脚本失效时，**不用 main/browser 手工补发**，必须 BLOCKED

---

**最后更新**: 2026-03-28
