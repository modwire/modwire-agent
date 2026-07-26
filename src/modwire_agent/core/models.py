from django.db import models
from shortuuid.django_fields import ShortUUIDField

class ShortUUIDModel(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class DjangoRepository:
    pass