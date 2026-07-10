from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.record_patch_in import RecordPatchIn
from ...models.siren_entity import SirenEntity
from typing import cast



def _get_kwargs(
    record_slug: str,
    *,
    body: RecordPatchIn,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/records/{record_slug}".format(record_slug=quote(str(record_slug), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    record_slug: str,
    *,
    client: AuthenticatedClient,
    body: RecordPatchIn,

) -> Response[SirenEntity]:
    """ Partially update record.

    Args:
        record_slug (str):
        body (RecordPatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SirenEntity]
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
    body: RecordPatchIn,

) -> SirenEntity | None:
    """ Partially update record.

    Args:
        record_slug (str):
        body (RecordPatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SirenEntity
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
    body: RecordPatchIn,

) -> Response[SirenEntity]:
    """ Partially update record.

    Args:
        record_slug (str):
        body (RecordPatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SirenEntity]
     """


    kwargs = _get_kwargs(
        record_slug=record_slug,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    record_slug: str,
    *,
    client: AuthenticatedClient,
    body: RecordPatchIn,

) -> SirenEntity | None:
    """ Partially update record.

    Args:
        record_slug (str):
        body (RecordPatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SirenEntity
     """


    return (await asyncio_detailed(
        record_slug=record_slug,
client=client,
body=body,

    )).parsed
