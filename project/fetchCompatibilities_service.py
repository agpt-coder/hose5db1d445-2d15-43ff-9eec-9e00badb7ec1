import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetCompatibilitiesRequest(BaseModel):
    """
    This model represents the request for fetching all hose compatibilities from the database. There are no input parameters required for this endpoint.
    """

    pass


class HoseCompatibility(BaseModel):
    """
    The HoseCompatibility type representing individual compatibility rules between hoses and attachments. It includes necessary details such as identity, related user, hose, and compatibility status.
    """

    id: str
    hoseId: str
    userId: str
    compatible: bool
    checkedAt: datetime  # TODO(autogpt): Module cannot be used as a type. reportGeneralTypeIssues
    attachment: str


class GetCompatibilitiesResponse(BaseModel):
    """
    This model represents the response containing the list of all hose compatibilities. It includes detailed information about each compatibility entry.
    """

    compatibilities: List[HoseCompatibility]


async def fetchCompatibilities(
    request: GetCompatibilitiesRequest,
) -> GetCompatibilitiesResponse:
    """
    Retrieves all compatibility entries from the database. It queries the Database Module for a list of all existing compatibility rules.
    The response includes an array of compatibility data.

    Args:
        request (GetCompatibilitiesRequest): This model represents the request for fetching all hose compatibilities from the database.
        There are no input parameters required for this endpoint.

    Returns:
        GetCompatibilitiesResponse: This model represents the response containing the list of all hose compatibilities.
        It includes detailed information about each compatibility entry.
    """
    compatibilities_records = await prisma.models.HoseCompatibility.prisma().find_many()
    compatibilities = [
        HoseCompatibility(
            id=record.id,
            hoseId=record.hose_id,
            userId=record.user_id,
            compatible=record.compatible,
            checkedAt=record.checked_at,
            attachment=record.attachment,
        )
        for record in compatibilities_records
    ]  # TODO(autogpt): Cannot access member "hose_id" for type "HoseCompatibility"
    #     Member "hose_id" is unknown. reportAttributeAccessIssue
    return GetCompatibilitiesResponse(compatibilities=compatibilities)
