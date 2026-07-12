from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.scaffolding_bundle_template_out import ScaffoldingBundleTemplateOut
    from ..models.scaffolding_bundle_variable_out import ScaffoldingBundleVariableOut


T = TypeVar("T", bound="ScaffoldingBundleOut")


@_attrs_define
class ScaffoldingBundleOut:
    """
    Attributes:
        id (str):
        name (str):
        variables (list[ScaffoldingBundleVariableOut]):
        templates (list[ScaffoldingBundleTemplateOut]):
    """

    id: str
    name: str
    variables: list[ScaffoldingBundleVariableOut]
    templates: list[ScaffoldingBundleTemplateOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        variables = []
        for variables_item_data in self.variables:
            variables_item = variables_item_data.to_dict()
            variables.append(variables_item)

        templates = []
        for templates_item_data in self.templates:
            templates_item = templates_item_data.to_dict()
            templates.append(templates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "variables": variables,
                "templates": templates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scaffolding_bundle_template_out import ScaffoldingBundleTemplateOut
        from ..models.scaffolding_bundle_variable_out import ScaffoldingBundleVariableOut

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        variables = []
        _variables = d.pop("variables")
        for variables_item_data in _variables:
            variables_item = ScaffoldingBundleVariableOut.from_dict(variables_item_data)

            variables.append(variables_item)

        templates = []
        _templates = d.pop("templates")
        for templates_item_data in _templates:
            templates_item = ScaffoldingBundleTemplateOut.from_dict(templates_item_data)

            templates.append(templates_item)

        scaffolding_bundle_out = cls(
            id=id,
            name=name,
            variables=variables,
            templates=templates,
        )

        scaffolding_bundle_out.additional_properties = d
        return scaffolding_bundle_out

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
