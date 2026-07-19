from dataclasses import dataclass

from ...domain.api_key import ApiKey
from ...domain.api_key_policy import ApiKeyPolicy
from ...ports.api_key.api_key_store import ApiKeyStore


@dataclass(frozen=True, slots=True)
class IssueApiKey:
    store: ApiKeyStore
    policy: ApiKeyPolicy

    def execute(self, name: str) -> tuple[ApiKey, str]:
        api_key, secret = self.policy.issue(name)
        return self.store.save(api_key), secret
