from django.shortcuts import get_object_or_404

from ...ports.variable_catalog import VariableCatalog
from ..django.models.scaffolding import Scaffolding
from ..django.models.variable import Variable


class DjangoVariableStore(VariableCatalog):
    model = Variable

    def list(self):
        return self.model.objects.order_by("name")

    def get(self, variable_id: str):
        return get_object_or_404(self.model, id=variable_id)

    def create(self, scaffolding_id: str, **data):
        instance = self.model(scaffolding=get_object_or_404(Scaffolding, id=scaffolding_id), **data)
        instance.full_clean()
        instance.save()
        return instance

    def update(self, variable_id: str, **data):
        instance = self.get(variable_id)
        if "scaffolding_id" in data:
            instance.scaffolding = get_object_or_404(Scaffolding, id=data.pop("scaffolding_id"))
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, variable_id: str):
        instance = self.get(variable_id)
        instance.delete()
from ...ports.variable_catalog import VariableCatalog
