from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.content_role import ContentRole
from typing import cast

if TYPE_CHECKING:
    from ..models.content_patch_in_metadata import ContentPatchInMetadata


T = TypeVar("T", bound="ContentPatchIn")


@_attrs_define
class ContentPatchIn:
    """
    Attributes:
        position (int):
        role (ContentRole):
        content (str):
        language (str):
        metadata (ContentPatchInMetadata):
    """

    position: int
    role: ContentRole
    content: str
    language: str
    metadata: ContentPatchInMetadata
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.content_patch_in_metadata import ContentPatchInMetadata

        position = self.position

        role = self.role.value

        content = self.content

        language = self.language

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "position": position,
                "role": role,
                "content": content,
                "language": language,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_patch_in_metadata import ContentPatchInMetadata

        d = dict(src_dict)
        position = d.pop("position")

        role = ContentRole(d.pop("role"))

        content = d.pop("content")

        language = d.pop("language")

        metadata = ContentPatchInMetadata.from_dict(d.pop("metadata"))

        content_patch_in = cls(
            position=position,
            role=role,
            content=content,
            language=language,
            metadata=metadata,
        )

        content_patch_in.additional_properties = d
        return content_patch_in

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
