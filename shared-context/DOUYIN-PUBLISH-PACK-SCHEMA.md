# 抖音发布包 Schema

用于 `wemedia` 在 Step 6 产出标准抖音发布包；晨星在 Step 7 确认后，由 `main` 通知 `wemedia` 在 Step 7.5 调 `douyin` skill 执行。

## 模板

```text
平台：douyin
内容ID：{{content_id}}
标题：{{title}}
描述：
{{description}}
#{{tag1}} #{{tag2}} #{{tag3}}
视频路径：{{video_path}}
竖封面路径：{{vertical_cover_path}}
横封面路径：{{horizontal_cover_path}}
音乐：{{music|默认=热门}}
可见性：{{visibility|默认=private}}
备注：{{notes|可选}}
```

## 最小可用要求
- 标题 ≤30 字
- 描述末尾必须带 `#标签`
- 视频路径必须是绝对路径
- 竖封面必须为 9:16
- 横封面必须为 4:3
- 可见性只允许：`private` / `public`

## 保存位置
`~/.openclaw/workspace/intel/collaboration/media/wemedia/douyin/{content_id}.md`

## 调用命令

```bash
# 校验发布包
python3 ~/.openclaw/skills/douyin/scripts/publish_douyin.py \
  --pack <pack_path> --step validate_pack

# 重复检查
python3 ~/.openclaw/skills/douyin/scripts/publish_douyin.py \
  --pack <pack_path> --step check_duplicate

# 完整发布
python3 ~/.openclaw/skills/douyin/scripts/publish_douyin.py \
  --pack <pack_path> --step full
```

## 注意
- CLI 参数与发布包同时传入时，CLI 参数优先
- 默认 `visibility=private`
- 封面上传可能受 Douyin Web Creator UI 限制阻塞
