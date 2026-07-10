from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.problem import Problem
from ...models.scaffolding_preview_in import ScaffoldingPreviewIn
from ...models.siren_entity import SirenEntity
from typing import cast



def _get_kwargs(
    scaffolding_id: str,
    *,
    body: ScaffoldingPreviewIn,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/scaffoldings/{scaffolding_id}/preview".format(scaffolding_id=quote(str(scaffolding_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Problem | SirenEntity | None:
    if response.status_code == 200:
        response_200 = SirenEntity.from_dict(response.json())



        return response_200

    if response.status_code == 422:
        response_422 = Problem.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Problem | SirenEntity]:
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
    body: ScaffoldingPreviewIn,

) -> Response[Problem | SirenEntity]:
    """ Preview a rendered scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingPreviewIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Problem | SirenEntity]
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
    body: ScaffoldingPreviewIn,

) -> Problem | SirenEntity | None:
    """ Preview a rendered scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingPreviewIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Problem | SirenEntity
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
    body: ScaffoldingPreviewIn,

) -> Response[Problem | SirenEntity]:
    """ Preview a rendered scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingPreviewIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Problem | SirenEntity]
     """


    kwargs = _get_kwargs(
        scaffolding_id=scaffolding_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    scaffolding_id: str,
    *,
    client: AuthenticatedClient,
    body: ScaffoldingPreviewIn,

) -> Problem | SirenEntity | None:
    """ Preview a rendered scaffolding.

    Args:
        scaffolding_id (str):
        body (ScaffoldingPreviewIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Problem | SirenEntity
     """


    return (await asyncio_detailed(
        scaffolding_id=scaffolding_id,
client=client,
body=body,

    )).parsed
