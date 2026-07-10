from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_in_role import ContentInRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.record_content_in_metadata import RecordContentInMetadata


T = TypeVar("T", bound="ContentIn")


@_attrs_define
class ContentIn:
    """
    Attributes:
        role (ContentInRole):
        content (str):
        language (str):
        metadata (RecordContentInMetadata):
    """

    role: ContentInRole
    content: str
    language: str
    metadata: RecordContentInMetadata

    def to_dict(self) -> dict[str, Any]:
        from ..models.record_content_in_metadata import RecordContentInMetadata

        role = self.role.value

        content = self.content

        language = self.language

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "role": role,
                "content": content,
                "language": language,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.record_content_in_metadata import RecordContentInMetadata

        d = dict(src_dict)
        role = ContentInRole(d.pop("role"))

        content = d.pop("content")

        language = d.pop("language")

        metadata = RecordContentInMetadata.from_dict(d.pop("metadata"))

        content_in = cls(
            role=role,
            content=content,
            language=language,
            metadata=metadata,
        )

        return content_in
