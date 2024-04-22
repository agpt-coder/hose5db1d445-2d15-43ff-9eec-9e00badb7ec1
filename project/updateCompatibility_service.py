from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateCompatibilityResponse(BaseModel):
    """
    This response model outputs the updated compatibility entry, confirming the details have been modified in the database.
    """

    compatibilityId: str
    hoseId: str
    userId: str
    compatible: bool
    attachment: str
    checkedAt: datetime


async def updateCompatibility(
    compatibilityId: str,
    compatible: bool,
    attachment: str,
    checkedAt: Optional[datetime] = None,
) -> UpdateCompatibilityResponse:
    """
    Updates an existing compatibility entry based on its ID. It modifies data in the Database Module. Expected response should confirm the update and show the modified compatibility data.

    Args:
        compatibilityId (str): The unique identifier for the existing compatibility entry to be updated.
        compatible (bool): Specifies whether the hose is compatible with the attachment.
        attachment (str): Describes the attachment or fixture that compatibility is being checked against.
        checkedAt (Optional[datetime]): The timestamp when this compatibility check was last updated. This field is optional and if not provided, the current datetime will be used.

    Returns:
        UpdateCompatibilityResponse: This response model outputs the updated compatibility entry, confirming the details have been modified in the database.
    """
    if checkedAt is None:
        checkedAt = datetime.now()
    compatibility = await prisma.models.HoseCompatibility.prisma().update(
        where={"id": compatibilityId},
        data={
            "compatible": compatible,
            "attachment": attachment,
            "checkedAt": checkedAt,
        },
    )
    response = UpdateCompatibilityResponse(
        compatibilityId=compatibility.id,
        hoseId=compatibility.hoseId,
        userId=compatibility.userId,
        compatible=compatibility.compatible,
        attachment=compatibility.attachment,
        checkedAt=compatibility.checkedAt,
    )
    return response
