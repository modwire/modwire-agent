from hashlib import sha256
from secrets import token_urlsafe

from .api_key import ApiKey


class ApiKeyPolicy:
    def issue(self, name: str) -> tuple[ApiKey, str]:
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("An API key name is required.")
        secret = token_urlsafe(32)
        return (
            ApiKey(None, normalized_name, secret[:12], sha256(secret.encode()).hexdigest(), True, None, None, None),
            secret,
        )
