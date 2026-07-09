from __future__ import annotations

import hashlib
import math
from typing import Protocol

from django.conf import settings


class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError


class DeterministicEmbeddingProvider:
    def __init__(self, dimensions: int) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        buckets = [0.0] * self.dimensions
        tokens = text.lower().split() or [""]
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            buckets[bucket] += sign

        norm = math.sqrt(sum(value * value for value in buckets)) or 1.0
        return [value / norm for value in buckets]


def empty_embedding() -> list[float]:
    return [0.0] * int(getattr(settings, "RECORDS_EMBEDDING_DIMENSIONS", 384))


def get_embedding_provider() -> EmbeddingProvider:
    provider = getattr(settings, "RECORDS_EMBEDDING_PROVIDER", "deterministic")
    if provider == "deterministic":
        return DeterministicEmbeddingProvider(
            int(getattr(settings, "RECORDS_EMBEDDING_DIMENSIONS", 384))
        )
    raise RuntimeError(f"Unsupported embedding provider '{provider}'.")


def embed_text(text: str) -> list[float]:
    if not getattr(settings, "RECORDS_EMBEDDINGS_ENABLED", True):
        return empty_embedding()
    return get_embedding_provider().embed(text)
