from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_tools_role import ListToolsRole
from ...models.tool_out import ToolOut
from ...types import UNSET, Response


def _get_kwargs(
    *,
    language_id: str,
    role: ListToolsRole,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["language_id"] = language_id

    json_role = role.value
    params["role"] = json_role

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/tools",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[ToolOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ToolOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[ToolOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    language_id: str,
    role: ListToolsRole,
) -> Response[list[ToolOut]]:
    """List tools.

    Args:
        language_id (str):
        role (ListToolsRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ToolOut]]
    """

    kwargs = _get_kwargs(
        language_id=language_id,
        role=role,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    language_id: str,
    role: ListToolsRole,
) -> list[ToolOut] | None:
    """List tools.

    Args:
        language_id (str):
        role (ListToolsRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ToolOut]
    """

    return sync_detailed(
        client=client,
        language_id=language_id,
        role=role,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    language_id: str,
    role: ListToolsRole,
) -> Response[list[ToolOut]]:
    """List tools.

    Args:
        language_id (str):
        role (ListToolsRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ToolOut]]
    """

    kwargs = _get_kwargs(
        language_id=language_id,
        role=role,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    language_id: str,
    role: ListToolsRole,
) -> list[ToolOut] | None:
    """List tools.

    Args:
        language_id (str):
        role (ListToolsRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ToolOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            language_id=language_id,
            role=role,
        )
    ).parsed
