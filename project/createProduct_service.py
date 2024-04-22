from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class CreateHoseResponse(BaseModel):
    """
    This model reports the result of a hose creation attempt, including the unique ID of the newly created hose.
    """

    success: bool
    hoseId: str
    message: str


async def createProduct(
    length: float, diameter: float, features: List[str]
) -> CreateHoseResponse:
    """
    Creates a new product entry, specifically for entering new types of hoses into the system. This includes unique length and features. Expected response includes success status with newly created product ID.

    Args:
        length (float): Specifies the length of the hose in meters.
        diameter (float): Specifies the diameter of the hose in centimeters.
        features (List[str]): A list of notable features associated with the hose.

    Returns:
        CreateHoseResponse: This model reports the result of a hose creation attempt, including the unique ID of the newly created hose.
    """
    try:
        new_hose = await prisma.models.Hose.prisma().create(
            data={
                "length": length,
                "diameter": diameter,
                "features": {"create": [{"name": feature} for feature in features]},
            }
        )
        return CreateHoseResponse(
            success=True, hoseId=new_hose.id, message="Successfully created new hose."
        )
    except Exception as e:
        return CreateHoseResponse(
            success=False, hoseId="", message=f"Failed to create new hose: {str(e)}"
        )
