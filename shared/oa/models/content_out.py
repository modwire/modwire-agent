from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.content_role import ContentRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_metadata import ContentMetadata


T = TypeVar("T", bound="ContentOut")


@_attrs_define
class ContentOut:
    """
    Attributes:
        role (ContentRole):
        content (list[str] | str): An array of plain strings for lists; a string for every other role.
        language (str): Natural language for prose and lists; syntax identifier for snippets.
        id (int):
        record_slug (str):
        position (int):
        metadata (ContentMetadata | Unset): Supported provenance, accessibility, and presentation metadata.
    """

    role: ContentRole
    content: list[str] | str
    language: str
    id: int
    record_slug: str
    position: int
    metadata: ContentMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        role = self.role.value

        content: list[str] | str
        if isinstance(self.content, list):
            content = self.content

        else:
            content = self.content

        language = self.language

        id = self.id

        record_slug = self.record_slug

        position = self.position

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "role": role,
                "content": content,
                "language": language,
                "id": id,
                "record_slug": record_slug,
                "position": position,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_metadata import ContentMetadata

        d = dict(src_dict)
        role = ContentRole(d.pop("role"))

        def _parse_content(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_1 = cast(list[str], data)

                return content_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str, data)

        content = _parse_content(d.pop("content"))

        language = d.pop("language")

        id = d.pop("id")

        record_slug = d.pop("record_slug")

        position = d.pop("position")

        _metadata = d.pop("metadata", UNSET)
        metadata: ContentMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ContentMetadata.from_dict(_metadata)

        content_out = cls(
            role=role,
            content=content,
            language=language,
            id=id,
            record_slug=record_slug,
            position=position,
            metadata=metadata,
        )

        return content_out
