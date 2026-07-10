from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.content_in import ContentIn





T = TypeVar("T", bound="RecordIn")



@_attrs_define
class RecordIn:
    """ 
        Attributes:
            section_slug (str):
            title (str):
            description (str):
            sources (list[str]):
            tag_slugs (list[str]):
            content (list[ContentIn]):
     """

    section_slug: str
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[str]
    content: list[ContentIn]





    def to_dict(self) -> dict[str, Any]:
        from ..models.content_in import ContentIn
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

        field_dict.update({
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
        from ..models.content_in import ContentIn
        d = dict(src_dict)
        section_slug = d.pop("section_slug")

        title = d.pop("title")

        description = d.pop("description")

        sources = cast(list[str], d.pop("sources"))


        tag_slugs = cast(list[str], d.pop("tag_slugs"))


        content = []
        _content = d.pop("content")
        for content_item_data in (_content):
            content_item = ContentIn.from_dict(content_item_data)



            content.append(content_item)


        record_in = cls(
            section_slug=section_slug,
            title=title,
            description=description,
            sources=sources,
            tag_slugs=tag_slugs,
            content=content,
        )

        return record_in

