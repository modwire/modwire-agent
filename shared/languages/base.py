import abc
from dataclasses import dataclass
from urllib.request import Request, urlopen


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

    @property
    @abc.abstractmethod
    def version_request(self) -> Request:
        raise NotImplementedError

    @abc.abstractmethod
    def on_version_response(self, response) -> str:
        raise NotImplementedError

    def get_current_version(self, timeout: float = 10) -> str:
        request = self.version_request

        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                version = self.on_version_response(response)
        except (OSError, ValueError, IndexError, KeyError, TypeError) as error:
            raise LanguageVersionError(f"Could not obtain the current {self.name} version: {error}") from error
        if not isinstance(version, str) or not version:
            raise LanguageVersionError(f"The version provider returned an invalid current {self.name} version.")
        return version
