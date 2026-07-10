from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SectionPatchIn")



@_attrs_define
class SectionPatchIn:
    """ 
        Attributes:
            title (str | Unset):
            description (str | Unset):
            tag_slugs (list[str] | Unset):
     """

    title: str | Unset = UNSET
    description: str | Unset = UNSET
    tag_slugs: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        tag_slugs: list[str] | Unset = UNSET
        if not isinstance(self.tag_slugs, Unset):
            tag_slugs = self.tag_slugs




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if tag_slugs is not UNSET:
            field_dict["tag_slugs"] = tag_slugs

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        tag_slugs = cast(list[str], d.pop("tag_slugs", UNSET))


        section_patch_in = cls(
            title=title,
            description=description,
            tag_slugs=tag_slugs,
        )

        return section_patch_in

