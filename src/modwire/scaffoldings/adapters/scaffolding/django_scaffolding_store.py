from django.shortcuts import get_object_or_404

from modwire.languages.use_cases import LanguageCatalogService

from ...ports.scaffolding_catalog import ScaffoldingCatalog
from ..django.models.scaffolding import Scaffolding


class DjangoScaffoldingStore(ScaffoldingCatalog):
    model = Scaffolding

    def __init__(self, catalog: LanguageCatalogService):
        self.catalog = catalog

    def list(self):
        return self.model.objects.order_by("name")

    def get(self, scaffolding_id: str):
        return get_object_or_404(self.model, id=scaffolding_id)

    def create(self, language_id: str, name: str, description: str):
        language = self.catalog.find(language_id)
        scaffolding = self.model(
            language_id=language.id,
            name=name,
            description=description,
        )
        scaffolding.full_clean()
        scaffolding.save()
        return scaffolding

    def update(self, scaffolding_id: str, **data):
        instance = self.get(scaffolding_id)
        if "language_id" in data:
            instance.language_id = self.catalog.find(data.pop("language_id")).id
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, scaffolding_id: str):
        instance = self.get(scaffolding_id)
        instance.delete()
