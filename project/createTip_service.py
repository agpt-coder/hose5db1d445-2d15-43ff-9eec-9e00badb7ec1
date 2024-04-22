from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class TipResponseModel(BaseModel):
    """
    Response model for a newly created care tip, reflecting the stored data in the database after successful creation.
    """

    id: str
    description: str
    hoseTypeId: str
    additionalTips: List[str]


async def createTip(
    description: str, hoseTypeId: str, additionalTips: List[str]
) -> TipResponseModel:
    """
    This function allows administrators to create a new care tip, associates it with a specific hose type, and optionally includes additional tips, storing all details in the database.

    Note: The function checks for the existence of the hose type in the database before creation and uses it to validate the incoming hoseTypeId.

    Args:
        description (str): Detailed description of the care tip.
        hoseTypeId (str): Identifier for the hose type to which this tip is relevant. Must match an existing hose type in the database.
        additionalTips (List[str]): Optional additional tips related to the main tip.

    Returns:
        TipResponseModel: Response model for a newly created care tip, reflecting the stored data in the database after successful creation.

    Raises:
        ValueError: Raised if the specified hoseTypeId does not match any existing hose type, ensuring data integrity and valid relationships in the database.
    """
    hose = await prisma.models.Hose.prisma().find_unique(where={"id": hoseTypeId})
    if not hose:
        raise ValueError(f"No hose found with the ID {hoseTypeId}")
    new_hose = await prisma.models.Hose.prisma().update(
        where={"id": hoseTypeId},
        data={
            "extraDetails": {
                "create": {"description": description, "additionalTips": additionalTips}
            }
        },
    )
    return TipResponseModel(
        id=new_hose.id,
        description=description,
        hoseTypeId=hoseTypeId,
        additionalTips=additionalTips,
    )
