from uuid import UUID

from modwire_hex.django import DjangoRepository

from ...domain.record.kind import RecordKind
from ...domain.section.placement import SectionPlacement
from ...domain.section.section import Section
from ...ports.section.section_store import SectionStore
from ..django.models import SectionModel, SectionPlacementModel


class DjangoSectionStore(DjangoRepository[Section, SectionModel, UUID], SectionStore):
    def key_of(self, domain: Section) -> UUID:
        return domain.identifier

    def find_record(self, key: UUID) -> SectionModel | None:
        try:
            return SectionModel.objects.get(identifier=key)
        except SectionModel.DoesNotExist:
            return None

    def create_record(self, domain: Section) -> SectionModel:
        return SectionModel(
            identifier=domain.identifier, title=domain.title, allowed_kinds=[str(kind) for kind in domain.allowed_kinds]
        )

    def update_record(self, model: SectionModel, domain: Section) -> None:
        model.title = domain.title
        model.allowed_kinds = [str(kind) for kind in domain.allowed_kinds]

    def get(self, section_id: UUID) -> Section:
        section = self.load(section_id)
        if section is None:
            raise LookupError(f"Section {section_id!r} was not found.")
        return section

    def save(self, domain: Section) -> None:
        super().save(domain)
        SectionPlacementModel.objects.filter(section_id=domain.identifier).delete()
        SectionPlacementModel.objects.bulk_create(
            SectionPlacementModel(
                section_id=domain.identifier, record_id=placement.record_id, position=placement.position
            )
            for placement in domain.placements
        )

    def to_domain(self, model: SectionModel) -> Section:
        placements = tuple(
            SectionPlacement(record_id=placement.record_id, position=placement.position)
            for placement in model.placements.all()
        )
        return Section(
            identifier=model.identifier,
            title=model.title,
            allowed_kinds=tuple(RecordKind(kind) for kind in model.allowed_kinds),
            placements=placements,
        )
