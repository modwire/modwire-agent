from django.db import models
from model_utils.models import TimeStampedModel


class Tag(TimeStampedModel):
    slug = models.SlugField(primary_key=True, max_length=80, validators=[slug_validator])
    name = models.CharField(max_length=120)
    description = models.TextField()

    class Meta:
        ordering = ["slug"]
