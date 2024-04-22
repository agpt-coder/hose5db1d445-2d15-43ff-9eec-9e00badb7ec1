from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CompatibilityResponse(BaseModel):
    """
    Response model containing detailed information about the hose compatibility.
    """

    compatibilityId: str
    hoseId: str
    userId: str
    compatible: bool
    checkedAt: datetime
    attachment: str


async def getCompatibility(compatibilityId: str) -> CompatibilityResponse:
    """
    Fetches detailed information about a specific compatibility entry using its ID from the database.

    Args:
        compatibilityId (str): The unique identifier for a hose compatibility entry.

    Returns:
        CompatibilityResponse: Response model containing detailed information about the hose compatibility.

    Example:
        getCompatibility("123e4567-e89b-12d3-a456-426655440000")
        > CompatibilityResponse(compatibilityId="123e4567-e89b-12d3-a456-426655440000", hoseId="hose123", ...)
    """
    compatibility = await prisma.models.HoseCompatibility.prisma().find_unique(
        where={"id": compatibilityId}, include={"User": True, "Hose": True}
    )
    if not compatibility:
        raise ValueError("Compatibility entry not found.")
    response = CompatibilityResponse(
        compatibilityId=compatibility.id,
        hoseId=compatibility.hoseId,
        userId=compatibility.userId,
        compatible=compatibility.compatible,
        checkedAt=compatibility.checkedAt,
        attachment=compatibility.attachment,
    )
    return response
