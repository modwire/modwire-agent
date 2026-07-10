from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.scaffolding import Scaffolding
from ...languages.models.language import Language


@injectable
class ScaffoldingService:
    model = Scaffolding

    def list(self):
        return self.model.objects.order_by("name")

    def get(self, slug: str):
        return get_object_or_404(self.model, slug=slug)

    def create(self, language_id: str, name: str, description: str):
        scaffold = self.model(language=get_object_or_404(Language, id=language_id))
        assert not self.model.objects.filter(name=name).exists()
        
        scaffold.name = name
        scaffold.description = description
        scaffold.save()

    def update(self, slug: str, **data):
        instance = self.get(slug)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, slug: str):
        instance = self.get(slug)
        instance.delete()
