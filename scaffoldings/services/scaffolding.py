from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.scaffolding import Scaffolding


@injectable
class ScaffoldingService:
    model = Scaffolding

    def list(self):
        return self.model.objects.order_by("id")

    def get(self, scaffolding_id: int):
        return get_object_or_404(self.model, id=scaffolding_id)

    def create(self, **data):
        return self.model.objects.create(**data)

    def update(self, scaffolding_id: int, **data):
        instance = self.get(scaffolding_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, scaffolding_id: int):
        instance = self.get(scaffolding_id)
        instance.delete()

    def import_from_code_package(self, )
