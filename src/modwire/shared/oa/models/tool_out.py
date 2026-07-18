from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tool_out_roles_item import ToolOutRolesItem

if TYPE_CHECKING:
    from ..models.tool_commands import ToolCommands


T = TypeVar("T", bound="ToolOut")


@_attrs_define
class ToolOut:
    """
    Attributes:
        id (str):
        name (str):
        roles (list[ToolOutRolesItem]):
        executable (str):
        package_name (str):
        stable_version (str):
        homepage_url (str):
        config_paths (list[str]):
        default_enabled (bool):
        commands (ToolCommands):
    """

    id: str
    name: str
    roles: list[ToolOutRolesItem]
    executable: str
    package_name: str
    stable_version: str
    homepage_url: str
    config_paths: list[str]
    default_enabled: bool
    commands: ToolCommands
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.value
            roles.append(roles_item)

        executable = self.executable

        package_name = self.package_name

        stable_version = self.stable_version

        homepage_url = self.homepage_url

        config_paths = self.config_paths

        default_enabled = self.default_enabled

        commands = self.commands.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "roles": roles,
                "executable": executable,
                "package_name": package_name,
                "stable_version": stable_version,
                "homepage_url": homepage_url,
                "config_paths": config_paths,
                "default_enabled": default_enabled,
                "commands": commands,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_commands import ToolCommands

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = ToolOutRolesItem(roles_item_data)

            roles.append(roles_item)

        executable = d.pop("executable")

        package_name = d.pop("package_name")

        stable_version = d.pop("stable_version")

        homepage_url = d.pop("homepage_url")

        config_paths = cast(list[str], d.pop("config_paths"))

        default_enabled = d.pop("default_enabled")

        commands = ToolCommands.from_dict(d.pop("commands"))

        tool_out = cls(
            id=id,
            name=name,
            roles=roles,
            executable=executable,
            package_name=package_name,
            stable_version=stable_version,
            homepage_url=homepage_url,
            config_paths=config_paths,
            default_enabled=default_enabled,
            commands=commands,
        )

        tool_out.additional_properties = d
        return tool_out

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
