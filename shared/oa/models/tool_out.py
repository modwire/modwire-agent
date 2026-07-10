from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.config_paths import ConfigPaths
    from ..models.roles import Roles


T = TypeVar("T", bound="ToolOut")


@_attrs_define
class ToolOut:
    """
    Attributes:
        language (str):
        name (str):
        executable (str):
        package_name (str):
        homepage_url (str):
        id (None | str | Unset):
        roles (Roles | Unset):
        stable_version (str | Unset):  Default: ''.
        config_paths (ConfigPaths | Unset):
        default_enabled (bool | Unset):  Default: True.
    """

    language: str
    name: str
    executable: str
    package_name: str
    homepage_url: str
    id: None | str | Unset = UNSET
    roles: Roles | Unset = UNSET
    stable_version: str | Unset = ""
    config_paths: ConfigPaths | Unset = UNSET
    default_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.config_paths import ConfigPaths
        from ..models.roles import Roles

        language = self.language

        name = self.name

        executable = self.executable

        package_name = self.package_name

        homepage_url = self.homepage_url

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        roles: dict[str, Any] | Unset = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles.to_dict()

        stable_version = self.stable_version

        config_paths: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config_paths, Unset):
            config_paths = self.config_paths.to_dict()

        default_enabled = self.default_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "language": language,
                "name": name,
                "executable": executable,
                "package_name": package_name,
                "homepage_url": homepage_url,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if roles is not UNSET:
            field_dict["roles"] = roles
        if stable_version is not UNSET:
            field_dict["stable_version"] = stable_version
        if config_paths is not UNSET:
            field_dict["config_paths"] = config_paths
        if default_enabled is not UNSET:
            field_dict["default_enabled"] = default_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.config_paths import ConfigPaths
        from ..models.roles import Roles

        d = dict(src_dict)
        language = d.pop("language")

        name = d.pop("name")

        executable = d.pop("executable")

        package_name = d.pop("package_name")

        homepage_url = d.pop("homepage_url")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        _roles = d.pop("roles", UNSET)
        roles: Roles | Unset
        if isinstance(_roles, Unset):
            roles = UNSET
        else:
            roles = Roles.from_dict(_roles)

        stable_version = d.pop("stable_version", UNSET)

        _config_paths = d.pop("config_paths", UNSET)
        config_paths: ConfigPaths | Unset
        if isinstance(_config_paths, Unset):
            config_paths = UNSET
        else:
            config_paths = ConfigPaths.from_dict(_config_paths)

        default_enabled = d.pop("default_enabled", UNSET)

        tool_out = cls(
            language=language,
            name=name,
            executable=executable,
            package_name=package_name,
            homepage_url=homepage_url,
            id=id,
            roles=roles,
            stable_version=stable_version,
            config_paths=config_paths,
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
