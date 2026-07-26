from ...core.models import DjangoRepository
from ..models import Scaffolding


class ScaffoldingRepository(DjangoRepository):
    model = Scaffolding
