from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.record_summary_out import RecordSummaryOut
from ...types import UNSET, Response


def _get_kwargs(
    *,
    limit: int,
    offset: int,
    section_slugs: list[str],
    tag: list[str],
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_section_slugs = section_slugs

    params["section_slugs"] = json_section_slugs

    json_tag = tag

    params["tag"] = json_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/records",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[RecordSummaryOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RecordSummaryOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[RecordSummaryOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int,
    offset: int,
    section_slugs: list[str],
    tag: list[str],
) -> Response[list[RecordSummaryOut]]:
    """List records.

    Args:
        limit (int):
        offset (int):
        section_slugs (list[str]):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[RecordSummaryOut]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        section_slugs=section_slugs,
        tag=tag,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int,
    offset: int,
    section_slugs: list[str],
    tag: list[str],
) -> list[RecordSummaryOut] | None:
    """List records.

    Args:
        limit (int):
        offset (int):
        section_slugs (list[str]):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[RecordSummaryOut]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        section_slugs=section_slugs,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int,
    offset: int,
    section_slugs: list[str],
    tag: list[str],
) -> Response[list[RecordSummaryOut]]:
    """List records.

    Args:
        limit (int):
        offset (int):
        section_slugs (list[str]):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[RecordSummaryOut]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        section_slugs=section_slugs,
        tag=tag,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int,
    offset: int,
    section_slugs: list[str],
    tag: list[str],
) -> list[RecordSummaryOut] | None:
    """List records.

    Args:
        limit (int):
        offset (int):
        section_slugs (list[str]):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[RecordSummaryOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            section_slugs=section_slugs,
            tag=tag,
        )
    ).parsed
