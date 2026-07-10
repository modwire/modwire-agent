from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="TemplatePatchIn")



@_attrs_define
class TemplatePatchIn:
    """ 
        Attributes:
            relative_path (str | Unset):
            file_content (str | Unset):
     """

    relative_path: str | Unset = UNSET
    file_content: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        relative_path = self.relative_path

        file_content = self.file_content


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if relative_path is not UNSET:
            field_dict["relative_path"] = relative_path
        if file_content is not UNSET:
            field_dict["file_content"] = file_content

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        relative_path = d.pop("relative_path", UNSET)

        file_content = d.pop("file_content", UNSET)

        template_patch_in = cls(
            relative_path=relative_path,
            file_content=file_content,
        )

        return template_patch_in

