from uuid import UUID

from ...ports.outbound import SectionDetails, SectionDetailsReader, SectionRecordDetails
from ..django.models import SectionModel


class DjangoSectionDetailsReader(SectionDetailsReader):
    def get(self, section_id: UUID) -> SectionDetails:
        try:
            section = SectionModel.objects.prefetch_related("placements__record").get(identifier=section_id)
        except SectionModel.DoesNotExist as error:
            raise LookupError(f"Section {section_id!r} was not found.") from error
        placements = sorted(section.placements.all(), key=lambda placement: placement.position)
        records = tuple(
            SectionRecordDetails(
                identifier=placement.record.identifier,
                title=placement.record.title,
                kind=placement.record.kind,
                status=placement.record.status,
            )
            for placement in placements
        )
        return SectionDetails(
            identifier=section.identifier,
            title=section.title,
            allowed_kinds=tuple(section.allowed_kinds),
            records=records,
        )
