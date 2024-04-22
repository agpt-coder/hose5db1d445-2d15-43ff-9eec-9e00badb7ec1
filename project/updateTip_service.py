from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class CareTip(BaseModel):
    """
    Model representing the care tip details.
    """

    id: str
    title: str
    content: str
    applicableProducts: List[str]


class UpdateTipResponse(BaseModel):
    """
    The response model returning the updated hose care tip details.
    """

    updatedTip: CareTip


async def updateTip(
    tipId: str, tipTitle: str, tipContent: str, applicableProducts: List[str]
) -> UpdateTipResponse:
    """
    Allows administrators to update existing care tip details identified by tipId. The function modifies the
    'CareTip' record in the database with new title, content, and applicable products and returns the updated tip object.

    Args:
        tipId (str): The unique identifier of the hose care tip to be updated.
        tipTitle (str): The new title for the tip, providing a brief overview.
        tipContent (str): Detailed description and best practices included in the care tip.
        applicableProducts (List[str]): A list of products IDs to which the tip applies, allowing for updates to product applicability.

    Returns:
        UpdateTipResponse: The response model returning the updated hose care tip details.
    """
    tip_record = await prisma.models.HoseCompatibility.prisma().find_unique(
        where={"id": tipId}
    )
    if tip_record:
        updated_record = await prisma.models.HoseCompatibility.prisma().update(
            where={"id": tipId},
            data={
                "attachment": tipTitle,
                "compatible": tipContent,
                "checkedAt": applicableProducts,
            },
        )
        updated_tip = CareTip(
            id=updated_record.id,
            title=updated_record.attachment,
            content=updated_record.compatible,
            applicableProducts=updated_record.checkedAt,
        )
        return UpdateTipResponse(updatedTip=updated_tip)
    else:
        raise ValueError(f"No HoseCompatibility found with ID '{tipId}'")
