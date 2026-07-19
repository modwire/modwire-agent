from modwire_hex import Module, Providers

from .adapters.api_key.django_api_key_store import DjangoApiKeyStore
from .domain.api_key_policy import ApiKeyPolicy
from .ports.api_key_store import ApiKeyStore
from .use_cases.issue_api_key import IssueApiKey


tokens = Module.auto(
    "tokens",
    roots=(IssueApiKey,),
    bindings=(
        Providers.bind(ApiKeyStore, DjangoApiKeyStore, "scoped", None),
        Providers.singleton(ApiKeyPolicy, None),
    ),
)
