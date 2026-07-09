from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils.text import slugify

from records.models.record import Record
from records.models.section import Section
from records.models.tag import Tag, slug_validator


@dataclass(frozen=True)
class RecordSearchResult:
    kind: str
    slug: str
    score: float
    title: str
    section_slug: str


@dataclass(frozen=True)
class SectionSearchResult:
    kind: str
    slug: str
    score: float
    title: str


def slug_from_name(value: str) -> str:
    slug = slugify(value)
    if not slug:
        raise ValidationError("A non-empty slug cannot be generated from this value.")
    slug_validator(slug)
    return slug


def set_tags(instance: Section | Record, tag_slugs: list[str]) -> None:
    if not tag_slugs:
        raise ValidationError({"tag_slugs": "At least one tag slug is required."})
    tags = list(Tag.objects.filter(slug__in=tag_slugs))
    missing = sorted(set(tag_slugs) - {tag.slug for tag in tags})
    if missing:
        raise ValidationError({"tag_slugs": f"Unknown tags: {', '.join(missing)}"})
    instance.tags.set(tags)


def filter_by_tags(queryset: QuerySet, tag_slugs: list[str]) -> QuerySet:
    for tag_slug in tag_slugs:
        queryset = queryset.filter(tags__slug=tag_slug)
    return queryset.distinct()


def lexical_score(query: str, text: str) -> float:
    tokens = [token for token in query.lower().split() if token]
    haystack = text.lower()
    matches = sum(1 for token in tokens if token in haystack)
    return float(matches) / float(len(tokens) or 1)


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    left_values = list(left)
    right_values = list(right)
    dot = sum(a * b for a, b in zip(left_values, right_values, strict=False))
    left_norm = math.sqrt(sum(value * value for value in left_values))
    right_norm = math.sqrt(sum(value * value for value in right_values))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)
