#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/lucifinil_chen/.openclaw/workspace"
PID_FILE="$ROOT/runtime/local-rerank-sidecar/server.pid"
PORT="${LOCAL_RERANK_PORT:-8765}"
HOST="${LOCAL_RERANK_HOST:-127.0.0.1}"
LABEL="com.openclaw.local-rerank-sidecar"
UID_NUM="$(id -u)"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "manual process: running (pid $(cat "$PID_FILE"))"
else
  echo "manual process: stopped"
fi

if launchctl print "gui/$UID_NUM/$LABEL" >/dev/null 2>&1; then
  echo "launchd: loaded ($LABEL)"
else
  echo "launchd: not loaded"
fi

if curl -fsS "http://$HOST:$PORT/health"; then
  exit 0
fi

echo "health: unavailable"
exit 1
