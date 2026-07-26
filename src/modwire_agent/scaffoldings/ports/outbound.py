from abc import ABC, abstractmethod
from typing import Any


class ScaffoldingCatalog(ABC):
    @abstractmethod
    def get(self, identifier: str) -> Any:
        raise NotImplementedError


class ScaffoldingConvergence(ABC):
    @abstractmethod
    def execute(self, request: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
