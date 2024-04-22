import prisma
import prisma.models
from pydantic import BaseModel


class DeleteMeasurementResponse(BaseModel):
    """
    Response model indicating the result of the deletion operation.
    """

    success: bool
    message: str


async def deleteMeasurement(measurementId: str) -> DeleteMeasurementResponse:
    """
    Deletes a specific measurement from the database by ID. This is generally accessed by administrators for managing data retention or correcting errors. Database Module carries out the deletion process. Responds with success status if deletion is successful.

    Args:
        measurementId (str): The unique identifier of the measurement to be deleted.

    Returns:
        DeleteMeasurementResponse: Response model indicating the result of the deletion operation.

    Example:
        await deleteMeasurement('123e4567-e89b-12d3-a456-426614174000')
        > DeleteMeasurementResponse(success=True, message="Measurement deleted successfully.")
    """
    try:
        measurement = await prisma.models.HoseMeasurement.prisma().delete(
            where={"id": measurementId}
        )
        if measurement:
            response = DeleteMeasurementResponse(
                success=True, message="Measurement deleted successfully."
            )
        else:
            response = DeleteMeasurementResponse(
                success=False, message="Measurement not found."
            )
    except Exception as e:
        response = DeleteMeasurementResponse(success=False, message=str(e))
    return response
