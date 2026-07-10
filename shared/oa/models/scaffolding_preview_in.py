from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.template_override_in import TemplateOverrideIn
    from ..models.values import Values


T = TypeVar("T", bound="ScaffoldingPreviewIn")


@_attrs_define
class ScaffoldingPreviewIn:
    """
    Attributes:
        values (Values | Unset):
        template_overrides (list[TemplateOverrideIn] | Unset):
    """

    values: Values | Unset = UNSET
    template_overrides: list[TemplateOverrideIn] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.template_override_in import TemplateOverrideIn
        from ..models.values import Values

        values: dict[str, Any] | Unset = UNSET
        if not isinstance(self.values, Unset):
            values = self.values.to_dict()

        template_overrides: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.template_overrides, Unset):
            template_overrides = []
            for template_overrides_item_data in self.template_overrides:
                template_overrides_item = template_overrides_item_data.to_dict()
                template_overrides.append(template_overrides_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if values is not UNSET:
            field_dict["values"] = values
        if template_overrides is not UNSET:
            field_dict["template_overrides"] = template_overrides

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.template_override_in import TemplateOverrideIn
        from ..models.values import Values

        d = dict(src_dict)
        _values = d.pop("values", UNSET)
        values: Values | Unset
        if isinstance(_values, Unset):
            values = UNSET
        else:
            values = Values.from_dict(_values)

        _template_overrides = d.pop("template_overrides", UNSET)
        template_overrides: list[TemplateOverrideIn] | Unset = UNSET
        if _template_overrides is not UNSET:
            template_overrides = []
            for template_overrides_item_data in _template_overrides:
                template_overrides_item = TemplateOverrideIn.from_dict(template_overrides_item_data)

                template_overrides.append(template_overrides_item)

        scaffolding_preview_in = cls(
            values=values,
            template_overrides=template_overrides,
        )

        scaffolding_preview_in.additional_properties = d
        return scaffolding_preview_in

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
