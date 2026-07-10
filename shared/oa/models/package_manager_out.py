from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.lockfile_paths import LockfilePaths
    from ..models.manifest_paths import ManifestPaths


T = TypeVar("T", bound="PackageManagerOut")


@_attrs_define
class PackageManagerOut:
    """
    Attributes:
        language (str):
        name (str):
        executable (str):
        id (None | str | Unset):
        manifest_paths (ManifestPaths | Unset):
        lockfile_paths (LockfilePaths | Unset):
        registry_url (str | Unset):  Default: ''.
        package_url_type (str | Unset):  Default: ''.
        version_constraint (str | Unset):  Default: ''.
        supports_workspaces (bool | Unset):  Default: False.
        commit_lockfiles (bool | Unset):  Default: True.
    """

    language: str
    name: str
    executable: str
    id: None | str | Unset = UNSET
    manifest_paths: ManifestPaths | Unset = UNSET
    lockfile_paths: LockfilePaths | Unset = UNSET
    registry_url: str | Unset = ""
    package_url_type: str | Unset = ""
    version_constraint: str | Unset = ""
    supports_workspaces: bool | Unset = False
    commit_lockfiles: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.lockfile_paths import LockfilePaths
        from ..models.manifest_paths import ManifestPaths

        language = self.language

        name = self.name

        executable = self.executable

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        manifest_paths: dict[str, Any] | Unset = UNSET
        if not isinstance(self.manifest_paths, Unset):
            manifest_paths = self.manifest_paths.to_dict()

        lockfile_paths: dict[str, Any] | Unset = UNSET
        if not isinstance(self.lockfile_paths, Unset):
            lockfile_paths = self.lockfile_paths.to_dict()

        registry_url = self.registry_url

        package_url_type = self.package_url_type

        version_constraint = self.version_constraint

        supports_workspaces = self.supports_workspaces

        commit_lockfiles = self.commit_lockfiles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "language": language,
                "name": name,
                "executable": executable,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if manifest_paths is not UNSET:
            field_dict["manifest_paths"] = manifest_paths
        if lockfile_paths is not UNSET:
            field_dict["lockfile_paths"] = lockfile_paths
        if registry_url is not UNSET:
            field_dict["registry_url"] = registry_url
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
        from ..models.lockfile_paths import LockfilePaths
        from ..models.manifest_paths import ManifestPaths

        d = dict(src_dict)
        language = d.pop("language")

        name = d.pop("name")

        executable = d.pop("executable")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        _manifest_paths = d.pop("manifest_paths", UNSET)
        manifest_paths: ManifestPaths | Unset
        if isinstance(_manifest_paths, Unset):
            manifest_paths = UNSET
        else:
            manifest_paths = ManifestPaths.from_dict(_manifest_paths)

        _lockfile_paths = d.pop("lockfile_paths", UNSET)
        lockfile_paths: LockfilePaths | Unset
        if isinstance(_lockfile_paths, Unset):
            lockfile_paths = UNSET
        else:
            lockfile_paths = LockfilePaths.from_dict(_lockfile_paths)

        registry_url = d.pop("registry_url", UNSET)

        package_url_type = d.pop("package_url_type", UNSET)

        version_constraint = d.pop("version_constraint", UNSET)

        supports_workspaces = d.pop("supports_workspaces", UNSET)

        commit_lockfiles = d.pop("commit_lockfiles", UNSET)

        package_manager_out = cls(
            language=language,
            name=name,
            executable=executable,
            id=id,
            manifest_paths=manifest_paths,
            lockfile_paths=lockfile_paths,
            registry_url=registry_url,
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
