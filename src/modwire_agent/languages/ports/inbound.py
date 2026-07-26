from abc import ABC, abstractmethod


class LanguagesInbound(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
