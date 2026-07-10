import abc
from dataclasses import dataclass


class LanguageVersionError(RuntimeError):
    pass


@dataclass(frozen=True)
class PackageManagerDefinition:
    name: str
    executable: str
    commands: dict[str, str]


class LanguageDefinition(abc.ABC):
    name: str
    executable: str
    package_managers: tuple[PackageManagerDefinition, ...]

    @abc.abstractmethod
    def get_current_version(self, timeout: float = 10) -> str:
        raise NotImplementedError
