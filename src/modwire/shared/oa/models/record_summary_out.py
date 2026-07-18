from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RecordSummaryOut")


@_attrs_define
class RecordSummaryOut:
    """
    Attributes:
        slug (str):
        local_slug (str):
        section_slug (str):
        title (str):
        description (str):
        sources (list[str]):
        tag_slugs (list[str]):
    """

    slug: str
    local_slug: str
    section_slug: str
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        slug = self.slug

        local_slug = self.local_slug

        section_slug = self.section_slug

        title = self.title

        description = self.description

        sources = self.sources

        tag_slugs = self.tag_slugs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "slug": slug,
                "local_slug": local_slug,
                "section_slug": section_slug,
                "title": title,
                "description": description,
                "sources": sources,
                "tag_slugs": tag_slugs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        slug = d.pop("slug")

        local_slug = d.pop("local_slug")

        section_slug = d.pop("section_slug")

        title = d.pop("title")

        description = d.pop("description")

        sources = cast(list[str], d.pop("sources"))

        tag_slugs = cast(list[str], d.pop("tag_slugs"))

        record_summary_out = cls(
            slug=slug,
            local_slug=local_slug,
            section_slug=section_slug,
            title=title,
            description=description,
            sources=sources,
            tag_slugs=tag_slugs,
        )

        record_summary_out.additional_properties = d
        return record_summary_out

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
