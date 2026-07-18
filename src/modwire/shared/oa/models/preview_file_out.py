from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.write_mode import WriteMode

T = TypeVar("T", bound="PreviewFileOut")


@_attrs_define
class PreviewFileOut:
    """
    Attributes:
        template_id (str):
        path (str):
        source (str):
        html (str):
        language (str):
        write_mode (WriteMode):
    """

    template_id: str
    path: str
    source: str
    html: str
    language: str
    write_mode: WriteMode
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        template_id = self.template_id

        path = self.path

        source = self.source

        html = self.html

        language = self.language

        write_mode = self.write_mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "template_id": template_id,
                "path": path,
                "source": source,
                "html": html,
                "language": language,
                "write_mode": write_mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        template_id = d.pop("template_id")

        path = d.pop("path")

        source = d.pop("source")

        html = d.pop("html")

        language = d.pop("language")

        write_mode = WriteMode(d.pop("write_mode"))

        preview_file_out = cls(
            template_id=template_id,
            path=path,
            source=source,
            html=html,
            language=language,
            write_mode=write_mode,
        )

        preview_file_out.additional_properties = d
        return preview_file_out

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
