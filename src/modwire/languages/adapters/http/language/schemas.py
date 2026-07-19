from ninja import Schema
from pydantic import Field

from modwire.languages.domain.contracts import (
    PackageManagerCommand,
    ToolCommand,
    ToolRole,
    VersionPathItem,
    VersionProviderKind,
)


class VersionProviderOut(Schema):
    kind: VersionProviderKind
    url: str
    result_path: tuple[VersionPathItem, ...]


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
    commands: dict[PackageManagerCommand, str] = Field(title="PackageManagerCommands")


class ToolOut(Schema):
    id: str
    name: str
    roles: tuple[ToolRole, ...]
    executable: str
    package_name: str
    stable_version: str
    homepage_url: str
    config_paths: tuple[str, ...]
    default_enabled: bool
    commands: dict[ToolCommand, str] = Field(title="ToolCommands")


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
