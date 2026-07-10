from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TemplatePatchInPatch")


@_attrs_define
class TemplatePatchInPatch:
    """
    Attributes:
        relative_path (None | str | Unset):
        file_content (None | str | Unset):
    """

    relative_path: None | str | Unset = UNSET
    file_content: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        relative_path: None | str | Unset
        if isinstance(self.relative_path, Unset):
            relative_path = UNSET
        else:
            relative_path = self.relative_path

        file_content: None | str | Unset
        if isinstance(self.file_content, Unset):
            file_content = UNSET
        else:
            file_content = self.file_content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if relative_path is not UNSET:
            field_dict["relative_path"] = relative_path
        if file_content is not UNSET:
            field_dict["file_content"] = file_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_relative_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        relative_path = _parse_relative_path(d.pop("relative_path", UNSET))

        def _parse_file_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_content = _parse_file_content(d.pop("file_content", UNSET))

        template_patch_in_patch = cls(
            relative_path=relative_path,
            file_content=file_content,
        )

        template_patch_in_patch.additional_properties = d
        return template_patch_in_patch

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
