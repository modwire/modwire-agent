import base64
import uuid

from django.db import models


def short_uuid() -> str:
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("ascii").rstrip("=")


class ShortUUIDModel(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)

    class Meta:
        abstract = True
