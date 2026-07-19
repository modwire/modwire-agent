from abc import ABC, abstractmethod
from typing import Any


class ScaffoldingConvergence(ABC):
    @abstractmethod
    def execute(self, request: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
