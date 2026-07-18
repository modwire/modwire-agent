from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel
from pgvector.django import VectorField

from .tag import Tag, slug_validator

EMBEDDING_DIMENSIONS = 384


class Section(TimeStampedModel):
    slug = models.SlugField(primary_key=True, max_length=80, validators=[slug_validator])
    title = models.CharField(max_length=160)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="sections")
    search_text = models.TextField()
    embedding = VectorField(dimensions=EMBEDDING_DIMENSIONS)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.slug

    def clean(self):
        super().clean()
        slug_validator(self.slug)
        if not self.search_text:
            raise ValidationError({"search_text": "Section search text is required."})
        if not isinstance(self.embedding, list):
            raise ValidationError({"embedding": "Section embedding must be a list."})
        if len(self.embedding) != EMBEDDING_DIMENSIONS:
            raise ValidationError({"embedding": "Section embedding is required."})
