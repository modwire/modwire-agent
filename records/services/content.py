from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.content import Content
from ..models.record import Record


@injectable
class ContentService:
    model = Content

    def list(self):
        return self.model.objects.select_related("record").order_by("record_id", "position", "id")

    def get(self, content_id: int):
        return get_object_or_404(self.model, id=content_id)

    def create(self, **data):
        record_slug = data.pop("record_slug")
        data["record"] = get_object_or_404(Record, slug=record_slug)
        instance = self.model(**data)
        instance.full_clean()
        instance.save()
        return instance

    def update(self, content_id: int, **data):
        instance = self.get(content_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, content_id: int):
        instance = self.get(content_id)
        instance.delete()
