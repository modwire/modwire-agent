from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.tag import Tag
from .shared import slug_from_name


@injectable
class TagService:
    model = Tag

    def list(self):
        return self.model.objects.order_by("slug")

    def get(self, slug: str):
        return get_object_or_404(self.model, slug=slug)

    @transaction.atomic
    def create_batch(self, items: list[dict]) -> list[Tag]:
        result = []
        for item in items:
            slug = slug_from_name(item["name"])
            if self.model.objects.filter(slug=slug).exists():
                raise ValidationError({"name": f"Tag '{slug}' already exists."})
            tag = self.model(slug=slug, name=item["name"], description=item["description"])
            tag.full_clean()
            tag.save()
            result.append(tag)
        return result

    def create(self, **data):
        [tag] = self.create_batch([data])
        return tag

    def update(self, slug: str, **data):
        instance = self.get(slug)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, slug: str):
        instance = self.get(slug)
        instance.delete()
