from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.content_role import ContentRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_metadata import ContentMetadata


T = TypeVar("T", bound="ContentPatchIn")


@_attrs_define
class ContentPatchIn:
    """
    Attributes:
        position (int | Unset):
        role (ContentRole | Unset):
        content (list[str] | str | Unset): An array of plain strings for lists; a string for every other role. The
            persisted result is checked against its effective role.
        language (str | Unset): Natural language for prose and lists; syntax identifier for snippets.
        metadata (ContentMetadata | Unset): Supported provenance, accessibility, and presentation metadata.
    """

    position: int | Unset = UNSET
    role: ContentRole | Unset = UNSET
    content: list[str] | str | Unset = UNSET
    language: str | Unset = UNSET
    metadata: ContentMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        position = self.position

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        content: list[str] | str | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, list):
            content = self.content

        else:
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
        from ..models.content_metadata import ContentMetadata

        d = dict(src_dict)
        position = d.pop("position", UNSET)

        _role = d.pop("role", UNSET)
        role: ContentRole | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = ContentRole(_role)

        def _parse_content(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_1 = cast(list[str], data)

                return content_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        content = _parse_content(d.pop("content", UNSET))

        language = d.pop("language", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ContentMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ContentMetadata.from_dict(_metadata)

        content_patch_in = cls(
            position=position,
            role=role,
            content=content,
            language=language,
            metadata=metadata,
        )

        return content_patch_in
