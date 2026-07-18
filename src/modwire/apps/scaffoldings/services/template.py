from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.scaffolding import Scaffolding
from ..models.template import Template


@injectable
class TemplateService:
    model = Template

    def list(self):
        return self.model.objects.order_by("relative_path")

    def get(self, template_id: str):
        return get_object_or_404(self.model, id=template_id)

    def create(self, scaffolding_id: str, **data):
        instance = self.model(scaffolding=get_object_or_404(Scaffolding, id=scaffolding_id), **data)
        instance.full_clean()
        instance.save()
        return instance

    def update(self, template_id: str, **data):
        instance = self.get(template_id)
        if "scaffolding_id" in data:
            instance.scaffolding = get_object_or_404(Scaffolding, id=data.pop("scaffolding_id"))
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, template_id: str):
        instance = self.get(template_id)
        instance.delete()
