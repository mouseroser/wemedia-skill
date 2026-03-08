from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RerankBackend(ABC):
    name: str
    model_name: str

    @abstractmethod
    def rerank(self, query: str, documents: list[str]) -> list[float]:
        raise NotImplementedError

    def health_payload(self) -> dict[str, Any]:
        return {
            "backend": self.name,
            "model": self.model_name,
        }
