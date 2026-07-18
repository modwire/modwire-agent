from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

from .settings import AdapterSettings


def create_server(settings: AdapterSettings) -> FastMCP:
    server = FastMCP(
        "Modwire",
        instructions="Modwire MCP adapter placeholder. API traversal will be rebuilt from a fresh contract.",
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

    @server.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> JSONResponse:
        return JSONResponse(
            {
                "version": settings.version,
                "api_url": settings.api_url,
                "api_traversal": "pending",
            }
        )

    return server


def main() -> None:
    create_server(AdapterSettings.from_environment()).run(transport="streamable-http")


if __name__ == "__main__":
    main()
