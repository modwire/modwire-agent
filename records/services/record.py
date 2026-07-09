from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from wireup import injectable

from records.embeddings import embed_text

from ..models.content import Content
from ..models.record import Record, build_record_slug
from ..models.section import Section
from .shared import (
    RecordSearchResult,
    SectionSearchResult,
    cosine_similarity,
    filter_by_tags,
    lexical_score,
    set_tags,
    slug_from_name,
)


@injectable
class RecordService:
    model = Record

    def list(
        self,
        limit: int,
        offset: int,
        section_slugs: list[str],
        tag_slugs: list[str],
    ):
        queryset = self.model.objects.select_related("section").prefetch_related("tags")
        if section_slugs:
            queryset = queryset.filter(section_id__in=section_slugs)
        queryset = filter_by_tags(queryset, tag_slugs)
        return queryset[offset : offset + limit]

    def get(self, record_slug: str):
        return get_object_or_404(
            self.model.objects.select_related("section").prefetch_related("content", "tags"),
            slug=record_slug,
        )

    @transaction.atomic
    def create(self, **data):
        tag_slugs = data.pop("tag_slugs", [])
        content_items = data.pop("content", [])
        if not tag_slugs:
            raise ValidationError({"tag_slugs": "At least one tag slug is required."})
        if not content_items:
            raise ValidationError({"content": "At least one content block is required."})
        section_slug = data.pop("section_slug")
        section = get_object_or_404(Section, slug=section_slug)
        local_slug = slug_from_name(data["title"])
        record_slug = build_record_slug(section.slug, local_slug)
        if self.model.objects.filter(slug=record_slug).exists():
            raise ValidationError({"title": f"Record '{record_slug}' already exists."})

        record = self.model(
            slug=record_slug,
            local_slug=local_slug,
            section=section,
            **data,
        )
        record.search_text = self.search_text_from_items(record, content_items, tuple(tag_slugs))
        record.embedding = embed_text(record.search_text)
        record.full_clean()
        record.save()
        self.replace_content(record, content_items)
        set_tags(record, tag_slugs)
        return record

    @transaction.atomic
    def update(self, record_slug: str, **data):
        instance = self.get(record_slug)
        has_tag_slugs = "tag_slugs" in data
        has_content = "content" in data
        tag_slugs = data.pop("tag_slugs", [])
        content_items = data.pop("content", None)
        if has_tag_slugs and not tag_slugs:
            raise ValidationError({"tag_slugs": "At least one tag slug is required."})
        if has_content and not content_items:
            raise ValidationError({"content": "At least one content block is required."})
        for field, value in data.items():
            setattr(instance, field, value)
        effective_tags = (
            tag_slugs if has_tag_slugs else list(instance.tags.values_list("slug", flat=True))
        )
        instance.search_text = (
            self.search_text_from_items(instance, content_items, tuple(effective_tags))
            if has_content and content_items is not None
            else self.search_text(instance, tuple(effective_tags))
        )
        instance.embedding = embed_text(instance.search_text)
        instance.full_clean()
        instance.save()
        if has_content and content_items is not None:
            self.replace_content(instance, content_items)
        if has_tag_slugs:
            set_tags(instance, tag_slugs)
        return instance

    def delete(self, record_slug: str):
        instance = self.get(record_slug)
        instance.delete()

    def replace_content(self, record: Record, content_items: list[dict]) -> None:
        record.content.all().delete()
        for position, content_item in enumerate(content_items):
            content = Content(record=record, position=position, **content_item)
            content.full_clean()
            content.save()

    def search_text(self, record: Record, tag_slugs: tuple[str, ...] = ()) -> str:
        tags = list(tag_slugs) or list(record.tags.values_list("slug", flat=True))
        content_text = "\n".join(record.content.order_by("position").values_list("content", flat=True))
        return "\n".join(
            [
                record.slug,
                record.local_slug,
                record.section_id,
                record.title,
                record.description,
                content_text,
                " ".join(tags),
            ]
        ).strip()

    def search_text_from_items(
        self,
        record: Record,
        content_items: list[dict],
        tag_slugs: tuple[str, ...] = (),
    ) -> str:
        content_text = "\n".join(item["content"] for item in content_items)
        return "\n".join(
            [
                record.slug,
                record.local_slug,
                record.section_id,
                record.title,
                record.description,
                content_text,
                " ".join(tag_slugs),
            ]
        ).strip()

    def search(
        self,
        query: str,
        mode: str,
        target: str,
        limit: int,
        offset: int,
        section_slugs: list[str],
        tag_slugs: list[str],
    ) -> list[RecordSearchResult | SectionSearchResult]:
        results: list[RecordSearchResult | SectionSearchResult] = []
        if target in {"records", "all"}:
            results.extend(self.search_records(query, mode, section_slugs, tag_slugs))
        if target in {"sections", "all"}:
            results.extend(self.search_sections(query, mode, section_slugs, tag_slugs))
        return sorted(results, key=lambda item: (-item.score, item.kind, item.slug))[
            offset : offset + limit
        ]

    def search_records(
        self,
        query: str,
        mode: str,
        section_slugs: list[str],
        tag_slugs: list[str],
    ) -> list[RecordSearchResult]:
        queryset = self.model.objects.select_related("section").prefetch_related("tags")
        if section_slugs:
            queryset = queryset.filter(section_id__in=section_slugs)
        queryset = filter_by_tags(queryset, tag_slugs)
        query_embedding = embed_text(query) if mode == "vector" else []
        results = []
        for record in queryset:
            score = (
                cosine_similarity(query_embedding, record.embedding)
                if mode == "vector"
                else lexical_score(query, record.search_text)
            )
            if score > 0:
                results.append(
                    RecordSearchResult(
                        "record",
                        record.slug,
                        score,
                        record.title,
                        record.section_id,
                    )
                )
        return results

    def search_sections(
        self,
        query: str,
        mode: str,
        section_slugs: list[str],
        tag_slugs: list[str],
    ) -> list[SectionSearchResult]:
        queryset = filter_by_tags(Section.objects.prefetch_related("tags"), tag_slugs)
        if section_slugs:
            queryset = queryset.filter(slug__in=section_slugs)
        query_embedding = embed_text(query) if mode == "vector" else []
        results = []
        for section in queryset:
            score = (
                cosine_similarity(query_embedding, section.embedding)
                if mode == "vector"
                else lexical_score(query, section.search_text)
            )
            if score > 0:
                results.append(SectionSearchResult("section", section.slug, score, section.title))
        return results
