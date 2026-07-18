from django.shortcuts import get_object_or_404
from wireup import injectable

from modwire.apps.languages.models.language import Language

from ..models.scaffolding import Scaffolding


@injectable
class ScaffoldingService:
    model = Scaffolding

    def list(self):
        return self.model.objects.order_by("name")

    def get(self, scaffolding_id: str):
        return get_object_or_404(self.model, id=scaffolding_id)

    def create(self, language_id: str, name: str, description: str):
        scaffolding = self.model(
            language=get_object_or_404(Language, id=language_id),
            name=name,
            description=description,
        )
        scaffolding.full_clean()
        scaffolding.save()
        return scaffolding

    def update(self, scaffolding_id: str, **data):
        instance = self.get(scaffolding_id)
        if "language_id" in data:
            instance.language = get_object_or_404(Language, id=data.pop("language_id"))
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, scaffolding_id: str):
        instance = self.get(scaffolding_id)
        instance.delete()
