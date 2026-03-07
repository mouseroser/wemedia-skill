#!/usr/bin/env node

// OpenClaw 文档抓取脚本 - 使用 Playwright
const fs = require('fs');
const path = require('path');

const DOCS_DIR = path.join(process.env.HOME, '.openclaw/workspace/agents/notebooklm/docs');
const RAW_DIR = path.join(DOCS_DIR, 'raw_md');

// 确保目录存在
if (!fs.existsSync(RAW_DIR)) {
  fs.mkdirSync(RAW_DIR, { recursive: true });
}

// 文档页面列表
const urls = [
  { url: 'https://docs.openclaw.ai/', name: 'index' },
  { url: 'https://docs.openclaw.ai/install', name: 'install' },
  { url: 'https://docs.openclaw.ai/start/getting-started', name: 'start_getting-started' },
  { url: 'https://docs.openclaw.ai/start/quickstart', name: 'start_quickstart' },
  { url: 'https://docs.openclaw.ai/start/hubs', name: 'start_hubs' },
  { url: 'https://docs.openclaw.ai/start/onboarding-overview', name: 'start_onboarding-overview' },
  { url: 'https://docs.openclaw.ai/start/onboarding', name: 'start_onboarding' },
  { url: 'https://docs.openclaw.ai/start/wizard', name: 'start_wizard' },
  { url: 'https://docs.openclaw.ai/start/wizard-cli-reference', name: 'start_wizard-cli-reference' },
  { url: 'https://docs.openclaw.ai/start/wizard-cli-automation', name: 'start_wizard-cli-automation' },
  { url: 'https://docs.openclaw.ai/start/openclaw', name: 'start_openclaw' },
  { url: 'https://docs.openclaw.ai/start/showcase', name: 'start_showcase' },
  { url: 'https://docs.openclaw.ai/concepts/features', name: 'concepts_features' },
  { url: 'https://docs.openclaw.ai/concepts/multi-agent', name: 'concepts_multi-agent' },
  { url: 'https://docs.openclaw.ai/channels', name: 'channels' },
  { url: 'https://docs.openclaw.ai/channels/telegram', name: 'channels_telegram' },
  { url: 'https://docs.openclaw.ai/gateway', name: 'gateway' },
  { url: 'https://docs.openclaw.ai/gateway/configuration', name: 'gateway_configuration' },
  { url: 'https://docs.openclaw.ai/gateway/configuration-reference', name: 'gateway_configuration-reference' },
  { url: 'https://docs.openclaw.ai/gateway/security', name: 'gateway_security' },
  { url: 'https://docs.openclaw.ai/gateway/remote', name: 'gateway_remote' },
  { url: 'https://docs.openclaw.ai/gateway/tailscale', name: 'gateway_tailscale' },
  { url: 'https://docs.openclaw.ai/gateway/troubleshooting', name: 'gateway_troubleshooting' },
  { url: 'https://docs.openclaw.ai/pi', name: 'pi' },
  { url: 'https://docs.openclaw.ai/tools', name: 'tools' },
  { url: 'https://docs.openclaw.ai/providers', name: 'providers' },
  { url: 'https://docs.openclaw.ai/platforms', name: 'platforms' },
  { url: 'https://docs.openclaw.ai/nodes', name: 'nodes' },
  { url: 'https://docs.openclaw.ai/cli', name: 'cli' },
  { url: 'https://docs.openclaw.ai/web', name: 'web' },
  { url: 'https://docs.openclaw.ai/web/control-ueb_control-ui' },
  { url: 'https://docs.openclaw.ai/help', name: 'help' },
  { url: 'https://docs.openclaw.ai/reference/credits', name: 'reference_credits' },
];

console.log(JSON.stringify(urls));
