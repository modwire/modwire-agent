from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

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
            relative_path (str):
            file_content (str):
     """

    id: str
    scaffolding: str
    relative_path: str
    file_content: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        scaffolding = self.scaffolding

        relative_path = self.relative_path

        file_content = self.file_content


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "scaffolding": scaffolding,
            "relative_path": relative_path,
            "file_content": file_content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        scaffolding = d.pop("scaffolding")

        relative_path = d.pop("relative_path")

        file_content = d.pop("file_content")

        template_out = cls(
            id=id,
            scaffolding=scaffolding,
            relative_path=relative_path,
            file_content=file_content,
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
