from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.record_search_result_out import RecordSearchResultOut
    from ..models.section_search_result_out import SectionSearchResultOut


T = TypeVar("T", bound="SearchOut")


@_attrs_define
class SearchOut:
    """
    Attributes:
        results (list[RecordSearchResultOut | SectionSearchResultOut]):
    """

    results: list[RecordSearchResultOut | SectionSearchResultOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.record_search_result_out import RecordSearchResultOut
        from ..models.section_search_result_out import SectionSearchResultOut

        results = []
        for results_item_data in self.results:
            results_item: dict[str, Any]
            if isinstance(results_item_data, RecordSearchResultOut):
                results_item = results_item_data.to_dict()
            else:
                results_item = results_item_data.to_dict()

            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.record_search_result_out import RecordSearchResultOut
        from ..models.section_search_result_out import SectionSearchResultOut

        d = dict(src_dict)
        results = []
        _results = d.pop("results")
        for results_item_data in _results:

            def _parse_results_item(data: object) -> RecordSearchResultOut | SectionSearchResultOut:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    results_item_type_0 = RecordSearchResultOut.from_dict(data)

                    return results_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                results_item_type_1 = SectionSearchResultOut.from_dict(data)

                return results_item_type_1

            results_item = _parse_results_item(results_item_data)

            results.append(results_item)

        search_out = cls(
            results=results,
        )

        search_out.additional_properties = d
        return search_out

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
