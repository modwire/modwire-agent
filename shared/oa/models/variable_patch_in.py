from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.variable_type import VariableType
from ..types import UNSET, Unset






T = TypeVar("T", bound="VariablePatchIn")



@_attrs_define
class VariablePatchIn:
    """ 
        Attributes:
            name (str | Unset):
            type_ (VariableType | Unset):
            description (str | Unset):
            default_value (Any | Unset):
            required (bool | Unset):
     """

    name: str | Unset = UNSET
    type_: VariableType | Unset = UNSET
    description: str | Unset = UNSET
    default_value: Any | Unset = UNSET
    required: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        description = self.description

        default_value = self.default_value

        required = self.required


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if description is not UNSET:
            field_dict["description"] = description
        if default_value is not UNSET:
            field_dict["default_value"] = default_value
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: VariableType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = VariableType(_type_)




        description = d.pop("description", UNSET)

        default_value = d.pop("default_value", UNSET)

        required = d.pop("required", UNSET)

        variable_patch_in = cls(
            name=name,
            type_=type_,
            description=description,
            default_value=default_value,
            required=required,
        )

        return variable_patch_in

