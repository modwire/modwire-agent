from django.core.management.base import BaseCommand

from modwire.tokens.adapters.api_key.django_api_key_store import DjangoApiKeyStore
from modwire.tokens.domain.api_key_policy import ApiKeyPolicy
from modwire.tokens.use_cases.issue_api_key import IssueApiKey


class Command(BaseCommand):
    help = "Generate an API key."

    def handle(self, *args, **opts):
        api_key, key = IssueApiKey(DjangoApiKeyStore(), ApiKeyPolicy()).execute("api key")
        self.stdout.write(f"key={key}")
        self.stdout.write("header=X-API-Key")
