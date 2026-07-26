from dataclasses import dataclass

from django.shortcuts import get_object_or_404

from modwire_agent.languages.use_cases.language.get_language import GetLanguage

from ...ports.outbound import ScaffoldingCatalog
from ..django.models import Scaffolding


@dataclass(frozen=True, slots=True)
class DjangoScaffoldingStore(ScaffoldingCatalog):
    model = Scaffolding
    languages: GetLanguage

    def list(self):
        return self.model.objects.order_by("name")

    def get(self, scaffolding_id: str):
        return get_object_or_404(self.model, id=scaffolding_id)

    def create(self, language_id: str, name: str, description: str):
        language = self.languages.execute(language_id)
        scaffolding = self.model(
            language_id=language.id,
            name=name,
            description=description,
        )
        scaffolding.full_clean()
        scaffolding.save()
        return scaffolding

    def update(self, scaffolding_id: str, data: dict[str, object]):
        instance = self.get(scaffolding_id)
        if "language_id" in data:
            instance.language_id = self.languages.execute(str(data.pop("language_id"))).id
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, scaffolding_id: str):
        instance = self.get(scaffolding_id)
        instance.delete()
