from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.variable_form_property_out_type import VariableFormPropertyOutType
from ..types import UNSET, Unset

T = TypeVar("T", bound="VariableFormPropertyOut")


@_attrs_define
class VariableFormPropertyOut:
    """
    Attributes:
        type_ (VariableFormPropertyOutType):
        description (str):
        default (Any):
    """

    type_: VariableFormPropertyOutType
    description: str
    default: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        description = self.description

        default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "description": description,
                "default": default,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = VariableFormPropertyOutType(d.pop("type"))

        description = d.pop("description")

        default = d.pop("default")

        variable_form_property_out = cls(
            type_=type_,
            description=description,
            default=default,
        )

        variable_form_property_out.additional_properties = d
        return variable_form_property_out

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
