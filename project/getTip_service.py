from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class TipDetailsResponse(BaseModel):
    """
    Detailed information about the hose care tip, including best practices for maintenance and use.
    """

    tipTitle: str
    tipDescription: str
    recommendedPractices: List[str]


async def getTip(tipId: str) -> TipDetailsResponse:
    """
    Fetches detailed information about a specific care tip identified by tipId. This endpoint extracts the tip details from the Database Module and is accessible by standard users and administrators, ensuring guests cannot access specific care tip details.

    Args:
        tipId (str): The unique identifier for the hose care tip.

    Returns:
        TipDetailsResponse: Detailed information about the hose care tip, including best practices for maintenance and use.
    """
    usage_details = await prisma.models.UsageLog.prisma().find_unique(
        where={"id": tipId}
    )
    if usage_details is None:
        raise ValueError("No care tip detail found with the provided tipId.")
    import json

    tip_info = json.loads(usage_details.information)
    return TipDetailsResponse(
        tipTitle=tip_info["title"],
        tipDescription=tip_info["description"],
        recommendedPractices=tip_info["practices"],
    )
