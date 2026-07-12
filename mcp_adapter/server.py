import json
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from modwire_siren import SirenClientError, SirenTransport
from starlette.requests import Request
from starlette.responses import JSONResponse

from .hypermedia import InspectRequest, ModwireHypermedia, ModwireRequest, ModwireResult
from .settings import AdapterSettings
from .transport import HttpxSirenTransport

TransportFactory = Callable[[], AbstractAsyncContextManager[SirenTransport]]


def create_server(
    settings: AdapterSettings,
    transport_factory: TransportFactory | None = None,
) -> FastMCP:
    transport_factory = transport_factory or (
        lambda: HttpxSirenTransport(settings.api_key())
    )
    hypermedia = ModwireHypermedia(settings.api_url, transport_factory)
    server = FastMCP(
        "Modwire",
        instructions=(
            "Navigate the Modwire Siren API from its root. Inspect advertised links, "
            "actions, and field schemas before executing an action."
        ),
        host=settings.host,
        port=settings.port,
        streamable_http_path="/mcp",
        json_response=True,
        stateless_http=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=["127.0.0.1:*", "localhost:*", "mcp-adapter:*"],
            allowed_origins=["http://127.0.0.1:*", "http://localhost:*"],
        ),
    )

    @server.tool()
    async def modwire(request: ModwireRequest) -> ModwireResult:
        """Inspect or execute controls advertised by the Modwire Siren API."""
        return await _call(hypermedia.handle(request))

    @server.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> JSONResponse:
        try:
            result = await hypermedia.handle(InspectRequest(kind="inspect"))
        except SirenClientError as error:
            return JSONResponse(
                {
                    "version": settings.version,
                    "api_reachable": False,
                    "error": error.as_dict(),
                },
                status_code=503,
            )
        document = result.document
        return JSONResponse(
            {
                "version": settings.version,
                "api_reachable": True,
                "root_links": len(document.get("links", [])),
                "root_actions": len(document.get("actions", [])),
            }
        )

    return server


async def _call(awaitable):
    try:
        return await awaitable
    except SirenClientError as error:
        raise ToolError(json.dumps(error.as_dict(), sort_keys=True)) from error


def main() -> None:
    create_server(AdapterSettings.from_environment()).run(transport="streamable-http")


if __name__ == "__main__":
    main()
