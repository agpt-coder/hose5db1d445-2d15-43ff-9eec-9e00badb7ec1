import prisma
import prisma.models
from pydantic import BaseModel


class UpdateMeasurementResponse(BaseModel):
    """
    This model details the response returned after attempting to update a measurement. It will indicate either success or failure along with an appropriate message.
    """

    success: bool
    message: str


async def updateMeasurement(
    measurementId: str, length: float, diameter: float
) -> UpdateMeasurementResponse:
    """
    Updates a specific measurement record. This endpoint allows modifications to length or diameter values of an existing record based on provided data. Database Module implements the update. Expect a success or error message in response.

    Args:
        measurementId (str): The ID of the measurement to update.
        length (float): The new length value for the hose.
        diameter (float): The new diameter value for the hose.

    Returns:
        UpdateMeasurementResponse: This model details the response returned after attempting to update a measurement. It will indicate either success or failure along with an appropriate message.
    """
    try:
        existing_measurement = await prisma.models.HoseMeasurement.prisma().find_unique(
            where={"id": measurementId}
        )
        if not existing_measurement:
            return UpdateMeasurementResponse(
                success=False, message="Measurement not found"
            )
        await prisma.models.HoseMeasurement.prisma().update(
            where={"id": measurementId},
            data={"Hose": {"update": {"length": length, "diameter": diameter}}},
        )
        return UpdateMeasurementResponse(
            success=True, message="Measurement updated successfully"
        )
    except Exception as e:
        return UpdateMeasurementResponse(
            success=False, message=f"Failed to update measurement: {str(e)}"
        )
