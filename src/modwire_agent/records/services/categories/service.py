from dataclasses import dataclass

from django.db.models import QuerySet
from wireup import injectable

from modwire_agent.shared import DomainError, JsonSchemaService

from ...errors import RecordsError
from ...models import Category
from .repository import CategoryRepository


@injectable
@dataclass(frozen=True)
class CategoryService:
    repository: CategoryRepository
    schemas: JsonSchemaService

    def create(self, data: dict) -> Category:
        return self.repository.save(**self._with_valid_schema(data))

    def get(self, id: str) -> Category:
        return self.repository.get(id)

    def find_all(self) -> QuerySet[Category]:
        return self.repository.find_all()

    def update(self, id: str, data: dict) -> Category:
        return self.repository.update(id, **self._with_valid_schema(data))

    def delete(self, id: str) -> None:
        self.repository.delete(id)

    def validate_content(self, category_id: str, content: object) -> None:
        category = self.get(category_id)
        try:
            self.schemas.load(category.content_schema).require_valid(content)
        except DomainError as error:
            raise RecordsError(str(error)) from error

    def _with_valid_schema(self, data: dict) -> dict:
        try:
            schema = self.schemas.load(data["content_schema"])
        except DomainError as error:
            raise RecordsError(str(error)) from error
        return {**data, "content_schema": schema.document}
