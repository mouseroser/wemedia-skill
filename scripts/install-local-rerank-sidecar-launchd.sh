#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/lucifinil_chen/.openclaw/workspace"
PLIST_SRC="$ROOT/services/local-rerank-sidecar/com.openclaw.local-rerank-sidecar.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.openclaw.local-rerank-sidecar.plist"
LABEL="com.openclaw.local-rerank-sidecar"
UID_NUM="$(id -u)"

mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "$ROOT/runtime/local-rerank-sidecar"
cp "$PLIST_SRC" "$PLIST_DST"

launchctl bootout "gui/$UID_NUM/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$UID_NUM" "$PLIST_DST"
launchctl kickstart -k "gui/$UID_NUM/$LABEL"

echo "installed and started $LABEL"
