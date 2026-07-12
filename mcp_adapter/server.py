from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import JsonValue
from starlette.requests import Request
from starlette.responses import JSONResponse

from .scaffoldings import (
    CreatedVariable,
    ScaffoldingBundle,
    ScaffoldingCapabilities,
    ScaffoldingCreate,
    ScaffoldingId,
    ScaffoldingPreview,
    ScaffoldingSchema,
    ScaffoldingsResult,
    ScaffoldingSummary,
    ScaffoldingUpdate,
    TemplateCreate,
    TemplateOverride,
    TemplateUpdate,
    UpdatedTemplate,
    VariableCreate,
)
from .settings import AdapterSettings
from .siren import AdapterError


def create_server(settings: AdapterSettings) -> FastMCP:
    capabilities = ScaffoldingCapabilities(settings.api_url, settings.api_key())
    server = FastMCP(
        "Modwire Scaffolding",
        instructions="Discover, preview, and maintain repository scaffoldings through the Modwire Siren API.",
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
    async def list_scaffoldings() -> ScaffoldingsResult:
        """List scaffoldings advertised by the scaffolding API."""
        return await _call(capabilities.list_scaffoldings())

    @server.tool()
    async def get_scaffolding_schema(scaffolding_id: ScaffoldingId) -> ScaffoldingSchema:
        """Get the variable JSON Schema advertised for a scaffolding."""
        return await _call(capabilities.schema(scaffolding_id))

    @server.tool()
    async def get_scaffolding_bundle(scaffolding_id: ScaffoldingId) -> ScaffoldingBundle:
        """Get variables and templates advertised for a local generator."""
        return await _call(capabilities.bundle(scaffolding_id))

    @server.tool()
    async def preview_scaffolding(
        scaffolding_id: ScaffoldingId,
        values: dict[str, JsonValue],
        template_overrides: tuple[TemplateOverride, ...] = (),
    ) -> ScaffoldingPreview:
        """Render a non-mutating scaffolding preview through the API."""
        return await _call(capabilities.preview(scaffolding_id, values, list(template_overrides)))

    @server.tool()
    async def update_scaffolding(
        scaffolding_id: ScaffoldingId,
        name: str,
        description: str,
    ) -> ScaffoldingSummary:
        """Replace a scaffolding's name and description through its advertised action."""
        return await _call(
            capabilities.update(
                scaffolding_id,
                ScaffoldingUpdate(name=name, description=description),
            )
        )

    @server.tool()
    async def update_scaffolding_template(update: TemplateUpdate) -> UpdatedTemplate:
        """Replace one advertised template and its convergence policy."""
        return await _call(capabilities.update_template(update))

    @server.tool()
    async def create_scaffolding(
        language_id: ScaffoldingId,
        name: str,
        description: str,
    ) -> ScaffoldingSummary:
        """Create a scaffolding through the collection's advertised action."""
        return await _call(
            capabilities.create(
                ScaffoldingCreate(
                    language_id=language_id,
                    name=name,
                    description=description,
                )
            )
        )

    @server.tool()
    async def create_scaffolding_variable(variable: VariableCreate) -> CreatedVariable:
        """Create a typed variable for a scaffolding through its advertised collection."""
        return await _call(capabilities.create_variable(variable))

    @server.tool()
    async def create_scaffolding_template(template: TemplateCreate) -> UpdatedTemplate:
        """Create a template and convergence policy through its advertised collection."""
        return await _call(capabilities.create_template(template))

    @server.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> JSONResponse:
        try:
            advertised = await capabilities.advertised_capabilities()
        except AdapterError as error:
            return JSONResponse(
                {
                    "version": settings.version,
                    "api_reachable": False,
                    "advertised_capabilities": [],
                    "error": error.payload,
                },
                status_code=503,
            )
        return JSONResponse(
            {
                "version": settings.version,
                "api_reachable": True,
                "advertised_capabilities": advertised,
            }
        )

    return server


async def _call(awaitable):
    try:
        return await awaitable
    except AdapterError as error:
        raise ToolError(str(error)) from error


def main() -> None:
    create_server(AdapterSettings.from_environment()).run(transport="streamable-http")


if __name__ == "__main__":
    main()
