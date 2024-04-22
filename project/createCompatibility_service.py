from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CompatibilityCreationResponse(BaseModel):
    """
    Response model representing the details of a newly created hose compatibility entry.
    """

    id: str
    hoseId: str
    compatible: bool
    attachment: str
    checkedAt: datetime


async def createCompatibility(
    hoseId: str, userId: str, compatible: bool, attachment: str
) -> CompatibilityCreationResponse:
    """
    Creates a new compatibility entry in the database. It uses the Database Module to store
    compatibility rules between hoses and attachments. Expected response should confirm the creation along
    with details of the new entry.

    Args:
        hoseId (str): The unique identifier of the hose involved in this compatibility check.
        userId (str): The unique identifier of the user creating this compatibility entry.
        compatible (bool): Boolean flag indicating if the hose is compatible with the attachment.
        attachment (str): Description or identifier of the attachment being tested for compatibility.

    Returns:
        CompatibilityCreationResponse: Response model representing the details of a newly created hose compatibility entry.
    """
    compatibility_log = await prisma.models.HoseCompatibility.prisma().create(
        data={
            "hoseId": hoseId,
            "userId": userId,
            "compatible": compatible,
            "attachment": attachment,
        }
    )
    return CompatibilityCreationResponse(
        id=compatibility_log.id,
        hoseId=compatibility_log.hoseId,
        compatible=compatibility_log.compatible,
        attachment=compatibility_log.attachment,
        checkedAt=compatibility_log.checkedAt,
    )
