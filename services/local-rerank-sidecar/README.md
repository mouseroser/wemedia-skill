# Local Rerank Sidecar

A local Jina-compatible rerank service for `memory-lancedb-pro`.

## Why this exists

- Keeps `memory-lancedb-pro` unchanged
- Exposes `POST /v1/rerank` in the format the plugin already understands
- Runs a local multilingual cross-encoder model by default: `BAAI/bge-reranker-v2-m3`
- Lets the backend evolve later without changing OpenClaw config

## Endpoints

- `GET /health`
- `POST /v1/rerank`

## Default model

- `BAAI/bge-reranker-v2-m3`

## Scripts

- `scripts/start-local-rerank-sidecar.sh` - one-off manual start
- `scripts/stop-local-rerank-sidecar.sh` - stop one-off manual process
- `scripts/status-local-rerank-sidecar.sh` - show manual process, launchd state, and health
- `scripts/install-local-rerank-sidecar-launchd.sh` - install auto-start service via launchd
- `scripts/uninstall-local-rerank-sidecar-launchd.sh` - remove launchd service

## Notes

- The first startup downloads model weights locally, so it can take a while.
- Current backend uses local Transformers on this machine.
- If Ollama gains a stable rerank API later, the sidecar can switch backends without changing `memory-lancedb-pro`.
