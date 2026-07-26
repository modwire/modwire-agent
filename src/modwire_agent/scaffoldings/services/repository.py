from typing import Any

from ..models import Scaffolding


class ScaffoldingRepository[Scaffolding](DjangoRepository):
    def key_of(self, domain: Any) -> Any:
        raise NotImplementedError

    def find_record(self, key: Any) -> Any | None:
        raise NotImplementedError

    def create_record(self, domain: Any) -> Any:
        raise NotImplementedError

    def update_record(self, model: Any, domain: Any) -> None:
        raise NotImplementedError

    def to_domain(self, model: Any) -> Any:
        raise NotImplementedError

   