from ...ports.outbound import TagCatalog, TagSummary
from ..django.models import TagModel


class DjangoTagCatalog(TagCatalog):
    def list(self) -> list[TagSummary]:
        return [TagSummary(identifier=tag.identifier, name=tag.name) for tag in TagModel.objects.order_by("name")]
