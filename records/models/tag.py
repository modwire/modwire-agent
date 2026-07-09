from django.core.validators import RegexValidator
from django.db import models
from model_utils.models import TimeStampedModel

SLUG_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
slug_validator = RegexValidator(
    SLUG_PATTERN,
    "Use lowercase letters, numbers, and hyphens. Hyphens cannot be leading, trailing, or repeated.",
)


class Tag(TimeStampedModel):
    slug = models.SlugField(primary_key=True, max_length=80, validators=[slug_validator])
    name = models.CharField(max_length=120)
    description = models.TextField()

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.slug
