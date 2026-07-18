from ninja import Schema
from pydantic import Field

from modwire.shared import languages


class VersionProviderOut(Schema):
    kind: languages.VersionProviderKind
    url: str
    result_path: tuple[languages.VersionPathItem, ...]


class PackageManagerOut(Schema):
    id: str
    name: str
    executable: str
    manifest_paths: tuple[str, ...]
    lockfile_paths: tuple[str, ...]
    registry_url: str
    package_url_type: str
    version_constraint: str
    supports_workspaces: bool
    commit_lockfiles: bool
    commands: dict[languages.PackageManagerCommand, str] = Field(title="PackageManagerCommands")


class ToolOut(Schema):
    id: str
    name: str
    roles: tuple[languages.ToolRole, ...]
    executable: str
    package_name: str
    stable_version: str
    homepage_url: str
    config_paths: tuple[str, ...]
    default_enabled: bool
    commands: dict[languages.ToolCommand, str] = Field(title="ToolCommands")


class LanguageOut(Schema):
    id: str
    name: str
    executable: str
    source_extensions: tuple[str, ...]
    aliases: tuple[str, ...]
    package_managers: tuple[PackageManagerOut, ...]
    tools: tuple[ToolOut, ...]
    stable_version: str
    version_provider: VersionProviderOut
