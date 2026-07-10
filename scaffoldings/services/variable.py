from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.variable import Variable


@injectable
class VariableService:
    model = Variable

    def list(self):
        return self.model.objects.order_by("name")

    def get(self, variable_id: str):
        return get_object_or_404(self.model, id=variable_id)

    def create(self, **data):
        assert not self.model.objects.filter(name=data["name"]).exists()
        return self.model.objects.create(**data)

    def update(self, variable_id: str, **data):
        instance = self.get(variable_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, variable_id: str):
        instance = self.get(variable_id)
        instance.delete()
