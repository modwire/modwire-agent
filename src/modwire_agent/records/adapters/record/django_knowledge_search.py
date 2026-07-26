from django.db import connection

from ...domain.record.status import RecordStatus
from ...ports.outbound import KnowledgeSearch, SearchResult
from ..django.models import ContentRevisionModel, ContentSearchProjectionModel, RecordModel
from .django_embeddings import DeterministicEmbeddings


class DjangoKnowledgeSearch(KnowledgeSearch):
    def semantic(self, query: str) -> list[SearchResult]:
        vector = DeterministicEmbeddings().embed(query)
        rows = ContentSearchProjectionModel.objects.select_related("record").filter(
            record__status=RecordStatus.PUBLISHED, embedding__isnull=False
        )
        if connection.vendor == "postgresql":
            from pgvector.django import CosineDistance

            rows = rows.annotate(distance=CosineDistance("embedding", vector)).order_by("distance")
            return [SearchResult(identifier=row.record_id, title=row.record.title, reason="semantic") for row in rows]
        scored = [(sum(left * right for left, right in zip(vector, row.embedding, strict=True)), row) for row in rows]
        return [
            SearchResult(identifier=row.record_id, title=row.record.title, reason="semantic")
            for _, row in sorted(scored, key=lambda item: item[0], reverse=True)
        ]

    def text(self, query: str) -> list[SearchResult]:
        if connection.vendor == "postgresql":
            from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

            rows = (
                ContentSearchProjectionModel.objects.select_related("record", "revision")
                .filter(record__status=RecordStatus.PUBLISHED)
                .annotate(rank=SearchRank(SearchVector("record__title", "revision__markdown"), SearchQuery(query)))
                .filter(rank__gt=0)
                .order_by("-rank")
            )
            return [SearchResult(identifier=row.record_id, title=row.record.title, reason="text") for row in rows]
        records = RecordModel.objects.filter(status=RecordStatus.PUBLISHED, title__icontains=query)
        revisions = ContentRevisionModel.objects.filter(
            markdown__icontains=query, record__status=RecordStatus.PUBLISHED
        ).select_related("record")
        found = {record.identifier: record for record in records}
        found.update({revision.record_id: revision.record for revision in revisions})
        return [
            SearchResult(identifier=record.identifier, title=record.title, reason="text") for record in found.values()
        ]
