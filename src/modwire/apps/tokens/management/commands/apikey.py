from django.core.management.base import BaseCommand

from modwire.apps.tokens.auth import API_KEY_HEADER
from modwire.apps.tokens.services.api_key import ApiKeyService


class Command(BaseCommand):
    help = "Generate an API key."

    def handle(self, *args, **opts):
        api_key, key = ApiKeyService().generate("api key")
        self.stdout.write(f"key={key}")
        self.stdout.write(f"header={API_KEY_HEADER}")
