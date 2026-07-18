from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from wireup import injectable

from modwire.apps.records.embeddings import embed_text

from ..models.section import Section
from .shared import filter_by_tags, set_tags, slug_from_name


@injectable
class SectionService:
    model = Section

    def list(self, limit: int, offset: int, tag_slugs: list[str]):
        queryset = filter_by_tags(self.model.objects.prefetch_related("tags"), tag_slugs)
        return queryset[offset : offset + limit]

    def get(self, slug: str):
        return get_object_or_404(self.model.objects.prefetch_related("tags"), slug=slug)

    @transaction.atomic
    def create(self, **data):
        tag_slugs = data.pop("tag_slugs", [])
        if not tag_slugs:
            raise ValidationError({"tag_slugs": "At least one tag slug is required."})
        slug = slug_from_name(data["title"])
        if self.model.objects.filter(slug=slug).exists():
            raise ValidationError({"title": f"Section '{slug}' already exists."})
        section = self.model(slug=slug, **data)
        section.search_text = self.search_text(section, tuple(tag_slugs))
        section.embedding = embed_text(section.search_text)
        section.full_clean()
        section.save()
        set_tags(section, tag_slugs)
        return section

    @transaction.atomic
    def update(self, slug: str, **data):
        instance = self.get(slug)
        has_tag_slugs = "tag_slugs" in data
        tag_slugs = data.pop("tag_slugs", [])
        if has_tag_slugs and not tag_slugs:
            raise ValidationError({"tag_slugs": "At least one tag slug is required."})
        for field, value in data.items():
            setattr(instance, field, value)
        effective_tags = (
            tag_slugs if has_tag_slugs else list(instance.tags.values_list("slug", flat=True))
        )
        instance.search_text = self.search_text(instance, tuple(effective_tags))
        instance.embedding = embed_text(instance.search_text)
        instance.full_clean()
        instance.save()
        if has_tag_slugs:
            set_tags(instance, tag_slugs)
        return instance

    @transaction.atomic
    def delete(self, slug: str):
        instance = self.get(slug)
        if instance.records.exists():
            raise ValidationError("Cannot delete a non-empty section.")
        instance.delete()

    def search_text(self, section: Section, tag_slugs: tuple[str, ...] = ()) -> str:
        tags = list(tag_slugs) or list(section.tags.values_list("slug", flat=True))
        return "\n".join([section.slug, section.title, section.description, " ".join(tags)]).strip()
