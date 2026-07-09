from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.api_key import ApiKey


@injectable
class ApiKeyService:
    model = ApiKey

    def list(self):
        return self.model.objects.order_by("id")

    def get(self, api_key_id: int):
        return get_object_or_404(self.model, id=api_key_id)

    def create(self, **data):
        return self.model.objects.create(**data)

    def generate(self, name: str):
        return self.model.generate(name)

    def update(self, api_key_id: int, **data):
        instance = self.get(api_key_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, api_key_id: int):
        instance = self.get(api_key_id)
        instance.delete()
