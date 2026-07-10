from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.siren_entity import SirenEntity
from typing import cast



def _get_kwargs(
    template_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/templates/{template_id}".format(template_id=quote(str(template_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SirenEntity | None:
    if response.status_code == 200:
        response_200 = SirenEntity.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SirenEntity]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[SirenEntity]:
    """ Get template.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SirenEntity]
     """


    kwargs = _get_kwargs(
        template_id=template_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> SirenEntity | None:
    """ Get template.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SirenEntity
     """


    return sync_detailed(
        template_id=template_id,
client=client,

    ).parsed

async def asyncio_detailed(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[SirenEntity]:
    """ Get template.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SirenEntity]
     """


    kwargs = _get_kwargs(
        template_id=template_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> SirenEntity | None:
    """ Get template.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SirenEntity
     """


    return (await asyncio_detailed(
        template_id=template_id,
client=client,

    )).parsed
