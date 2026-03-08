#!/usr/bin/env bash
set -euo pipefail

LABEL="com.openclaw.local-rerank-sidecar"
PLIST_DST="$HOME/Library/LaunchAgents/com.openclaw.local-rerank-sidecar.plist"
UID_NUM="$(id -u)"

launchctl bootout "gui/$UID_NUM/$LABEL" >/dev/null 2>&1 || true
rm -f "$PLIST_DST"

echo "uninstalled $LABEL"
