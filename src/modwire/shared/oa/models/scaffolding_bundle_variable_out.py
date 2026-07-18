from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scaffolding_bundle_variable_out_type import ScaffoldingBundleVariableOutType

T = TypeVar("T", bound="ScaffoldingBundleVariableOut")


@_attrs_define
class ScaffoldingBundleVariableOut:
    """
    Attributes:
        id (str):
        name (str):
        type_ (ScaffoldingBundleVariableOutType):
        description (str):
        default_value (Any):
        required (bool):
    """

    id: str
    name: str
    type_: ScaffoldingBundleVariableOutType
    description: str
    default_value: Any
    required: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        type_ = self.type_.value

        description = self.description

        default_value = self.default_value

        required = self.required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type_,
                "description": description,
                "default_value": default_value,
                "required": required,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        type_ = ScaffoldingBundleVariableOutType(d.pop("type"))

        description = d.pop("description")

        default_value = d.pop("default_value")

        required = d.pop("required")

        scaffolding_bundle_variable_out = cls(
            id=id,
            name=name,
            type_=type_,
            description=description,
            default_value=default_value,
            required=required,
        )

        scaffolding_bundle_variable_out.additional_properties = d
        return scaffolding_bundle_variable_out

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
