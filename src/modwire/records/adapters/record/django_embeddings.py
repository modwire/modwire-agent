import hashlib
import math


class DeterministicEmbeddings:
    def embed(self, text: str) -> list[float]:
        buckets = [0.0] * 384
        for token in text.lower().split() or [""]:
            digest = hashlib.sha256(token.encode()).digest()
            bucket = int.from_bytes(digest[:4], "big") % 384
            buckets[bucket] += 1.0 if digest[4] % 2 == 0 else -1.0
        norm = math.sqrt(sum(value * value for value in buckets)) or 1.0
        return [value / norm for value in buckets]
