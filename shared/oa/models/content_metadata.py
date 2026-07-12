from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContentMetadata")


@_attrs_define
class ContentMetadata:
    """Supported provenance, accessibility, and presentation metadata.

    Attributes:
        source (str | Unset): Name of the system that supplied the block. Default: ''.
        source_url (str | Unset): Canonical URL from which the block was collected. Default: ''.
        alt (str | Unset): Accessible alternative text for image content. Default: ''.
        title (str | Unset): Optional image title or caption. Default: ''.
        format_ (str | Unset): Source-specific content format when one is known. Default: ''.
        accepted_on (str | Unset): Owner acceptance date in ISO 8601 calendar-date form when applicable. Default: ''.
    """

    source: str | Unset = ""
    source_url: str | Unset = ""
    alt: str | Unset = ""
    title: str | Unset = ""
    format_: str | Unset = ""
    accepted_on: str | Unset = ""

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        source_url = self.source_url

        alt = self.alt

        title = self.title

        format_ = self.format_

        accepted_on = self.accepted_on

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if source_url is not UNSET:
            field_dict["source_url"] = source_url
        if alt is not UNSET:
            field_dict["alt"] = alt
        if title is not UNSET:
            field_dict["title"] = title
        if format_ is not UNSET:
            field_dict["format"] = format_
        if accepted_on is not UNSET:
            field_dict["accepted_on"] = accepted_on

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source", UNSET)

        source_url = d.pop("source_url", UNSET)

        alt = d.pop("alt", UNSET)

        title = d.pop("title", UNSET)

        format_ = d.pop("format", UNSET)

        accepted_on = d.pop("accepted_on", UNSET)

        content_metadata = cls(
            source=source,
            source_url=source_url,
            alt=alt,
            title=title,
            format_=format_,
            accepted_on=accepted_on,
        )

        return content_metadata
