from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="TemplateIn")



@_attrs_define
class TemplateIn:
    """ 
        Attributes:
            scaffolding_id (str):
            relative_path (str):
            file_content (str):
     """

    scaffolding_id: str
    relative_path: str
    file_content: str





    def to_dict(self) -> dict[str, Any]:
        scaffolding_id = self.scaffolding_id

        relative_path = self.relative_path

        file_content = self.file_content


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "scaffolding_id": scaffolding_id,
            "relative_path": relative_path,
            "file_content": file_content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scaffolding_id = d.pop("scaffolding_id")

        relative_path = d.pop("relative_path")

        file_content = d.pop("file_content")

        template_in = cls(
            scaffolding_id=scaffolding_id,
            relative_path=relative_path,
            file_content=file_content,
        )

        return template_in

