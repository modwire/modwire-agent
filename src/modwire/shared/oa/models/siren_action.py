from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.siren_field import SirenField


T = TypeVar("T", bound="SirenAction")


@_attrs_define
class SirenAction:
    """
    Attributes:
        name (str):
        method (str):
        href (str):
        title (str | Unset):
        type_ (str | Unset):
        fields (list[SirenField] | Unset):
    """

    name: str
    method: str
    href: str
    title: str | Unset = UNSET
    type_: str | Unset = UNSET
    fields: list[SirenField] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        method = self.method

        href = self.href

        title = self.title

        type_ = self.type_

        fields: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()
                fields.append(fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "method": method,
                "href": href,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if type_ is not UNSET:
            field_dict["type"] = type_
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.siren_field import SirenField

        d = dict(src_dict)
        name = d.pop("name")

        method = d.pop("method")

        href = d.pop("href")

        title = d.pop("title", UNSET)

        type_ = d.pop("type", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: list[SirenField] | Unset = UNSET
        if _fields is not UNSET:
            fields = []
            for fields_item_data in _fields:
                fields_item = SirenField.from_dict(fields_item_data)

                fields.append(fields_item)

        siren_action = cls(
            name=name,
            method=method,
            href=href,
            title=title,
            type_=type_,
            fields=fields,
        )

        siren_action.additional_properties = d
        return siren_action

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
