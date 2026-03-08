#!/usr/bin/env python3
import json
import logging
import os
import sys
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch


HOST = os.environ.get("LOCAL_RERANK_HOST", "127.0.0.1")
PORT = int(os.environ.get("LOCAL_RERANK_PORT", "8765"))
MODEL_NAME = os.environ.get(
    "LOCAL_RERANK_MODEL", "BAAI/bge-reranker-v2-m3"
)
MAX_LENGTH = int(os.environ.get("LOCAL_RERANK_MAX_LENGTH", "512"))
LOG_LEVEL = os.environ.get("LOCAL_RERANK_LOG_LEVEL", "INFO").upper()


logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("local-rerank-sidecar")


@dataclass
class AppState:
    model_name: str
    device: str
    tokenizer: Any
    model: Any


def detect_device() -> str:
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_state() -> AppState:
    device = detect_device()
    logger.info("loading reranker model %s on %s", MODEL_NAME, device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
    )
    model.to(device)
    model.eval()
    logger.info("reranker model ready")
    return AppState(
        model_name=MODEL_NAME,
        device=device,
        tokenizer=tokenizer,
        model=model,
    )


STATE = load_state()


def rerank(query: str, documents: list[str]) -> list[float]:
    pairs = [[query, doc] for doc in documents]
    with torch.inference_mode():
        inputs = STATE.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )
        inputs = {k: v.to(STATE.device) for k, v in inputs.items()}
        logits = STATE.model(**inputs).logits
        if logits.ndim > 1:
            logits = logits[:, 0]
        scores = torch.sigmoid(logits).detach().cpu().tolist()
    return [float(score) for score in scores]


class Handler(BaseHTTPRequestHandler):
    server_version = "LocalRerankSidecar/0.1"

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/health", "/healthz"):
            self._send_json(
                200,
                {
                    "ok": True,
                    "model": STATE.model_name,
                    "device": STATE.device,
                    "port": PORT,
                },
            )
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path != "/v1/rerank":
            self._send_json(404, {"error": "not_found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)

        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(400, {"error": "invalid_json"})
            return

        query = payload.get("query")
        documents = payload.get("documents")
        top_n = payload.get("top_n")

        if not isinstance(query, str) or not isinstance(documents, list):
            self._send_json(400, {"error": "invalid_request"})
            return

        normalized_docs: list[str] = []
        for item in documents:
            if isinstance(item, str):
                normalized_docs.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                normalized_docs.append(item["text"])
            else:
                normalized_docs.append("")

        if top_n is None or not isinstance(top_n, int) or top_n <= 0:
            top_n = len(normalized_docs)

        try:
            scores = rerank(query, normalized_docs)
        except Exception as exc:
            logger.exception("rerank failed")
            self._send_json(500, {"error": "rerank_failed", "detail": str(exc)})
            return

        ranked = sorted(
            [
                {
                    "index": idx,
                    "relevance_score": score,
                }
                for idx, score in enumerate(scores)
            ],
            key=lambda item: item["relevance_score"],
            reverse=True,
        )[:top_n]

        self._send_json(
            200,
            {
                "model": payload.get("model") or STATE.model_name,
                "results": ranked,
            },
        )

    def log_message(self, fmt: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), fmt % args)


if __name__ == "__main__":
    logger.info("starting local rerank sidecar on %s:%s", HOST, PORT)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("shutting down")
        server.server_close()
        sys.exit(0)
