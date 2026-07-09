from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SectionSearchResultOut")


@_attrs_define
class SectionSearchResultOut:
    """
    Attributes:
        kind (Literal['section']):
        slug (str):
        score (float):
        title (str):
    """

    kind: Literal["section"]
    slug: str
    score: float
    title: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        slug = self.slug

        score = self.score

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "slug": slug,
                "score": score,
                "title": title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = cast(Literal["section"], d.pop("kind"))
        if kind != "section":
            raise ValueError(f"kind must match const 'section', got '{kind}'")

        slug = d.pop("slug")

        score = d.pop("score")

        title = d.pop("title")

        section_search_result_out = cls(
            kind=kind,
            slug=slug,
            score=score,
            title=title,
        )

        section_search_result_out.additional_properties = d
        return section_search_result_out

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
