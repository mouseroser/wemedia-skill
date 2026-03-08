from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from .base import RerankBackend


logger = logging.getLogger("local-rerank-sidecar")


@dataclass
class TransformersSettings:
    model_name: str
    max_length: int = 512


class TransformersBackend(RerankBackend):
    name = "transformers"

    def __init__(self, settings: TransformersSettings):
        self.model_name = settings.model_name
        self.max_length = settings.max_length
        self.device = self._detect_device()
        logger.info(
            "loading transformers reranker model %s on %s",
            self.model_name,
            self.device,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )
        self.model.to(self.device)
        self.model.eval()
        logger.info("transformers reranker model ready")

    @staticmethod
    def _detect_device() -> str:
        if torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def rerank(self, query: str, documents: list[str]) -> list[float]:
        pairs = [[query, doc] for doc in documents]
        with torch.inference_mode():
            inputs = self.tokenizer(
                pairs,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt",
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            logits = self.model(**inputs).logits
            if logits.ndim > 1:
                logits = logits[:, 0]
            scores = torch.sigmoid(logits).detach().cpu().tolist()
        return [float(score) for score in scores]

    def health_payload(self) -> dict[str, Any]:
        payload = super().health_payload()
        payload.update(
            {
                "device": self.device,
                "maxLength": self.max_length,
            }
        )
        return payload
