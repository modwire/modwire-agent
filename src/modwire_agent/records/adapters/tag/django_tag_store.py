from uuid import UUID

from modwire_hex.django import DjangoRepository

from ...domain.tag.tag import Tag
from ...ports.outbound import TagStore
from ..django.models import TagModel


class DjangoTagStore(DjangoRepository[Tag, TagModel, UUID], TagStore):
    def has_all(self, tag_ids: list[UUID]) -> bool:
        return TagModel.objects.filter(identifier__in=tag_ids).count() == len(tag_ids)

    def key_of(self, domain: Tag) -> UUID:
        return domain.identifier

    def find_record(self, key: UUID) -> TagModel | None:
        try:
            return TagModel.objects.get(identifier=key)
        except TagModel.DoesNotExist:
            return None

    def create_record(self, domain: Tag) -> TagModel:
        return TagModel(identifier=domain.identifier, name=domain.name)

    def update_record(self, model: TagModel, domain: Tag) -> None:
        model.name = domain.name

    def to_domain(self, model: TagModel) -> Tag:
        return Tag(identifier=model.identifier, name=model.name)
