from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="SectionIn")


@_attrs_define
class SectionIn:
    """
    Attributes:
        title (str):
        description (str):
        tag_slugs (list[str]):
    """

    title: str
    description: str
    tag_slugs: list[str]

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        tag_slugs = self.tag_slugs

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "title": title,
                "description": description,
                "tag_slugs": tag_slugs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        description = d.pop("description")

        tag_slugs = cast(list[str], d.pop("tag_slugs"))

        section_in = cls(
            title=title,
            description=description,
            tag_slugs=tag_slugs,
        )

        return section_in
