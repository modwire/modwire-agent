from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SirenFieldOptionsItem")


@_attrs_define
class SirenFieldOptionsItem:
    """
    Attributes:
        value (Any):
        title (str):
    """

    value: Any
    title: str

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        title = self.title

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "value": value,
                "title": title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        title = d.pop("title")

        siren_field_options_item = cls(
            value=value,
            title=title,
        )

        return siren_field_options_item
