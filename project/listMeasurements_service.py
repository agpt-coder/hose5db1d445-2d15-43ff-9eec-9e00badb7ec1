from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetMeasurementsRequest(BaseModel):
    """
    This model defines the input parameters, which are none for this GET endpoint. However, authentication like roles should be handled in the middleware or the layer managing the security.
    """

    pass


class HoseMeasurement(BaseModel):
    """
    Represents the detailed measurements of a hose, including linked user and hose data.
    """

    id: str
    hoseId: str
    userId: str
    measuredAt: datetime


class GetMeasurementsResponse(BaseModel):
    """
    This model defines the structure of the response which contains a list of hose measurements, detailing each measurement's properties.
    """

    measurements: List[HoseMeasurement]


async def listMeasurements(request: GetMeasurementsRequest) -> GetMeasurementsResponse:
    """
    Retrieves a list of all hose measurements. This route queries the Database Module to fetch all measurement records and displays them, typically used in reporting or dashboard features. Returns an array of measurements.

    Args:
        request (GetMeasurementsRequest): This model defines the input parameters, which are none for this GET endpoint. However, authentication like roles should be handled in the middleware or the layer managing the security.

    Returns:
        GetMeasurementsResponse: This model defines the structure of the response which contains a list of hose measurements, detailing each measurement's properties.
    """
    measurements = await prisma.models.HoseMeasurement.prisma().find_many(
        include={"Hose": True, "User": True}
    )
    hose_measurements = [
        HoseMeasurement(
            id=measurement.id,
            hoseId=measurement.hoseId,
            userId=measurement.userId,
            measuredAt=measurement.measuredAt,
        )
        for measurement in measurements
    ]
    return GetMeasurementsResponse(measurements=hose_measurements)
