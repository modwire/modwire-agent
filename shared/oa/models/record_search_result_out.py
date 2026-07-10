from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Literal, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecordSearchResultOut")


@_attrs_define
class RecordSearchResultOut:
    """
    Attributes:
        kind (Literal['record']):
        slug (str):
        score (float):
        title (str):
        section_slug (str):
    """

    kind: Literal["record"]
    slug: str
    score: float
    title: str
    section_slug: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        slug = self.slug

        score = self.score

        title = self.title

        section_slug = self.section_slug

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "slug": slug,
                "score": score,
                "title": title,
                "section_slug": section_slug,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = cast(Literal["record"], d.pop("kind"))
        if kind != "record":
            raise ValueError(f"kind must match const 'record', got '{kind}'")

        slug = d.pop("slug")

        score = d.pop("score")

        title = d.pop("title")

        section_slug = d.pop("section_slug")

        record_search_result_out = cls(
            kind=kind,
            slug=slug,
            score=score,
            title=title,
            section_slug=section_slug,
        )

        record_search_result_out.additional_properties = d
        return record_search_result_out

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
