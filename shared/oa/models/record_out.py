from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.content_out import ContentOut





T = TypeVar("T", bound="RecordOut")



@_attrs_define
class RecordOut:
    """ 
        Attributes:
            slug (str):
            local_slug (str):
            section_slug (str):
            title (str):
            description (str):
            sources (list[str]):
            tag_slugs (list[str]):
            content (list[ContentOut]):
     """

    slug: str
    local_slug: str
    section_slug: str
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[str]
    content: list[ContentOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.content_out import ContentOut
        slug = self.slug

        local_slug = self.local_slug

        section_slug = self.section_slug

        title = self.title

        description = self.description

        sources = self.sources



        tag_slugs = self.tag_slugs



        content = []
        for content_item_data in self.content:
            content_item = content_item_data.to_dict()
            content.append(content_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "slug": slug,
            "local_slug": local_slug,
            "section_slug": section_slug,
            "title": title,
            "description": description,
            "sources": sources,
            "tag_slugs": tag_slugs,
            "content": content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_out import ContentOut
        d = dict(src_dict)
        slug = d.pop("slug")

        local_slug = d.pop("local_slug")

        section_slug = d.pop("section_slug")

        title = d.pop("title")

        description = d.pop("description")

        sources = cast(list[str], d.pop("sources"))


        tag_slugs = cast(list[str], d.pop("tag_slugs"))


        content = []
        _content = d.pop("content")
        for content_item_data in (_content):
            content_item = ContentOut.from_dict(content_item_data)



            content.append(content_item)


        record_out = cls(
            slug=slug,
            local_slug=local_slug,
            section_slug=section_slug,
            title=title,
            description=description,
            sources=sources,
            tag_slugs=tag_slugs,
            content=content,
        )


        record_out.additional_properties = d
        return record_out

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
