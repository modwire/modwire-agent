import abc
from dataclasses import dataclass
from urllib.request import Request, urlopen


class LanguageVersionError(RuntimeError):
    pass


@dataclass(frozen=True)
class PackageManagerDefinition:
    name: str
    executable: str
    manifest_paths: tuple[str, ...]
    lockfile_paths: tuple[str, ...]
    registry_url: str
    package_url_type: str
    version_constraint: str
    supports_workspaces: bool
    commit_lockfiles: bool
    commands: dict[str, str]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    roles: tuple[str, ...]
    executable: str
    package_name: str
    homepage_url: str
    config_paths: tuple[str, ...]
    default_enabled: bool
    commands: dict[str, str]
    stable_version: str = ""


class LanguageDefinition(abc.ABC):
    name: str
    executable: str
    package_managers: tuple[PackageManagerDefinition, ...]
    tools: tuple[ToolDefinition, ...]

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
