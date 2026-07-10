from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.content_in_role import ContentInRole
from typing import cast

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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.record_content_in_metadata import RecordContentInMetadata

        role = self.role.value

        content = self.content

        language = self.language

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        content_in.additional_properties = d
        return content_in

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
