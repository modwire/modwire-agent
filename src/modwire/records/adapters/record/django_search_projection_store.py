from ...domain.record.record import Record
from ...ports.record.search_projection_store import SearchProjectionStore
from ..django.models import ContentRevisionModel, ContentSearchProjectionModel, RecordModel
from .django_embeddings import DeterministicEmbeddings


class DjangoSearchProjectionStore(SearchProjectionStore):
    def index(self, record: Record) -> None:
        revision = ContentRevisionModel.objects.filter(record_id=record.identifier).order_by("-schema_version").first()
        if revision is None:
            return
        model = RecordModel.objects.prefetch_related("tags").get(identifier=record.identifier)
        text = " ".join((model.title, revision.markdown, *[tag.name for tag in model.tags.all()]))
        ContentSearchProjectionModel.objects.update_or_create(record_id=record.identifier, defaults={"revision_id": revision.identifier, "embedding": DeterministicEmbeddings().embed(text), "indexed_version": revision.schema_version})
