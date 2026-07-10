from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.variable_type import VariableType
from ..types import UNSET, Unset

T = TypeVar("T", bound="VariableIn")


@_attrs_define
class VariableIn:
    """
    Attributes:
        scaffolding_id (str):
        name (str):
        type_ (VariableType):
        description (str):
        default_value (Any):
        required (bool | Unset):  Default: False.
    """

    scaffolding_id: str
    name: str
    type_: VariableType
    description: str
    default_value: Any
    required: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        scaffolding_id = self.scaffolding_id

        name = self.name

        type_ = self.type_.value

        description = self.description

        default_value = self.default_value

        required = self.required

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "scaffolding_id": scaffolding_id,
                "name": name,
                "type": type_,
                "description": description,
                "default_value": default_value,
            }
        )
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scaffolding_id = d.pop("scaffolding_id")

        name = d.pop("name")

        type_ = VariableType(d.pop("type"))

        description = d.pop("description")

        default_value = d.pop("default_value")

        required = d.pop("required", UNSET)

        variable_in = cls(
            scaffolding_id=scaffolding_id,
            name=name,
            type_=type_,
            description=description,
            default_value=default_value,
            required=required,
        )

        return variable_in
