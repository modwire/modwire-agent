from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.package_manager_out import PackageManagerOut
    from ..models.tool_out import ToolOut
    from ..models.version_provider_out import VersionProviderOut


T = TypeVar("T", bound="LanguageOut")


@_attrs_define
class LanguageOut:
    """
    Attributes:
        id (str):
        name (str):
        executable (str):
        source_extensions (list[str]):
        aliases (list[str]):
        package_managers (list[PackageManagerOut]):
        tools (list[ToolOut]):
        stable_version (str):
        version_provider (VersionProviderOut):
    """

    id: str
    name: str
    executable: str
    source_extensions: list[str]
    aliases: list[str]
    package_managers: list[PackageManagerOut]
    tools: list[ToolOut]
    stable_version: str
    version_provider: VersionProviderOut
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        executable = self.executable

        source_extensions = self.source_extensions

        aliases = self.aliases

        package_managers = []
        for package_managers_item_data in self.package_managers:
            package_managers_item = package_managers_item_data.to_dict()
            package_managers.append(package_managers_item)

        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()
            tools.append(tools_item)

        stable_version = self.stable_version

        version_provider = self.version_provider.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "executable": executable,
                "source_extensions": source_extensions,
                "aliases": aliases,
                "package_managers": package_managers,
                "tools": tools,
                "stable_version": stable_version,
                "version_provider": version_provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.package_manager_out import PackageManagerOut
        from ..models.tool_out import ToolOut
        from ..models.version_provider_out import VersionProviderOut

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        executable = d.pop("executable")

        source_extensions = cast(list[str], d.pop("source_extensions"))

        aliases = cast(list[str], d.pop("aliases"))

        package_managers = []
        _package_managers = d.pop("package_managers")
        for package_managers_item_data in _package_managers:
            package_managers_item = PackageManagerOut.from_dict(package_managers_item_data)

            package_managers.append(package_managers_item)

        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = ToolOut.from_dict(tools_item_data)

            tools.append(tools_item)

        stable_version = d.pop("stable_version")

        version_provider = VersionProviderOut.from_dict(d.pop("version_provider"))

        language_out = cls(
            id=id,
            name=name,
            executable=executable,
            source_extensions=source_extensions,
            aliases=aliases,
            package_managers=package_managers,
            tools=tools,
            stable_version=stable_version,
            version_provider=version_provider,
        )

        language_out.additional_properties = d
        return language_out

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
