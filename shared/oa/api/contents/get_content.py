from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.content_out import ContentOut
from ...types import Response


def _get_kwargs(
    content_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/contents/{content_id}".format(
            content_id=quote(str(content_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ContentOut | None:
    if response.status_code == 200:
        response_200 = ContentOut.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ContentOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    content_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[ContentOut]:
    """Get content.

    Args:
        content_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ContentOut]
    """

    kwargs = _get_kwargs(
        content_id=content_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    content_id: int,
    *,
    client: AuthenticatedClient,
) -> ContentOut | None:
    """Get content.

    Args:
        content_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ContentOut
    """

    return sync_detailed(
        content_id=content_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    content_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[ContentOut]:
    """Get content.

    Args:
        content_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ContentOut]
    """

    kwargs = _get_kwargs(
        content_id=content_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    content_id: int,
    *,
    client: AuthenticatedClient,
) -> ContentOut | None:
    """Get content.

    Args:
        content_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ContentOut
    """

    return (
        await asyncio_detailed(
            content_id=content_id,
            client=client,
        )
    ).parsed
