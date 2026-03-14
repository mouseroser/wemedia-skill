#!/bin/bash
# 高优先级记忆同步脚本
# 自动查询 importance >= 0.9 的记忆并生成同步文档

set -euo pipefail

WORKSPACE="$HOME/.openclaw/workspace"
TMP_DIR="$WORKSPACE/.tmp"
ARCHIVE_DIR="$WORKSPACE/openclaw-docs/troubleshooting/memory-archive"
TIMESTAMP_HUMAN=$(date +"%Y-%m-%d %H:%M:%S")
TIMESTAMP_FILE=$(date +%Y%m%d-%H%M%S)
LOG_FILE="$WORKSPACE/memory/sync-high-priority-$TIMESTAMP_FILE.log"
MEMORY_DATA="$TMP_DIR/high-priority-memories.json"
SYNC_DOC="$TMP_DIR/high-priority-sync-$TIMESTAMP_FILE.md"

mkdir -p "$TMP_DIR" "$ARCHIVE_DIR" "$(dirname "$LOG_FILE")"

echo "[$TIMESTAMP_HUMAN] 开始高优先级记忆同步" | tee "$LOG_FILE"
echo "[$TIMESTAMP_HUMAN] 查询 importance >= 0.9 的记忆..." | tee -a "$LOG_FILE"

RAW_OUTPUT=$(openclaw memory-pro list --json --scope agent:main --limit 500 2>/dev/null || true)
JSON_OUTPUT=$(printf '%s\n' "$RAW_OUTPUT" | sed -n '/^\[$/,$p')

if [ -z "$JSON_OUTPUT" ]; then
    echo "[$TIMESTAMP_HUMAN] ❌ 无法从 openclaw memory-pro list 提取 JSON 输出" | tee -a "$LOG_FILE"
    exit 1
fi

printf '%s\n' "$JSON_OUTPUT" | jq '[.[] | select((.importance // 0) >= 0.9)]' > "$MEMORY_DATA"
MEMORY_COUNT=$(jq 'length' "$MEMORY_DATA")

echo "[$TIMESTAMP_HUMAN] 找到 $MEMORY_COUNT 条高优先级记忆" | tee -a "$LOG_FILE"

if [ "$MEMORY_COUNT" -eq 0 ]; then
    echo "[$TIMESTAMP_HUMAN] ✅ 当前没有需要同步的高优先级记忆" | tee -a "$LOG_FILE"
    exit 0
fi

cat > "$SYNC_DOC" <<EOF
# 高优先级记忆同步 - $TIMESTAMP_HUMAN

> 自动同步 importance >= 0.9 的记忆

## 同步统计

- 记忆数量: $MEMORY_COUNT
- 同步时间: $TIMESTAMP_HUMAN
- 最小重要性: 0.9

## 记忆列表

EOF

jq -r '.[] | "### \(.text)\n\n- **重要性**: \(.importance // 0)\n- **分类**: \(.category // "unknown")\n- **作用域**: \(.scope // "default")\n- **时间戳**: \(.timestamp // "unknown")\n- **ID**: \(.id)\n\n---\n"' "$MEMORY_DATA" >> "$SYNC_DOC"

echo "[$TIMESTAMP_HUMAN] 已生成同步文档: $SYNC_DOC" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP_HUMAN] 将同步文档纳入 Memory Archive staging..." | tee -a "$LOG_FILE"

bash "$WORKSPACE/scripts/sync-memory-to-notebooklm.sh" "$SYNC_DOC" >> "$LOG_FILE" 2>&1

FINAL_DOC="$ARCHIVE_DIR/$(basename "$SYNC_DOC")"
if [ -f "$FINAL_DOC" ]; then
    echo "[$TIMESTAMP_HUMAN] ✅ 高优先级记忆同步完成: $FINAL_DOC" | tee -a "$LOG_FILE"
else
    echo "[$TIMESTAMP_HUMAN] ❌ 同步文档未出现在目标目录: $FINAL_DOC" | tee -a "$LOG_FILE"
    exit 1
fi
