from dataclasses import dataclass, field
from typing import Any

from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from wireup import injectable

from ....core.models import DjangoRepository
from ...errors import RecordsError
from ...models import Category


@injectable
@dataclass
class CategoryRepository(DjangoRepository):
    model: type[Category] = field(default=Category, init=False)

    def save(self, **data: Any) -> Category:
        try:
            return super().save(**data)
        except IntegrityError as error:
            raise RecordsError("A category with this title already exists.") from error

    def update(self, id: str, **data: Any) -> Category:
        category = self.get(id)
        for attribute, value in data.items():
            setattr(category, attribute, value)
        try:
            category.save()
        except IntegrityError as error:
            raise RecordsError("A category with this title already exists.") from error
        return category

    def delete(self, id: str) -> None:
        try:
            self.get(id).delete()
        except ProtectedError as error:
            raise RecordsError("A category assigned to records cannot be deleted.") from error
