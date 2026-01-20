
from __future__ import annotations

from fastmcp import FastMCP

from logic import get_service_guidelines

mcp = FastMCP("public-hotel-policies")


@mcp.tool(
    name="get_service_guidelines",
    description="Devuelve directrices de actuación para una lista de incidencias/aspectos.",
    annotations={"readOnlyHint": True},
)
def get_service_guidelines_tool(issues: list[str]) -> dict:
    return get_service_guidelines(issues=issues)


if __name__ == "__main__":
    mcp.run()
