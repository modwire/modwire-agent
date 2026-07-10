from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.preview_error_out_code import PreviewErrorOutCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.details import Details


T = TypeVar("T", bound="PreviewErrorOut")


@_attrs_define
class PreviewErrorOut:
    """
    Attributes:
        code (PreviewErrorOutCode):
        message (str):
        details (Details | Unset):
    """

    code: PreviewErrorOutCode
    message: str
    details: Details | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.details import Details

        code = self.code.value

        message = self.message

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.details import Details

        d = dict(src_dict)
        code = PreviewErrorOutCode(d.pop("code"))

        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: Details | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = Details.from_dict(_details)

        preview_error_out = cls(
            code=code,
            message=message,
            details=details,
        )

        preview_error_out.additional_properties = d
        return preview_error_out

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
