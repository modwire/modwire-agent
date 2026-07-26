from abc import ABC, abstractmethod


class RecordsInbound(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
