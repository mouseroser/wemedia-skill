#!/bin/bash
# Memory Compression Script
# 自动检测和压缩超大日志文件

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
MAX_TOKENS=40000
TOKENS_PER_CHAR=0.25  # 粗略估算：1 token ≈ 4 chars

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

# 计算文件的大致 token 数
estimate_tokens() {
    local file="$1"
    local chars=$(wc -c < "$file")
    echo $(( chars * TOKENS_PER_CHAR / 1 ))
}

# 压缩单个日志文件
compress_log() {
    local file="$1"
    local tokens=$(estimate_tokens "$file")
    local basename=$(basename "$file")
    
    log "压缩 $basename (约 $tokens tokens)"
    
    # 创建备份
    cp "$file" "$file.bak"
    
    # 提取关键内容（保留标题、重要事件、错误、解决方案）
    cat "$file" | grep -E '^##|^###|❌|✅|⚠️|🔧|💡|踩坑|解决|错误|成功|完成' > "$file.compressed" || true
    
    # 如果压缩后的文件不为空，替换原文件
    if [ -s "$file.compressed" ]; then
        mv "$file.compressed" "$file"
        log "✅ 压缩完成，备份保存在 $file.bak"
    else
        log "⚠️  压缩后文件为空，保持原文件"
        rm "$file.compressed"
    fi
}

# 归档旧日志
archive_old_logs() {
    local days_ago=30
    local archive_dir="$MEMORY_DIR/archive"
    
    mkdir -p "$archive_dir"
    
    # 查找 30 天前的日志
    find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -mtime +$days_ago | while read -r file; do
        local basename=$(basename "$file")
        if [[ "$basename" != "MEMORY.md" ]]; then
            log "归档 $basename"
            mv "$file" "$archive_dir/"
        fi
    done
}

# 主函数
main() {
    log "开始记忆压缩检查"
    
    if [ ! -d "$MEMORY_DIR" ]; then
        log "❌ 记忆目录不存在: $MEMORY_DIR"
        exit 1
    fi
    
    # 检查所有日志文件
    find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f | while read -r file; do
        local basename=$(basename "$file")
        
        # 跳过 MEMORY.md
        if [[ "$basename" == "MEMORY.md" ]]; then
            continue
        fi
        
        local tokens=$(estimate_tokens "$file")
        
        if [ "$tokens" -gt "$MAX_TOKENS" ]; then
            log "⚠️  $basename 超过限制 ($tokens > $MAX_TOKENS tokens)"
            compress_log "$file"
        else
            log "✅ $basename 正常 ($tokens tokens)"
        fi
    done
    
    # 归档旧日志
    archive_old_logs
    
    log "记忆压缩检查完成"
}

main "$@"
