from __future__ import annotations

from fastmcp import FastMCP

from logic import analyze_review

mcp = FastMCP("hotel-review-processor")


@mcp.tool(
    name="analyze_review",
    description="Analiza una reseña de hotel: idioma, sentimiento, aspectos y severidad aproximada.",
    annotations={"readOnlyHint": True},
)
def analyze_review_tool(text: str) -> dict:
    return analyze_review(text=text)


if __name__ == "__main__":
    mcp.run()