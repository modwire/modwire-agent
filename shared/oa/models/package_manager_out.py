from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Literal, cast






T = TypeVar("T", bound="PackageManagerOut")



@_attrs_define
class PackageManagerOut:
    """ 
        Attributes:
            id (str):
            language (str):
            manifest_paths (list[str]):
            lockfile_paths (list[str]):
            registry_url (Literal[''] | str):
            name (str):
            executable (str):
            package_url_type (str | Unset):  Default: ''.
            version_constraint (str | Unset):  Default: ''.
            supports_workspaces (bool | Unset):  Default: False.
            commit_lockfiles (bool | Unset):  Default: True.
     """

    id: str
    language: str
    manifest_paths: list[str]
    lockfile_paths: list[str]
    registry_url: Literal[''] | str
    name: str
    executable: str
    package_url_type: str | Unset = ''
    version_constraint: str | Unset = ''
    supports_workspaces: bool | Unset = False
    commit_lockfiles: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        language = self.language

        manifest_paths = self.manifest_paths



        lockfile_paths = self.lockfile_paths



        registry_url: Literal[''] | str
        registry_url = self.registry_url

        name = self.name

        executable = self.executable

        package_url_type = self.package_url_type

        version_constraint = self.version_constraint

        supports_workspaces = self.supports_workspaces

        commit_lockfiles = self.commit_lockfiles


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "language": language,
            "manifest_paths": manifest_paths,
            "lockfile_paths": lockfile_paths,
            "registry_url": registry_url,
            "name": name,
            "executable": executable,
        })
        if package_url_type is not UNSET:
            field_dict["package_url_type"] = package_url_type
        if version_constraint is not UNSET:
            field_dict["version_constraint"] = version_constraint
        if supports_workspaces is not UNSET:
            field_dict["supports_workspaces"] = supports_workspaces
        if commit_lockfiles is not UNSET:
            field_dict["commit_lockfiles"] = commit_lockfiles

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        language = d.pop("language")

        manifest_paths = cast(list[str], d.pop("manifest_paths"))


        lockfile_paths = cast(list[str], d.pop("lockfile_paths"))


        def _parse_registry_url(data: object) -> Literal[''] | str:
            registry_url_type_0 = cast(Literal[''] , data)
            if registry_url_type_0 != '':
                raise ValueError(f"registry_url_type_0 must match const '', got '{registry_url_type_0}'")
            return registry_url_type_0
            return cast(Literal[''] | str, data)

        registry_url = _parse_registry_url(d.pop("registry_url"))


        name = d.pop("name")

        executable = d.pop("executable")

        package_url_type = d.pop("package_url_type", UNSET)

        version_constraint = d.pop("version_constraint", UNSET)

        supports_workspaces = d.pop("supports_workspaces", UNSET)

        commit_lockfiles = d.pop("commit_lockfiles", UNSET)

        package_manager_out = cls(
            id=id,
            language=language,
            manifest_paths=manifest_paths,
            lockfile_paths=lockfile_paths,
            registry_url=registry_url,
            name=name,
            executable=executable,
            package_url_type=package_url_type,
            version_constraint=version_constraint,
            supports_workspaces=supports_workspaces,
            commit_lockfiles=commit_lockfiles,
        )


        package_manager_out.additional_properties = d
        return package_manager_out

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
