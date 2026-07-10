from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.command_result import CommandResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="CommandOut")


@_attrs_define
class CommandOut:
    """
    Attributes:
        id (str):
        package_manager (str):
        result (CommandResult):
        cmd (str):
    """

    id: str
    package_manager: str
    result: CommandResult
    cmd: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        package_manager = self.package_manager

        result = self.result.value

        cmd = self.cmd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "package_manager": package_manager,
                "result": result,
                "cmd": cmd,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        package_manager = d.pop("package_manager")

        result = CommandResult(d.pop("result"))

        cmd = d.pop("cmd")

        command_out = cls(
            id=id,
            package_manager=package_manager,
            result=result,
            cmd=cmd,
        )

        command_out.additional_properties = d
        return command_out

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
