from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scaffolding_convergence_template_in import ScaffoldingConvergenceTemplateIn
    from ..models.scaffolding_convergence_variable_in import ScaffoldingConvergenceVariableIn


T = TypeVar("T", bound="ScaffoldingConvergenceIn")


@_attrs_define
class ScaffoldingConvergenceIn:
    """
    Attributes:
        language_id (str):
        name (str):
        description (str):
        variables (list[ScaffoldingConvergenceVariableIn]):
        templates (list[ScaffoldingConvergenceTemplateIn]):
        dry_run (bool | Unset):  Default: True.
    """

    language_id: str
    name: str
    description: str
    variables: list[ScaffoldingConvergenceVariableIn]
    templates: list[ScaffoldingConvergenceTemplateIn]
    dry_run: bool | Unset = True

    def to_dict(self) -> dict[str, Any]:
        language_id = self.language_id

        name = self.name

        description = self.description

        variables = []
        for variables_item_data in self.variables:
            variables_item = variables_item_data.to_dict()
            variables.append(variables_item)

        templates = []
        for templates_item_data in self.templates:
            templates_item = templates_item_data.to_dict()
            templates.append(templates_item)

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "language_id": language_id,
                "name": name,
                "description": description,
                "variables": variables,
                "templates": templates,
            }
        )
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scaffolding_convergence_template_in import ScaffoldingConvergenceTemplateIn
        from ..models.scaffolding_convergence_variable_in import ScaffoldingConvergenceVariableIn

        d = dict(src_dict)
        language_id = d.pop("language_id")

        name = d.pop("name")

        description = d.pop("description")

        variables = []
        _variables = d.pop("variables")
        for variables_item_data in _variables:
            variables_item = ScaffoldingConvergenceVariableIn.from_dict(variables_item_data)

            variables.append(variables_item)

        templates = []
        _templates = d.pop("templates")
        for templates_item_data in _templates:
            templates_item = ScaffoldingConvergenceTemplateIn.from_dict(templates_item_data)

            templates.append(templates_item)

        dry_run = d.pop("dry_run", UNSET)

        scaffolding_convergence_in = cls(
            language_id=language_id,
            name=name,
            description=description,
            variables=variables,
            templates=templates,
            dry_run=dry_run,
        )

        return scaffolding_convergence_in
