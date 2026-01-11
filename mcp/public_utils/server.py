from fastmcp import FastMCP

mcp = FastMCP("public-hotel-policies")

@mcp.tool()
def get_service_guidelines(issues: list[str]) -> dict:
    """
    Returns general service guidelines based on reported issues.
    These guidelines are generic and applicable to hotel customer service.
    """

    guidelines = {
        "cleanliness": "Apologize sincerely and escalate the issue to housekeeping for immediate review.",
        "service": "Acknowledge the issue and ensure follow-up from hotel management.",
        "room": "Express regret and coordinate inspection with maintenance staff.",
        "noise": "Acknowledge the disturbance and explain mitigation or compensation measures.",
        "food": "Thank the guest for the feedback and review the food service offering.",
        "location": "Acknowledge the concern and provide contextual explanation if relevant."
    }

    return {
        issue: guidelines.get(
            issue,
            "Acknowledge the feedback and ensure it is reviewed internally."
        )
        for issue in issues
    }
