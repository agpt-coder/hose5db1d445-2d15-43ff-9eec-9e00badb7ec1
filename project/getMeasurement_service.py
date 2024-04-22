from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class MeasurementDetailsResponse(BaseModel):
    """
    Provides detailed information about a specific hose measurement, returning data that includes hose ID, user ID, and the timestamp of measurement.
    """

    measurementId: str
    hoseId: str
    userId: str
    length: float
    diameter: float
    measuredAt: datetime


async def getMeasurement(measurementId: str) -> MeasurementDetailsResponse:
    """
    Fetches specific measurement details using the measurement ID. It queries the Database Module for the record and presents the details. Useful for audits or detailed reviews. Returns a single measurement detail.

    Args:
        measurementId (str): The ID of the measurement to fetch details for. This should correspond to the 'id' field in the HoseMeasurement model.

    Returns:
        MeasurementDetailsResponse: Provides detailed information about a specific hose measurement, returning data that includes hose ID, user ID, and the timestamp of measurement.

    Example:
        measurement_id_example = "b2f5ff4743664474aeb1b3e3c2a77e83"
        measurement_details = await getMeasurement(measurement_id_example)
        print(measurement_details)
    """
    hose_measurement = await prisma.models.HoseMeasurement.prisma().find_unique(
        where={"id": measurementId}, include={"Hose": True, "User": True}
    )
    if not hose_measurement:
        raise ValueError("Measurement not found.")
    response = MeasurementDetailsResponse(
        measurementId=hose_measurement.id,
        hoseId=hose_measurement.Hose.id,
        userId=hose_measurement.User.id,
        length=hose_measurement.Hose.length,
        diameter=hose_measurement.Hose.diameter,
        measuredAt=hose_measurement.measuredAt,
    )
    return response
