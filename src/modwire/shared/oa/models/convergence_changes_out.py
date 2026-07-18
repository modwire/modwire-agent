from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ConvergenceChangesOut")


@_attrs_define
class ConvergenceChangesOut:
    """
    Attributes:
        create (list[str]):
        update (list[str]):
        delete (list[str]):
    """

    create: list[str]
    update: list[str]
    delete: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        create = self.create

        update = self.update

        delete = self.delete

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "create": create,
                "update": update,
                "delete": delete,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        create = cast(list[str], d.pop("create"))

        update = cast(list[str], d.pop("update"))

        delete = cast(list[str], d.pop("delete"))

        convergence_changes_out = cls(
            create=create,
            update=update,
            delete=delete,
        )

        convergence_changes_out.additional_properties = d
        return convergence_changes_out

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
