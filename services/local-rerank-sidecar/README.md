# Local Rerank Sidecar

A local Jina-compatible rerank service for `memory-lancedb-pro`.

## Why this exists

- Keeps `memory-lancedb-pro` unchanged
- Exposes `POST /v1/rerank` in the format the plugin already understands
- Uses a single stable production path: local Transformers cross-encoder reranking

## Fixed external interface

- `GET /health`
- `POST /v1/rerank`

OpenClaw always talks to the same sidecar endpoint.

## Runtime

- Backend: local Hugging Face Transformers
- Default model: `BAAI/bge-reranker-v2-m3`
- Current production default on this machine

## Key environment variables

- `LOCAL_RERANK_MODEL=...`
- `LOCAL_RERANK_HOST=127.0.0.1`
- `LOCAL_RERANK_PORT=8765`

## Scripts

- `scripts/start-local-rerank-sidecar.sh` - one-off manual start
- `scripts/stop-local-rerank-sidecar.sh` - stop one-off manual process
- `scripts/status-local-rerank-sidecar.sh` - show manual process, launchd state, and health
- `scripts/install-local-rerank-sidecar-launchd.sh` - install auto-start service via launchd
- `scripts/uninstall-local-rerank-sidecar-launchd.sh` - remove launchd service

## Notes

- The first startup downloads model weights locally, so it can take a while.
- `Ollama` is still used elsewhere for embeddings, but no longer participates in reranking.
