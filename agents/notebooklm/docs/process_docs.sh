#!/bin/bash

# OpenClaw 文档处理脚本
# 将 HTML 转换为 Markdown 并合并

RAW_DIR="$HOME/.openclaw/workspace/agents/notebooklm/docs/raw"
OUTPUT_FILE="$HOME/.openclaw/workspace/agents/notebooklm/docs/openclaw_docs_combined_$(date +%Y%m%d).md"

echo "# OpenClaw Documentation" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "**Generated:** $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "**Source:** https://docs.openclaw.ai (English only)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 按顺序处理文档
process_section() {
  local section_name="$1"
  shift
  local files=("$@")
  
  echo "" >> "$OUTPUT_FILE"
  echo "# $section_name" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  
  for file in "${files[@]}"; do
    html_file="$RAW_DIR/${file}.html"
    
    if [ -f "$html_file" ]; then
      echo "处理: $file"
      
      # 提取标题
      title=$(grep -o '<title>[^<]*</title>' "$html_file" | sed 's/<title>\(.*\)<\/title>/\1/' | sed 's/ | OpenClaw//')
      
      if [ -n "$title" ]; then
        echo "## $title" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
      fi
      
      # 使用 pandoc 转换（如果可用）
      if command -v pandoc &> /dev/null; then
        pandoc -f html -t markdown "$html_file" >> "$OUTPUT_FILE" 2>/dev/null
      else
        # 简单清理
        sed -n '/<main/,/<\/main>/p' "$html_file" | \
          sed 's/<[^>]*>//g' | \
          sed 's/&nbsp;/ /g' | \
          sed 's/&lt;/</g' | \
          sed 's/&gt;/>/g' | \
          sed 's/&amp;/\&/g' | \
          sed '/^[[:space:]]*$/d' >> "$OUTPUT_FILE"
      fi
      
      echo "" >> "$OUTPUT_FILE"
      echo "---" >> "$OUTPUT_FILE"
      echo "" >> "$OUTPUT_FILE"
    fi
  done
}

# 按章节处理
process_section "Getting Started" index install start_getting-started start_quickstart start_hubs
process_section "Onboarding" start_onboarding-overview start_onboarding start_wizard start_wizard-cli-reference start_wizard-cli-automation start_openclaw
process_section "Core Concepts" concepts_features concepts_multi-agent start_showcase
process_section "Channels" channels channels_telegram
process_section "Gateway & Operations" gateway gateway_configuration gateway_security gateway_remote gateway_tailscale gateway_troubleshooting
process_section "Agents & Tools" pi tools providers
process_section "Platforms & Nodes" platforms nodes
process_section "Web Interface" web web_control-ui
process_section "Reference" cli help reference_credits

echo "处理完成！"
echo "输出文件: $OUTPUT_FILE"
echo "文件大小: $(du -h "$OUTPUT_FILE" | cut -f1)"
