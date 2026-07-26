from abc import ABC, abstractmethod


class ScaffoldingsInbound(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
