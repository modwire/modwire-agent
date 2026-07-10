from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.default_value import DefaultValue


T = TypeVar("T", bound="VariableOut")


@_attrs_define
class VariableOut:
    """
    Attributes:
        scaffolding (str):
        name (str):
        type_ (str):
        description (str):
        id (None | str | Unset):
        default_value (DefaultValue | Unset):
        required (bool | Unset):  Default: False.
    """

    scaffolding: str
    name: str
    type_: str
    description: str
    id: None | str | Unset = UNSET
    default_value: DefaultValue | Unset = UNSET
    required: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.default_value import DefaultValue

        scaffolding = self.scaffolding

        name = self.name

        type_ = self.type_

        description = self.description

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        default_value: dict[str, Any] | Unset = UNSET
        if not isinstance(self.default_value, Unset):
            default_value = self.default_value.to_dict()

        required = self.required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scaffolding": scaffolding,
                "name": name,
                "type": type_,
                "description": description,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if default_value is not UNSET:
            field_dict["default_value"] = default_value
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.default_value import DefaultValue

        d = dict(src_dict)
        scaffolding = d.pop("scaffolding")

        name = d.pop("name")

        type_ = d.pop("type")

        description = d.pop("description")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        _default_value = d.pop("default_value", UNSET)
        default_value: DefaultValue | Unset
        if isinstance(_default_value, Unset):
            default_value = UNSET
        else:
            default_value = DefaultValue.from_dict(_default_value)

        required = d.pop("required", UNSET)

        variable_out = cls(
            scaffolding=scaffolding,
            name=name,
            type_=type_,
            description=description,
            id=id,
            default_value=default_value,
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
