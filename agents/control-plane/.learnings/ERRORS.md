# ERRORS.md — Control Plane

## 2026-03-28

### [cdp_publish.py] content-data 分页参数 ambiguous option
- 命令：`cdp_publish.py content-data --page-num 2`
- 错误：`ambiguous option: --page could match --page-num, --page-size`（argparse 缩写冲突）
- 触发场景：cron `xhs-content-data-sync` 尝试拉取第2页时
- 影响：分页拉取失败，30篇笔记仅能拿到最近10篇
- 处置：已跳过分页，用第1页数据完成报告；建议修复 argparse 缩写冲突或改用 `--page-size 30` 一次全量
- 状态：⚠️ 待修复（可通知 wemedia/main 反馈给 skill 维护方）

### [notebooklm] media-research notebook 写入权限拒绝
- 错误：`acl_denied: Permission denied for operation 'source-add' on notebook 'media-research', role=none, agent=control-plane`
- 原因：control-plane agent 没有 media-research notebook 的写入角色
- 影响：NLM 同步失败，数据仅落本地 md 文件
- 处置：已跳过，报告正常生成
- 建议：在 NLM 配置中给 control-plane 添加 media-research 的 source-add 权限，或改由 wemedia agent 执行 NLM 写入
- 状态：⚠️ 待确认权限配置

### [notebooklm] skill 路径缺失
- 错误：`ENOENT: /opt/homebrew/lib/node_modules/openclaw/skills/notebooklm/SKILL.md`
- 原因：notebooklm skill 未安装到系统路径（用户自定义 skill 在 `~/.openclaw/skills/`）
- 影响：仅影响 skill 路径解析提示，实际用户安装路径正常
- 状态：ℹ️ 低优先级，可忽略
