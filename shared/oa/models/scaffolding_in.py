from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScaffoldingIn")


@_attrs_define
class ScaffoldingIn:
    """
    Attributes:
        language_id (str):
        name (str):
        description (str):
    """

    language_id: str
    name: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        language_id = self.language_id

        name = self.name

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "language_id": language_id,
                "name": name,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        language_id = d.pop("language_id")

        name = d.pop("name")

        description = d.pop("description")

        scaffolding_in = cls(
            language_id=language_id,
            name=name,
            description=description,
        )

        return scaffolding_in
