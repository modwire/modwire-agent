from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

from .section import Section
from .tag import Tag, slug_validator


def build_record_slug(section_slug: str, local_slug: str) -> str:
    return f"{section_slug}/{local_slug}"


class Record(TimeStampedModel):
    slug = models.CharField(primary_key=True, max_length=180)
    local_slug = models.SlugField(max_length=80, validators=[slug_validator])
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name="records")
    title = models.CharField(max_length=160)
    description = models.TextField()
    sources = models.JSONField()
    tags = models.ManyToManyField(Tag, related_name="records")
    search_text = models.TextField()
    embedding = models.JSONField()

    class Meta:
        ordering = ["slug"]
        constraints = [
            models.UniqueConstraint(
                fields=["section", "local_slug"],
                name="unique_record_local_slug_per_section",
            ),
        ]

    def __str__(self):
        return self.slug

    def clean(self):
        super().clean()
        slug_validator(self.local_slug)
        expected = build_record_slug(self.section_id, self.local_slug)
        if self.slug and self.slug != expected:
            raise ValidationError({"slug": f"Record slug must be '{expected}'."})
        if not isinstance(self.sources, list) or any(
            not isinstance(source, str) or not source for source in self.sources
        ):
            raise ValidationError({"sources": "Record sources must be a list of URLs."})
        if not self.sources:
            raise ValidationError({"sources": "At least one record source is required."})
        if not self.search_text:
            raise ValidationError({"search_text": "Record search text is required."})
        if not isinstance(self.embedding, list):
            raise ValidationError({"embedding": "Record embedding must be a list."})
        if not self.embedding:
            raise ValidationError({"embedding": "Record embedding is required."})
