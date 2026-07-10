from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_role import ContentRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="ContentPatchIn")


@_attrs_define
class ContentPatchIn:
    """
    Attributes:
        position (int | Unset):
        role (ContentRole | Unset):
        content (str | Unset):
        language (str | Unset):
        metadata (Metadata | Unset):
    """

    position: int | Unset = UNSET
    role: ContentRole | Unset = UNSET
    content: str | Unset = UNSET
    language: str | Unset = UNSET
    metadata: Metadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.metadata import Metadata

        position = self.position

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        content = self.content

        language = self.language

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if position is not UNSET:
            field_dict["position"] = position
        if role is not UNSET:
            field_dict["role"] = role
        if content is not UNSET:
            field_dict["content"] = content
        if language is not UNSET:
            field_dict["language"] = language
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        position = d.pop("position", UNSET)

        _role = d.pop("role", UNSET)
        role: ContentRole | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = ContentRole(_role)

        content = d.pop("content", UNSET)

        language = d.pop("language", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Metadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        content_patch_in = cls(
            position=position,
            role=role,
            content=content,
            language=language,
            metadata=metadata,
        )

        return content_patch_in
