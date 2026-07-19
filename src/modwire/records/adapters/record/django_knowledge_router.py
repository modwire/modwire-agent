from ...domain.record.status import RecordStatus
from ...ports.record.knowledge_router import KnowledgeRouter, RoutedRecord
from ..django.models import RecordModel


class DjangoKnowledgeRouter(KnowledgeRouter):
    def route(self, tag_names: list[str]) -> list[RoutedRecord]:
        records = RecordModel.objects.filter(status=RecordStatus.PUBLISHED, tags__name__in=tag_names).prefetch_related("tags").distinct()
        return [
            RoutedRecord(identifier=record.identifier, title=record.title, matched_tag=next(tag.name for tag in record.tags.all() if tag.name in tag_names))
            for record in records
        ]
