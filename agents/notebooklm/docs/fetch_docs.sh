#!/bin/bash

# OpenClaw 文档抓取脚本
# 从 docs.openclaw.ai 抓取所有英文文档页面

DOCS_DIR="$HOME/.openclaw/workspace/agents/notebooklm/docs/raw"
mkdir -p "$DOCS_DIR"

# 文档页面列表
URLS=(
  "https://docs.openclaw.ai/"
  "https://docs.openclaw.ai/install"
  "https://docs.openclaw.ai/start/getting-started"
  "https://docs.openclaw.ai/start/quickstart"
  "https://docs.openclaw.ai/start/hubs"
  "https://docs.openclaw.ai/start/onboarding-overview"
  "https://docs.openclaw.ai/start/onboarding"
  "https://docs.openclaw.ai/start/wizard"
  "https://docs.openclaw.ai/start/wizard-cli-reference"
  "https://docs.openclaw.ai/start/wizard-cli-automation"
  "https://docs.openclaw.ai/start/openclaw"
  "https://docs.openclaw.ai/start/showcase"
  "https://docs.openclaw.ai/concepts/features"
  "https://docs.openclaw.ai/concepts/multi-agent"
  "https://docs.openclaw.ai/channels"
  "https://docs.openclaw.ai/channels/telegram"
  "https://docs.openclaw.ai/gateway"
  "https://docs.openclaw.ai/gateway/configuration"
  "https://docs.openclaw.ai/gateway/security"
  "https://docs.openclaw.ai/gateway/remote"
  "https://docs.openclaw.ai/gateway/tailscale"
  "https://docs.openclaw.ai/gateway/troubleshooting"
  "https://docs.openclaw.ai/pi"
  "https://docs.openclaw.ai/tools"
  "https://docs.openclaw.ai/providers"
  "https://docs.openclaw.ai/platforms"
  "https://docs.openclaw.ai/nodes"
  "https://docs.openclaw.ai/cli"
  "https://docs.openclaw.ai/web"
  "https://docs.openclaw.ai/web/control-ui"
  "https://docs.openclaw.ai/help"
  "https://docs.openclaw.ai/reference/credits"
)

echo "开始抓取 ${#URLS[@]} 个文档页面..."

for url in "${URLS[@]}"; do
  # 生成文件名
  filename=$(echo "$url" | sed 's|https://docs.openclaw.ai/||' | sed 's|/$||' | sed 's|/|_|g')
  if [ -z "$filename" ]; then
    filename="index"
  fi
  
  output_file="$DOCS_DIR/${filename}.html"
  
  echo "抓取: $url -> ${filename}.html"
  
  # 使用 curl 抓取
  curl -s -L "$url" -o "$output_file"
  
  sleep 0.5  # 避免请求过快
done

echo "抓取完成！文件保存在: $DOCS_DIR"
