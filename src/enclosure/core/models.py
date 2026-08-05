from typing import Any, get_args, get_origin

from django.db import models
from shortuuid.django_fields import ShortUUIDField


class ShortUUIDModel(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class DjangoRepository[Model: models.Model]:
    model: type[Model]

    def __init__(self, model: type[Model] | None = None) -> None:
        self.model = model or self._model_from_type_argument()

    def find(self, **kwargs: Any) -> Model | None:
        return self.find_all().filter(**kwargs).first()

    def find_all(self) -> models.QuerySet[Model]:
        return self.model.objects.all()

    def get(self, id: Any) -> Model:
        return self.find_all().get(pk=id)

    def save(self, **data: Any) -> Model:
        return self.model.objects.create(**data)

    def select_related(self, *fields: str) -> models.QuerySet[Model]:
        return self.find_all().select_related(*fields)

    def prefetch_related(self, *lookups: str | models.Prefetch) -> models.QuerySet[Model]:
        return self.find_all().prefetch_related(*lookups)

    def _model_from_type_argument(self) -> type[Model]:
        for base in type(self).__orig_bases__:
            if get_origin(base) is DjangoRepository:
                model = get_args(base)[0]
                if isinstance(model, type) and issubclass(model, models.Model):
                    return model

        raise TypeError("Pass a Django model to DjangoRepository or bind one as DjangoRepository[Model].")
