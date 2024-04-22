from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class MeasurementCreationResponse(BaseModel):
    """
    This model represents the response after attempting to create a measurement for a hose. It returns success or failure with an error message.
    """

    success: bool
    message: Optional[str] = None
    measurementId: Optional[str] = None


async def createMeasurement(
    hoseId: str, length: float, diameter: float, userId: str
) -> MeasurementCreationResponse:
    """
    Creates a new measurement record in the database. This route receives measurement data (length, diameter) from the User Interface Module, and stores it in the Database Module. Expect a response indicating successful creation or an error.

    Args:
    hoseId (str): Identifier for the hose which the measurements belong to.
    length (float): The measured length of the hose.
    diameter (float): The measured diameter of the hose.
    userId (str): Identifier for the user making the measurement. Validated by the system.

    Returns:
    MeasurementCreationResponse: This model represents the response after attempting to create a measurement for a hose. It returns success or failure with an error message.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": userId})
        if not user:
            return MeasurementCreationResponse(success=False, message="User not found.")
        hose = await prisma.models.Hose.prisma().find_unique(where={"id": hoseId})
        if not hose:
            return MeasurementCreationResponse(success=False, message="Hose not found.")
        new_measurement = await prisma.models.HoseMeasurement.prisma().create(
            data={
                "hose_id": hoseId,
                "user_id": userId,
                "length": length,
                "diameter": diameter,
            }
        )
        return MeasurementCreationResponse(
            success=True,
            message="Measurement created successfully.",
            measurementId=new_measurement.id,
        )
    except Exception as e:
        return MeasurementCreationResponse(
            success=False, message=f"Error creating measurement: {str(e)}"
        )
