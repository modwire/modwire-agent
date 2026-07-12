from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.write_mode import WriteMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="TemplateIn")


@_attrs_define
class TemplateIn:
    """
    Attributes:
        scaffolding_id (str):
        relative_path (str):
        file_content (str):
        write_mode (WriteMode | Unset):  Default: WriteMode.MANAGED.
    """

    scaffolding_id: str
    relative_path: str
    file_content: str
    write_mode: WriteMode | Unset = WriteMode.MANAGED

    def to_dict(self) -> dict[str, Any]:
        scaffolding_id = self.scaffolding_id

        relative_path = self.relative_path

        file_content = self.file_content

        write_mode: str | Unset = UNSET
        if not isinstance(self.write_mode, Unset):
            write_mode = self.write_mode.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "scaffolding_id": scaffolding_id,
                "relative_path": relative_path,
                "file_content": file_content,
            }
        )
        if write_mode is not UNSET:
            field_dict["write_mode"] = write_mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scaffolding_id = d.pop("scaffolding_id")

        relative_path = d.pop("relative_path")

        file_content = d.pop("file_content")

        _write_mode = d.pop("write_mode", UNSET)
        write_mode: WriteMode | Unset
        if isinstance(_write_mode, Unset):
            write_mode = UNSET
        else:
            write_mode = WriteMode(_write_mode)

        template_in = cls(
            scaffolding_id=scaffolding_id,
            relative_path=relative_path,
            file_content=file_content,
            write_mode=write_mode,
        )

        return template_in
