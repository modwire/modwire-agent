from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="VariableIn")


@_attrs_define
class VariableIn:
    """
    Attributes:
        scaffolding_id (str):
        name (str):
        type_ (str):
        description (str):
        default_value (Any):
        required (bool | Unset):  Default: False.
    """

    scaffolding_id: str
    name: str
    type_: str
    description: str
    default_value: Any
    required: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scaffolding_id = self.scaffolding_id

        name = self.name

        type_ = self.type_

        description = self.description

        default_value = self.default_value

        required = self.required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        type_ = d.pop("type")

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

        variable_in.additional_properties = d
        return variable_in

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
