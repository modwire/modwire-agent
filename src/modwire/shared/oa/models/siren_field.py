from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.siren_field_options_item import SirenFieldOptionsItem
    from ..models.siren_field_schema import SirenFieldSchema


T = TypeVar("T", bound="SirenField")


@_attrs_define
class SirenField:
    """
    Attributes:
        name (str):
        type_ (str | Unset):
        required (bool | Unset):
        title (str | Unset):
        value (Any | Unset):
        options (list[SirenFieldOptionsItem] | Unset):
        schema (SirenFieldSchema | Unset):
    """

    name: str
    type_: str | Unset = UNSET
    required: bool | Unset = UNSET
    title: str | Unset = UNSET
    value: Any | Unset = UNSET
    options: list[SirenFieldOptionsItem] | Unset = UNSET
    schema: SirenFieldSchema | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        required = self.required

        title = self.title

        value = self.value

        options: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        schema: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if required is not UNSET:
            field_dict["required"] = required
        if title is not UNSET:
            field_dict["title"] = title
        if value is not UNSET:
            field_dict["value"] = value
        if options is not UNSET:
            field_dict["options"] = options
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.siren_field_options_item import SirenFieldOptionsItem
        from ..models.siren_field_schema import SirenFieldSchema

        d = dict(src_dict)
        name = d.pop("name")

        type_ = d.pop("type", UNSET)

        required = d.pop("required", UNSET)

        title = d.pop("title", UNSET)

        value = d.pop("value", UNSET)

        _options = d.pop("options", UNSET)
        options: list[SirenFieldOptionsItem] | Unset = UNSET
        if _options is not UNSET:
            options = []
            for options_item_data in _options:
                options_item = SirenFieldOptionsItem.from_dict(options_item_data)

                options.append(options_item)

        _schema = d.pop("schema", UNSET)
        schema: SirenFieldSchema | Unset
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = SirenFieldSchema.from_dict(_schema)

        siren_field = cls(
            name=name,
            type_=type_,
            required=required,
            title=title,
            value=value,
            options=options,
            schema=schema,
        )

        siren_field.additional_properties = d
        return siren_field

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
