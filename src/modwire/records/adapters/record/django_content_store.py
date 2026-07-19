from uuid import UUID

from modwire_hex.django import DjangoRepository

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.actor_kind import ActorKind
from ...domain.record.content_revision import ContentRevision
from ...ports.record.content_store import ContentStore
from ..django.models import ContentRevisionModel


class DjangoContentStore(DjangoRepository[ContentRevision, ContentRevisionModel, UUID], ContentStore):
    def for_record(self, record_id: UUID) -> list[ContentRevision]:
        return [self.to_domain(model) for model in ContentRevisionModel.objects.filter(record_id=record_id).order_by("schema_version")]

    def has_revision(self, record_id: UUID) -> bool:
        return ContentRevisionModel.objects.filter(record_id=record_id).exists()

    def next_version(self, record_id: UUID) -> int:
        latest = ContentRevisionModel.objects.filter(record_id=record_id).order_by("-schema_version").values_list("schema_version", flat=True).first()
        return 1 if latest is None else latest + 1

    def key_of(self, domain: ContentRevision) -> UUID:
        return domain.identifier

    def find_record(self, key: UUID) -> ContentRevisionModel | None:
        try:
            return ContentRevisionModel.objects.get(identifier=key)
        except ContentRevisionModel.DoesNotExist:
            return None

    def create_record(self, domain: ContentRevision) -> ContentRevisionModel:
        return ContentRevisionModel(identifier=domain.identifier, record_id=domain.record_id, actor_id=domain.actor.identifier, actor_kind=domain.actor.kind, markdown=domain.markdown, schema_version=domain.schema_version)

    def update_record(self, model: ContentRevisionModel, domain: ContentRevision) -> None:
        model.markdown = domain.markdown
        model.schema_version = domain.schema_version

    def to_domain(self, model: ContentRevisionModel) -> ContentRevision:
        return ContentRevision(identifier=model.identifier, record_id=model.record_id, actor=Actor(identifier=model.actor_id, kind=ActorKind(model.actor_kind)), markdown=model.markdown, schema_version=model.schema_version)
