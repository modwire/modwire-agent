from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.tool_role import ToolRole
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ToolOut")



@_attrs_define
class ToolOut:
    """ 
        Attributes:
            id (str):
            language (str):
            roles (list[ToolRole]):
            config_paths (list[str]):
            homepage_url (str):
            name (str):
            executable (str):
            package_name (str):
            stable_version (str | Unset):  Default: ''.
            default_enabled (bool | Unset):  Default: True.
     """

    id: str
    language: str
    roles: list[ToolRole]
    config_paths: list[str]
    homepage_url: str
    name: str
    executable: str
    package_name: str
    stable_version: str | Unset = ''
    default_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        language = self.language

        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.value
            roles.append(roles_item)



        config_paths = self.config_paths



        homepage_url = self.homepage_url

        name = self.name

        executable = self.executable

        package_name = self.package_name

        stable_version = self.stable_version

        default_enabled = self.default_enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "language": language,
            "roles": roles,
            "config_paths": config_paths,
            "homepage_url": homepage_url,
            "name": name,
            "executable": executable,
            "package_name": package_name,
        })
        if stable_version is not UNSET:
            field_dict["stable_version"] = stable_version
        if default_enabled is not UNSET:
            field_dict["default_enabled"] = default_enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        language = d.pop("language")

        roles = []
        _roles = d.pop("roles")
        for roles_item_data in (_roles):
            roles_item = ToolRole(roles_item_data)



            roles.append(roles_item)


        config_paths = cast(list[str], d.pop("config_paths"))


        homepage_url = d.pop("homepage_url")

        name = d.pop("name")

        executable = d.pop("executable")

        package_name = d.pop("package_name")

        stable_version = d.pop("stable_version", UNSET)

        default_enabled = d.pop("default_enabled", UNSET)

        tool_out = cls(
            id=id,
            language=language,
            roles=roles,
            config_paths=config_paths,
            homepage_url=homepage_url,
            name=name,
            executable=executable,
            package_name=package_name,
            stable_version=stable_version,
            default_enabled=default_enabled,
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
