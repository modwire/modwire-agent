from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_block import ContentBlock


T = TypeVar("T", bound="RecordPatchIn")


@_attrs_define
class RecordPatchIn:
    """
    Attributes:
        title (str | Unset):
        description (str | Unset):
        sources (list[str] | Unset):
        tag_slugs (list[str] | Unset):
        content (list[ContentBlock] | Unset):
    """

    title: str | Unset = UNSET
    description: str | Unset = UNSET
    sources: list[str] | Unset = UNSET
    tag_slugs: list[str] | Unset = UNSET
    content: list[ContentBlock] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        sources: list[str] | Unset = UNSET
        if not isinstance(self.sources, Unset):
            sources = self.sources

        tag_slugs: list[str] | Unset = UNSET
        if not isinstance(self.tag_slugs, Unset):
            tag_slugs = self.tag_slugs

        content: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item = content_item_data.to_dict()
                content.append(content_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if sources is not UNSET:
            field_dict["sources"] = sources
        if tag_slugs is not UNSET:
            field_dict["tag_slugs"] = tag_slugs
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_block import ContentBlock

        d = dict(src_dict)
        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        sources = cast(list[str], d.pop("sources", UNSET))

        tag_slugs = cast(list[str], d.pop("tag_slugs", UNSET))

        _content = d.pop("content", UNSET)
        content: list[ContentBlock] | Unset = UNSET
        if _content is not UNSET:
            content = []
            for content_item_data in _content:
                content_item = ContentBlock.from_dict(content_item_data)

                content.append(content_item)

        record_patch_in = cls(
            title=title,
            description=description,
            sources=sources,
            tag_slugs=tag_slugs,
            content=content,
        )

        return record_patch_in
