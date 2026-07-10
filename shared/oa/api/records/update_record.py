from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.record_in import RecordIn
from ...models.record_out import RecordOut
from ...types import UNSET, Response


def _get_kwargs(
    record_slug: str,
    *,
    body: RecordIn,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/records/{record_slug}".format(
            record_slug=quote(str(record_slug), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> RecordOut | None:
    if response.status_code == 200:
        response_200 = RecordOut.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[RecordOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    record_slug: str,
    *,
    client: AuthenticatedClient,
    body: RecordIn,
) -> Response[RecordOut]:
    """Update record.

    Args:
        record_slug (str):
        body (RecordIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RecordOut]
    """

    kwargs = _get_kwargs(
        record_slug=record_slug,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    record_slug: str,
    *,
    client: AuthenticatedClient,
    body: RecordIn,
) -> RecordOut | None:
    """Update record.

    Args:
        record_slug (str):
        body (RecordIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RecordOut
    """

    return sync_detailed(
        record_slug=record_slug,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    record_slug: str,
    *,
    client: AuthenticatedClient,
    body: RecordIn,
) -> Response[RecordOut]:
    """Update record.

    Args:
        record_slug (str):
        body (RecordIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RecordOut]
    """

    kwargs = _get_kwargs(
        record_slug=record_slug,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    record_slug: str,
    *,
    client: AuthenticatedClient,
    body: RecordIn,
) -> RecordOut | None:
    """Update record.

    Args:
        record_slug (str):
        body (RecordIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RecordOut
    """

    return (
        await asyncio_detailed(
            record_slug=record_slug,
            client=client,
            body=body,
        )
    ).parsed
