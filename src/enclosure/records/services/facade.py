from dataclasses import dataclass

from django.db.models import QuerySet
from wireup import injectable

from ..models import Category, Record, Tag
from .categories.service import CategoryService
from .records.service import RecordService
from .tags.service import TagService


@injectable
@dataclass(frozen=True)
class RecordsService:
    categories: CategoryService
    tags: TagService
    records: RecordService

    def create_category(self, data: dict) -> Category:
        return self.categories.create(data)

    def get_category(self, id: str) -> Category:
        return self.categories.get(id)

    def find_all_categories(self) -> QuerySet[Category]:
        return self.categories.find_all()

    def update_category(self, id: str, data: dict) -> Category:
        return self.categories.update(id, data)

    def delete_category(self, id: str) -> None:
        self.categories.delete(id)

    def create_tag(self, data: dict) -> Tag:
        return self.tags.create(data)

    def get_tag(self, id: str) -> Tag:
        return self.tags.get(id)

    def find_all_tags(self) -> QuerySet[Tag]:
        return self.tags.find_all()

    def update_tag(self, id: str, data: dict) -> Tag:
        return self.tags.update(id, data)

    def delete_tag(self, id: str) -> None:
        self.tags.delete(id)

    def create_record(self, data: dict) -> Record:
        self._validate_record(data)
        return self.records.create(data)

    def get_record(self, id: str) -> Record:
        return self.records.get(id)

    def find_all_records(self) -> QuerySet[Record]:
        return self.records.find_all()

    def search_records(self, query: str, limit: int = 10) -> list[Record]:
        return self.records.search(query, limit)

    def update_record(self, id: str, data: dict) -> Record:
        self._validate_record(data, self.records.get(id))
        return self.records.update(id, data)

    def delete_record(self, id: str) -> None:
        self.records.delete(id)

    def _validate_record(self, data: dict, existing: Record | None = None) -> None:
        category_id = data.get("category_id", existing.category_id if existing else None)
        content = data.get("content", existing.content if existing else None)
        tag_ids = data.get("tag_ids", [tag.id for tag in existing.tags.all()] if existing else None)
        self.categories.validate_content(category_id, content)
        self.tags.require_all(tag_ids)
