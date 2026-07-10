from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.language import Language


@injectable
class LanguageService:
    model = Language

    def list(self):
        return self.model.objects.order_by("name")

    def get(self, language_id: str):
        return get_object_or_404(self.model, id=language_id)

    def create(self, **data):
        instance = self.model(**data)
        instance.full_clean()
        instance.save()
        return instance

    def update(self, language_id: str, **data):
        instance = self.get(language_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, language_id: str):
        instance = self.get(language_id)
        instance.delete()
