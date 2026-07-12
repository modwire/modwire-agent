from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TemplateOut")


@_attrs_define
class TemplateOut:
    """
    Attributes:
        id (str):
        scaffolding (str):
        file_content (str):
        relative_path (str):
        write_mode (str | Unset):  Default: 'managed'.
    """

    id: str
    scaffolding: str
    file_content: str
    relative_path: str
    write_mode: str | Unset = "managed"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        scaffolding = self.scaffolding

        file_content = self.file_content

        relative_path = self.relative_path

        write_mode = self.write_mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scaffolding": scaffolding,
                "file_content": file_content,
                "relative_path": relative_path,
            }
        )
        if write_mode is not UNSET:
            field_dict["write_mode"] = write_mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        scaffolding = d.pop("scaffolding")

        file_content = d.pop("file_content")

        relative_path = d.pop("relative_path")

        write_mode = d.pop("write_mode", UNSET)

        template_out = cls(
            id=id,
            scaffolding=scaffolding,
            file_content=file_content,
            relative_path=relative_path,
            write_mode=write_mode,
        )

        template_out.additional_properties = d
        return template_out

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
