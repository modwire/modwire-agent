from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.language import Language


@injectable
class LanguageService:
    model = Language

    def list(self):
        return self.model.objects.order_by("id")

    def get(self, language_id: int):
        return get_object_or_404(self.model, id=language_id)

    def create(self, **data):
        return self.model.objects.create(**data)

    def update(self, language_id: int, **data):
        instance = self.get(language_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, language_id: int):
        instance = self.get(language_id)
        instance.delete()
