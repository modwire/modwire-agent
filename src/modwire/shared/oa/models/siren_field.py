from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.siren_field_options_item import SirenFieldOptionsItem
    from ..models.siren_field_schema import SirenFieldSchema


T = TypeVar("T", bound="SirenField")


@_attrs_define
class SirenField:
    """A Siren action input. Complex inputs include a self-contained JSON Schema in schema.

    Attributes:
        name (str): Request property or query parameter name.
        type_ (str): Siren field type. json identifies an array, object, or union described by schema.
        required (bool): Whether the operation requires this field.
        title (str | Unset): Human-readable field label.
        description (str | Unset): Usage and validation guidance.
        value (Any | Unset): Advertised default or current value.
        options (list[SirenFieldOptionsItem] | Unset):
        schema (SirenFieldSchema | Unset): Self-contained JSON Schema for a complex field; it contains no external
            component references.
        minimum (float | Unset):
        maximum (float | Unset):
        min_length (int | Unset):
        max_length (int | Unset):
        pattern (str | Unset):
    """

    name: str
    type_: str
    required: bool
    title: str | Unset = UNSET
    description: str | Unset = UNSET
    value: Any | Unset = UNSET
    options: list[SirenFieldOptionsItem] | Unset = UNSET
    schema: SirenFieldSchema | Unset = UNSET
    minimum: float | Unset = UNSET
    maximum: float | Unset = UNSET
    min_length: int | Unset = UNSET
    max_length: int | Unset = UNSET
    pattern: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        required = self.required

        title = self.title

        description = self.description

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

        minimum = self.minimum

        maximum = self.maximum

        min_length = self.min_length

        max_length = self.max_length

        pattern = self.pattern

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "type": type_,
                "required": required,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if value is not UNSET:
            field_dict["value"] = value
        if options is not UNSET:
            field_dict["options"] = options
        if schema is not UNSET:
            field_dict["schema"] = schema
        if minimum is not UNSET:
            field_dict["minimum"] = minimum
        if maximum is not UNSET:
            field_dict["maximum"] = maximum
        if min_length is not UNSET:
            field_dict["minLength"] = min_length
        if max_length is not UNSET:
            field_dict["maxLength"] = max_length
        if pattern is not UNSET:
            field_dict["pattern"] = pattern

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.siren_field_options_item import SirenFieldOptionsItem
        from ..models.siren_field_schema import SirenFieldSchema

        d = dict(src_dict)
        name = d.pop("name")

        type_ = d.pop("type")

        required = d.pop("required")

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

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

        minimum = d.pop("minimum", UNSET)

        maximum = d.pop("maximum", UNSET)

        min_length = d.pop("minLength", UNSET)

        max_length = d.pop("maxLength", UNSET)

        pattern = d.pop("pattern", UNSET)

        siren_field = cls(
            name=name,
            type_=type_,
            required=required,
            title=title,
            description=description,
            value=value,
            options=options,
            schema=schema,
            minimum=minimum,
            maximum=maximum,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
        )

        return siren_field
