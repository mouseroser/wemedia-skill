#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/lucifinil_chen/.openclaw/workspace"
PID_FILE="$ROOT/runtime/local-rerank-sidecar/server.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "local-rerank-sidecar is not running"
  exit 0
fi

PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "stopped local-rerank-sidecar (pid $PID)"
else
  echo "stale pid file removed"
fi

rm -f "$PID_FILE"
