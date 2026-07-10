from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.section_out import SectionOut
from typing import cast


def _get_kwargs(
    *,
    limit: int,
    offset: int,
    tag: list[str],
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_tag = tag

    params["tag"] = json_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/sections",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[SectionOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SectionOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[SectionOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int,
    offset: int,
    tag: list[str],
) -> Response[list[SectionOut]]:
    """List sections.

    Args:
        limit (int):
        offset (int):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[SectionOut]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        tag=tag,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int,
    offset: int,
    tag: list[str],
) -> list[SectionOut] | None:
    """List sections.

    Args:
        limit (int):
        offset (int):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[SectionOut]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int,
    offset: int,
    tag: list[str],
) -> Response[list[SectionOut]]:
    """List sections.

    Args:
        limit (int):
        offset (int):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[SectionOut]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        tag=tag,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int,
    offset: int,
    tag: list[str],
) -> list[SectionOut] | None:
    """List sections.

    Args:
        limit (int):
        offset (int):
        tag (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[SectionOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            tag=tag,
        )
    ).parsed
