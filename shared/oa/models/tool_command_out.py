from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.tool_command_capability import ToolCommandCapability






T = TypeVar("T", bound="ToolCommandOut")



@_attrs_define
class ToolCommandOut:
    """ 
        Attributes:
            id (str):
            tool (str):
            capability (ToolCommandCapability):
            cmd (str):
     """

    id: str
    tool: str
    capability: ToolCommandCapability
    cmd: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tool = self.tool

        capability = self.capability.value

        cmd = self.cmd


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "tool": tool,
            "capability": capability,
            "cmd": cmd,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        tool = d.pop("tool")

        capability = ToolCommandCapability(d.pop("capability"))




        cmd = d.pop("cmd")

        tool_command_out = cls(
            id=id,
            tool=tool,
            capability=capability,
            cmd=cmd,
        )


        tool_command_out.additional_properties = d
        return tool_command_out

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
