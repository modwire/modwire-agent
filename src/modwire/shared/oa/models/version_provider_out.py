from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.version_provider_out_kind import VersionProviderOutKind

T = TypeVar("T", bound="VersionProviderOut")


@_attrs_define
class VersionProviderOut:
    """
    Attributes:
        kind (VersionProviderOutKind):
        url (str):
        result_path (list[int | str]):
    """

    kind: VersionProviderOutKind
    url: str
    result_path: list[int | str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        url = self.url

        result_path = []
        for result_path_item_data in self.result_path:
            result_path_item: int | str
            result_path_item = result_path_item_data
            result_path.append(result_path_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "url": url,
                "result_path": result_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = VersionProviderOutKind(d.pop("kind"))

        url = d.pop("url")

        result_path = []
        _result_path = d.pop("result_path")
        for result_path_item_data in _result_path:

            def _parse_result_path_item(data: object) -> int | str:
                return cast(int | str, data)

            result_path_item = _parse_result_path_item(result_path_item_data)

            result_path.append(result_path_item)

        version_provider_out = cls(
            kind=kind,
            url=url,
            result_path=result_path,
        )

        version_provider_out.additional_properties = d
        return version_provider_out

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
