from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.template import Template


@injectable
class TemplateService:
    model = Template

    def list(self):
        return self.model.objects.order_by("id")

    def get(self, template_id: int):
        return get_object_or_404(self.model, id=template_id)

    def create(self, **data):
        return self.model.objects.create(**data)

    def update(self, template_id: int, **data):
        instance = self.get(template_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, template_id: int):
        instance = self.get(template_id)
        instance.delete()
