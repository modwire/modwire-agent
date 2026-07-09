from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_in_mode import SearchInMode
from ..models.search_in_target import SearchInTarget

T = TypeVar("T", bound="SearchIn")


@_attrs_define
class SearchIn:
    """
    Attributes:
        query (str):
        mode (SearchInMode):
        target (SearchInTarget):
        limit (int):
        offset (int):
        section_slugs (list[str]):
        tag_slugs (list[str]):
    """

    query: str
    mode: SearchInMode
    target: SearchInTarget
    limit: int
    offset: int
    section_slugs: list[str]
    tag_slugs: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        mode = self.mode.value

        target = self.target.value

        limit = self.limit

        offset = self.offset

        section_slugs = self.section_slugs

        tag_slugs = self.tag_slugs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "mode": mode,
                "target": target,
                "limit": limit,
                "offset": offset,
                "section_slugs": section_slugs,
                "tag_slugs": tag_slugs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        mode = SearchInMode(d.pop("mode"))

        target = SearchInTarget(d.pop("target"))

        limit = d.pop("limit")

        offset = d.pop("offset")

        section_slugs = cast(list[str], d.pop("section_slugs"))

        tag_slugs = cast(list[str], d.pop("tag_slugs"))

        search_in = cls(
            query=query,
            mode=mode,
            target=target,
            limit=limit,
            offset=offset,
            section_slugs=section_slugs,
            tag_slugs=tag_slugs,
        )

        search_in.additional_properties = d
        return search_in

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
