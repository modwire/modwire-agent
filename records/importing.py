from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from django.db import transaction

from records.models.record import build_record_slug
from records.services.record import RecordService
from records.services.section import SectionService
from records.services.shared import slug_from_name
from records.services.tag import TagService


class ScrapedContentLike(Protocol):
    def as_record_content(self) -> dict:
        raise NotImplementedError


class ScrapedRecordLike(Protocol):
    title: str
    description: str
    sources: list[str]
    content: list[ScrapedContentLike]
    tag_names: list[str]


@dataclass(frozen=True)
class ImportResult:
    created: int
    updated: int
    skipped: int


@transaction.atomic
def import_scraped_records(
    *,
    section_title: str,
    section_description: str,
    section_tag_names: list[str],
    records: list[ScrapedRecordLike],
    update_existing: bool = True,
) -> ImportResult:
    tag_service = TagService()
    section_service = SectionService()
    record_service = RecordService()
    section_tag_slugs = ensure_tags(tag_service, section_tag_names)
    section = ensure_section(
        section_service,
        title=section_title,
        description=section_description,
        tag_slugs=section_tag_slugs,
    )

    created = 0
    updated = 0
    skipped = 0

    for scraped in records:
        tag_slugs = ensure_tags(tag_service, scraped.tag_names)
        local_slug = slug_from_name(scraped.title)
        record_slug = build_record_slug(section.slug, local_slug)
        data = {
            "section_slug": section.slug,
            "title": scraped.title,
            "description": scraped.description,
            "sources": scraped.sources,
            "tag_slugs": tag_slugs,
            "content": [block.as_record_content() for block in scraped.content],
        }

        if record_service.model.objects.filter(slug=record_slug).exists():
            if not update_existing:
                skipped += 1
                continue
            record_service.update(record_slug, **data)
            updated += 1
        else:
            record_service.create(**data)
            created += 1

    return ImportResult(created=created, updated=updated, skipped=skipped)


def ensure_tags(service: TagService, names: list[str]) -> list[str]:
    slugs = []
    for name in names:
        slug = slug_from_name(name)
        data = {"name": name, "description": name}
        if service.model.objects.filter(slug=slug).exists():
            service.update(slug, **data)
        else:
            service.create(**data)
        slugs.append(slug)
    return slugs


def ensure_section(service: SectionService, *, title: str, description: str, tag_slugs: list[str]):
    slug = slug_from_name(title)
    data = {"title": title, "description": description, "tag_slugs": tag_slugs}
    if service.model.objects.filter(slug=slug).exists():
        return service.update(slug, **data)
    return service.create(**data)
