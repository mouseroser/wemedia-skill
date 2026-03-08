from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class SidecarConfig:
    host: str = "127.0.0.1"
    port: int = 8765
    model_name: str = "BAAI/bge-reranker-v2-m3"
    max_length: int = 512
    log_level: str = "INFO"


def load_config() -> SidecarConfig:
    return SidecarConfig(
        host=os.environ.get("LOCAL_RERANK_HOST", "127.0.0.1"),
        port=int(os.environ.get("LOCAL_RERANK_PORT", "8765")),
        model_name=os.environ.get(
            "LOCAL_RERANK_MODEL", "BAAI/bge-reranker-v2-m3"
        ),
        max_length=int(os.environ.get("LOCAL_RERANK_MAX_LENGTH", "512")),
        log_level=os.environ.get("LOCAL_RERANK_LOG_LEVEL", "INFO").upper(),
    )
