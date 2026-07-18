from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.convergence_plan_out import ConvergencePlanOut


T = TypeVar("T", bound="ScaffoldingConvergenceOut")


@_attrs_define
class ScaffoldingConvergenceOut:
    """
    Attributes:
        name (str):
        dry_run (bool):
        changed (bool):
        plan (ConvergencePlanOut):
    """

    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlanOut
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        dry_run = self.dry_run

        changed = self.changed

        plan = self.plan.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "dry_run": dry_run,
                "changed": changed,
                "plan": plan,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.convergence_plan_out import ConvergencePlanOut

        d = dict(src_dict)
        name = d.pop("name")

        dry_run = d.pop("dry_run")

        changed = d.pop("changed")

        plan = ConvergencePlanOut.from_dict(d.pop("plan"))

        scaffolding_convergence_out = cls(
            name=name,
            dry_run=dry_run,
            changed=changed,
            plan=plan,
        )

        scaffolding_convergence_out.additional_properties = d
        return scaffolding_convergence_out

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
