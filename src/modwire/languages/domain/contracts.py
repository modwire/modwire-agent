from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator

PackageManagerCommand = Literal[
    "init",
    "install",
    "add_runtime",
    "add_development",
    "add_optional",
    "add_peer",
    "remove",
    "update",
    "lock",
    "run",
    "publish",
    "audit",
]
ToolCommand = Literal[
    "init",
    "check",
    "fix",
    "test",
    "coverage",
    "build",
    "serve",
    "audit",
    "render",
]
ToolRole = Literal[
    "build",
    "coverage",
    "development_runner",
    "diagram_renderer",
    "diagram_validator",
    "documentation",
    "formatter",
    "linter",
    "security",
    "test_runner",
    "type_checker",
]
VersionProviderKind = Literal["endoflife", "npm"]
VersionPathItem = str | int


class LanguageModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class VersionProvider(LanguageModel):
    kind: VersionProviderKind
    url: str
    result_path: tuple[VersionPathItem, ...]


class PackageManager(LanguageModel):
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
    commands: dict[PackageManagerCommand, str]


class Tool(LanguageModel):
    id: str
    name: str
    roles: tuple[ToolRole, ...]
    executable: str
    package_name: str
    stable_version: str
    homepage_url: str
    config_paths: tuple[str, ...]
    default_enabled: bool
    commands: dict[ToolCommand, str]


class Language(LanguageModel):
    id: str
    name: str
    executable: str
    source_extensions: tuple[str, ...]
    aliases: tuple[str, ...]
    package_managers: tuple[PackageManager, ...]
    tools: tuple[Tool, ...]
    stable_version: str
    version_provider: VersionProvider


class LanguageCatalog(LanguageModel):
    languages: tuple[Language, ...]

    @model_validator(mode="after")
    def validate_catalog(self):
        language_ids = [language.id for language in self.languages]
        if len(language_ids) != len(set(language_ids)):
            raise ValueError("language ids must be unique")

        for language in self.languages:
            manager_ids = [manager.id for manager in language.package_managers]
            if len(manager_ids) != len(set(manager_ids)):
                raise ValueError(f"package manager ids must be unique for {language.id}")

            tool_ids = [tool.id for tool in language.tools]
            if len(tool_ids) != len(set(tool_ids)):
                raise ValueError(f"tool ids must be unique for {language.id}")

        return self
