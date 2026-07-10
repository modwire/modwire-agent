from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TemplateOverrideIn")


@_attrs_define
class TemplateOverrideIn:
    """
    Attributes:
        template_id (str):
        relative_path (str):
        file_content (str):
    """

    template_id: str
    relative_path: str
    file_content: str

    def to_dict(self) -> dict[str, Any]:
        template_id = self.template_id

        relative_path = self.relative_path

        file_content = self.file_content

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "template_id": template_id,
                "relative_path": relative_path,
                "file_content": file_content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        template_id = d.pop("template_id")

        relative_path = d.pop("relative_path")

        file_content = d.pop("file_content")

        template_override_in = cls(
            template_id=template_id,
            relative_path=relative_path,
            file_content=file_content,
        )

        return template_override_in
