from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.scaffolding_convergence_variable_in_type import ScaffoldingConvergenceVariableInType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScaffoldingConvergenceVariableIn")


@_attrs_define
class ScaffoldingConvergenceVariableIn:
    """
    Attributes:
        name (str):
        type_ (ScaffoldingConvergenceVariableInType):
        description (str):
        default_value (Any):
        required (bool | Unset):  Default: False.
    """

    name: str
    type_: ScaffoldingConvergenceVariableInType
    description: str
    default_value: Any
    required: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        description = self.description

        default_value = self.default_value

        required = self.required

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
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
        name = d.pop("name")

        type_ = ScaffoldingConvergenceVariableInType(d.pop("type"))

        description = d.pop("description")

        default_value = d.pop("default_value")

        required = d.pop("required", UNSET)

        scaffolding_convergence_variable_in = cls(
            name=name,
            type_=type_,
            description=description,
            default_value=default_value,
            required=required,
        )

        return scaffolding_convergence_variable_in
