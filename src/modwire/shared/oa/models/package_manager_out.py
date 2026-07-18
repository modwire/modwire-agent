from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.package_manager_commands import PackageManagerCommands


T = TypeVar("T", bound="PackageManagerOut")


@_attrs_define
class PackageManagerOut:
    """
    Attributes:
        id (str):
        name (str):
        executable (str):
        manifest_paths (list[str]):
        lockfile_paths (list[str]):
        registry_url (str):
        package_url_type (str):
        version_constraint (str):
        supports_workspaces (bool):
        commit_lockfiles (bool):
        commands (PackageManagerCommands):
    """

    id: str
    name: str
    executable: str
    manifest_paths: list[str]
    lockfile_paths: list[str]
    registry_url: str
    package_url_type: str
    version_constraint: str
    supports_workspaces: bool
    commit_lockfiles: bool
    commands: PackageManagerCommands
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        executable = self.executable

        manifest_paths = self.manifest_paths

        lockfile_paths = self.lockfile_paths

        registry_url = self.registry_url

        package_url_type = self.package_url_type

        version_constraint = self.version_constraint

        supports_workspaces = self.supports_workspaces

        commit_lockfiles = self.commit_lockfiles

        commands = self.commands.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "executable": executable,
                "manifest_paths": manifest_paths,
                "lockfile_paths": lockfile_paths,
                "registry_url": registry_url,
                "package_url_type": package_url_type,
                "version_constraint": version_constraint,
                "supports_workspaces": supports_workspaces,
                "commit_lockfiles": commit_lockfiles,
                "commands": commands,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.package_manager_commands import PackageManagerCommands

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        executable = d.pop("executable")

        manifest_paths = cast(list[str], d.pop("manifest_paths"))

        lockfile_paths = cast(list[str], d.pop("lockfile_paths"))

        registry_url = d.pop("registry_url")

        package_url_type = d.pop("package_url_type")

        version_constraint = d.pop("version_constraint")

        supports_workspaces = d.pop("supports_workspaces")

        commit_lockfiles = d.pop("commit_lockfiles")

        commands = PackageManagerCommands.from_dict(d.pop("commands"))

        package_manager_out = cls(
            id=id,
            name=name,
            executable=executable,
            manifest_paths=manifest_paths,
            lockfile_paths=lockfile_paths,
            registry_url=registry_url,
            package_url_type=package_url_type,
            version_constraint=version_constraint,
            supports_workspaces=supports_workspaces,
            commit_lockfiles=commit_lockfiles,
            commands=commands,
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
