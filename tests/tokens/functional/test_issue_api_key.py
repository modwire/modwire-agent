from django.test import TestCase

from modwire.tokens.domain.api_key import ApiKey
from modwire.tokens.domain.api_key_policy import ApiKeyPolicy
from modwire.tokens.ports.api_key_store import ApiKeyStore
from modwire.tokens.use_cases.issue_api_key import IssueApiKey


class InMemoryApiKeyStore(ApiKeyStore):
    def save(self, api_key: ApiKey) -> ApiKey:
        return ApiKey(1, api_key.name, api_key.prefix, api_key.secret_hash, api_key.is_active, None, None, None)


class IssueApiKeyScenarios(TestCase):
    def test_returns_the_secret_only_when_the_key_is_issued(self) -> None:
        api_key, secret = IssueApiKey(InMemoryApiKeyStore(), ApiKeyPolicy()).execute("automation")

        self.assertEqual(api_key.identifier, 1)
        self.assertEqual(api_key.prefix, secret[:12])
        self.assertNotEqual(api_key.secret_hash, secret)
