#!/bin/bash
# NotebookLM 记忆同步脚本
# 功能：将最近 4 周的记忆文件同步到 Memory Archive staging 目录
# 可选参数：额外复制一个或多个文件到目标目录

set -euo pipefail

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$WORKSPACE/openclaw-docs/troubleshooting/memory-archive"
LOG_FILE="$WORKSPACE/logs/notebooklm-sync.log"

mkdir -p "$ARCHIVE_DIR" "$(dirname "$LOG_FILE")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始同步记忆文件到 NotebookLM staging..." | tee -a "$LOG_FILE"

CUTOFF_DATE=$(date -v-4w '+%Y-%m-%d' 2>/dev/null || date -d '4 weeks ago' '+%Y-%m-%d')
echo "保留日期范围: $CUTOFF_DATE 至今" | tee -a "$LOG_FILE"

SYNCED=0
SKIPPED=0
EXTRA_SYNCED=0

for file in "$MEMORY_DIR"/2026-*.md; do
    [ -f "$file" ] || continue

    filename=$(basename "$file")

    if [[ "$filename" =~ ^(README|audit-|daily-report-|layer2-health-|memory-) ]]; then
        continue
    fi

    file_date=$(echo "$filename" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)
    [ -n "$file_date" ] || continue

    if [[ "$file_date" < "$CUTOFF_DATE" ]]; then
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    cp "$file" "$ARCHIVE_DIR/"
    SYNCED=$((SYNCED + 1))
done

if [ -f "$WORKSPACE/MEMORY.md" ]; then
    cp "$WORKSPACE/MEMORY.md" "$ARCHIVE_DIR/"
    echo "已同步 MEMORY.md" | tee -a "$LOG_FILE"
fi

if [ -d "$MEMORY_DIR/reflections" ]; then
    mkdir -p "$ARCHIVE_DIR/reflections"
    cp -r "$MEMORY_DIR/reflections/"* "$ARCHIVE_DIR/reflections/" 2>/dev/null || true
    echo "已同步 reflections 目录" | tee -a "$LOG_FILE"
fi

for extra_file in "$@"; do
    [ -n "$extra_file" ] || continue
    if [ ! -f "$extra_file" ]; then
        echo "⚠️ 跳过不存在的额外文件: $extra_file" | tee -a "$LOG_FILE"
        continue
    fi

    if [ "$(cd "$(dirname "$extra_file")" && pwd)" = "$ARCHIVE_DIR" ]; then
        echo "额外文件已在目标目录中: $extra_file" | tee -a "$LOG_FILE"
    else
        cp "$extra_file" "$ARCHIVE_DIR/"
        echo "已同步额外文件: $(basename "$extra_file")" | tee -a "$LOG_FILE"
    fi
    EXTRA_SYNCED=$((EXTRA_SYNCED + 1))
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 同步完成" | tee -a "$LOG_FILE"
echo "- 同步文件数: $SYNCED" | tee -a "$LOG_FILE"
echo "- 跳过文件数: $SKIPPED (超过 4 周)" | tee -a "$LOG_FILE"
echo "- 额外文件数: $EXTRA_SYNCED" | tee -a "$LOG_FILE"
echo "- 目标目录: $ARCHIVE_DIR" | tee -a "$LOG_FILE"

exit 0
