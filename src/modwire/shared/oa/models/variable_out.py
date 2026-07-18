from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.variable_type import VariableType
from ..types import UNSET, Unset

T = TypeVar("T", bound="VariableOut")


@_attrs_define
class VariableOut:
    """
    Attributes:
        id (str):
        scaffolding (str):
        type_ (VariableType):
        default_value (Any):
        name (str):
        description (str):
        required (bool | Unset):  Default: False.
    """

    id: str
    scaffolding: str
    type_: VariableType
    default_value: Any
    name: str
    description: str
    required: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        scaffolding = self.scaffolding

        type_ = self.type_.value

        default_value = self.default_value

        name = self.name

        description = self.description

        required = self.required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scaffolding": scaffolding,
                "type": type_,
                "default_value": default_value,
                "name": name,
                "description": description,
            }
        )
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        scaffolding = d.pop("scaffolding")

        type_ = VariableType(d.pop("type"))

        default_value = d.pop("default_value")

        name = d.pop("name")

        description = d.pop("description")

        required = d.pop("required", UNSET)

        variable_out = cls(
            id=id,
            scaffolding=scaffolding,
            type_=type_,
            default_value=default_value,
            name=name,
            description=description,
            required=required,
        )

        variable_out.additional_properties = d
        return variable_out

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
