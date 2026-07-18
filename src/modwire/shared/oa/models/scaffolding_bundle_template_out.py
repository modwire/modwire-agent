from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.write_mode import WriteMode

T = TypeVar("T", bound="ScaffoldingBundleTemplateOut")


@_attrs_define
class ScaffoldingBundleTemplateOut:
    """
    Attributes:
        id (str):
        relative_path (str):
        file_content (str):
        write_mode (WriteMode):
    """

    id: str
    relative_path: str
    file_content: str
    write_mode: WriteMode
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        relative_path = self.relative_path

        file_content = self.file_content

        write_mode = self.write_mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "relative_path": relative_path,
                "file_content": file_content,
                "write_mode": write_mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        relative_path = d.pop("relative_path")

        file_content = d.pop("file_content")

        write_mode = WriteMode(d.pop("write_mode"))

        scaffolding_bundle_template_out = cls(
            id=id,
            relative_path=relative_path,
            file_content=file_content,
            write_mode=write_mode,
        )

        scaffolding_bundle_template_out.additional_properties = d
        return scaffolding_bundle_template_out

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
