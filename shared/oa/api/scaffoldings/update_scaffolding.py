from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.scaffolding_in import ScaffoldingIn
from ...models.scaffolding_out import ScaffoldingOut
from typing import cast


def _get_kwargs(
    scaffolding_id: str,
    *,
    body: ScaffoldingIn,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/scaffoldings/{scaffolding_id}".format(
            scaffolding_id=quote(str(scaffolding_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ScaffoldingOut | None:
    if response.status_code == 200:
        response_200 = ScaffoldingOut.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ScaffoldingOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scaffolding_id: str,
    *,
    client: AuthenticatedClient,
    body: ScaffoldingIn,
) -> Response[ScaffoldingOut]:
    """Update scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScaffoldingOut]
    """

    kwargs = _get_kwargs(
        scaffolding_id=scaffolding_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    scaffolding_id: str,
    *,
    client: AuthenticatedClient,
    body: ScaffoldingIn,
) -> ScaffoldingOut | None:
    """Update scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScaffoldingOut
    """

    return sync_detailed(
        scaffolding_id=scaffolding_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    scaffolding_id: str,
    *,
    client: AuthenticatedClient,
    body: ScaffoldingIn,
) -> Response[ScaffoldingOut]:
    """Update scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScaffoldingOut]
    """

    kwargs = _get_kwargs(
        scaffolding_id=scaffolding_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scaffolding_id: str,
    *,
    client: AuthenticatedClient,
    body: ScaffoldingIn,
) -> ScaffoldingOut | None:
    """Update scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScaffoldingOut
    """

    return (
        await asyncio_detailed(
            scaffolding_id=scaffolding_id,
            client=client,
            body=body,
        )
    ).parsed
