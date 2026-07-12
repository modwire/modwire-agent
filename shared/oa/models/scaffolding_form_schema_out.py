from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.properties import Properties


T = TypeVar("T", bound="ScaffoldingFormSchemaOut")


@_attrs_define
class ScaffoldingFormSchemaOut:
    """
    Attributes:
        schema (Literal['https://json-schema.org/draft/2020-12/schema']):
        type_ (Literal['object']):
        properties (Properties):
        required (list[str]):
        additional_properties (bool):
    """

    schema: Literal["https://json-schema.org/draft/2020-12/schema"]
    type_: Literal["object"]
    properties: Properties
    required: list[str]
    additional_properties: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        type_ = self.type_

        properties = self.properties.to_dict()

        required = self.required

        additional_properties = self.additional_properties

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "$schema": schema,
                "type": type_,
                "properties": properties,
                "required": required,
                "additionalProperties": additional_properties,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.properties import Properties

        d = dict(src_dict)
        schema = cast(Literal["https://json-schema.org/draft/2020-12/schema"], d.pop("$schema"))
        if schema != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError(f"$schema must match const 'https://json-schema.org/draft/2020-12/schema', got '{schema}'")

        type_ = cast(Literal["object"], d.pop("type"))
        if type_ != "object":
            raise ValueError(f"type must match const 'object', got '{type_}'")

        properties = Properties.from_dict(d.pop("properties"))

        required = cast(list[str], d.pop("required"))

        additional_properties = d.pop("additionalProperties")

        scaffolding_form_schema_out = cls(
            schema=schema,
            type_=type_,
            properties=properties,
            required=required,
            additional_properties=additional_properties,
        )

        scaffolding_form_schema_out.additional_properties = d
        return scaffolding_form_schema_out

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
