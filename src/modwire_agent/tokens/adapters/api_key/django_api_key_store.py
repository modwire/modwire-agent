from modwire_hex.django import DjangoRepository

from ...domain.api_key import ApiKey
from ...ports.api_key.api_key_store import ApiKeyStore
from ..django.models import api_key


class DjangoApiKeyStore(DjangoRepository[ApiKey, api_key.ApiKey, int | None], ApiKeyStore):
    def key_of(self, domain: ApiKey) -> int | None:
        return domain.identifier

    def find_record(self, key: int | None) -> api_key.ApiKey | None:
        if key is None:
            return None
        try:
            return api_key.ApiKey.objects.get(id=key)
        except api_key.ApiKey.DoesNotExist:
            return None

    def create_record(self, domain: ApiKey) -> api_key.ApiKey:
        return api_key.ApiKey(
            name=domain.name,
            prefix=domain.prefix,
            key_hash=domain.secret_hash,
            is_active=domain.is_active,
        )

    def update_record(self, model: api_key.ApiKey, domain: ApiKey) -> None:
        model.name = domain.name
        model.is_active = domain.is_active

    def to_domain(self, model: api_key.ApiKey) -> ApiKey:
        return ApiKey(
            model.id,
            model.name,
            model.prefix,
            model.key_hash,
            model.is_active,
            model.created_at,
            model.updated_at,
            model.last_used_at,
        )

    def save(self, api_key: ApiKey) -> ApiKey:
        super().save(api_key)
        return self.load(api_key.identifier) if api_key.identifier is not None else self._latest(api_key.prefix)

    def _latest(self, prefix: str) -> ApiKey:
        return self.to_domain(api_key.ApiKey.objects.get(prefix=prefix))
