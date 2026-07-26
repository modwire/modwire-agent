from wireup import injectable

from ...core.models import DjangoRepository
from ..models import Scaffolding


@injectable
class ScaffoldingRepository(DjangoRepository):
    model = Scaffolding

    def update(self, id: str, **data) -> Scaffolding:
        scaffolding = self.get(id)
        for field, value in data.items():
            setattr(scaffolding, field, value)
        scaffolding.save()
        return scaffolding

    def delete(self, id: str) -> None:
        self.get(id).delete()
