from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

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

    def to_dict(self) -> dict[str, Any]:
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

        return scaffolding_preview_in
