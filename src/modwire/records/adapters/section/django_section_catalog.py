from ...ports.section.section_catalog import SectionCatalog, SectionSummary
from ..django.models import SectionModel


class DjangoSectionCatalog(SectionCatalog):
    def list(self) -> list[SectionSummary]:
        return [
            SectionSummary(
                identifier=section.identifier, title=section.title, allowed_kinds=tuple(section.allowed_kinds)
            )
            for section in SectionModel.objects.order_by("title")
        ]
