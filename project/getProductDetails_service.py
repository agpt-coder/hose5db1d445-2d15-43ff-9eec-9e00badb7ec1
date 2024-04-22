from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class HoseMeasurement(BaseModel):
    """
    Represents the detailed measurements of a hose, including linked user and hose data.
    """

    id: str
    hoseId: str
    userId: str
    measuredAt: datetime


class HoseCompatibility(BaseModel):
    """
    The HoseCompatibility type representing individual compatibility rules between hoses and attachments. It includes necessary details such as identity, related user, hose, and compatibility status.
    """

    id: str
    hoseId: str
    userId: str
    compatible: bool
    checkedAt: datetime
    attachment: str


class Hose(BaseModel):
    """
    Information about the hose including its measurements, compatibilities, purchase options, and usage logs.
    """

    id: str
    length: float
    diameter: float
    HoseMeasurements: List[HoseMeasurement]
    HoseCompatibilities: List[HoseCompatibility]
    PurchaseOptions: List[prisma.models.PurchaseOption]
    UsageLogs: List[prisma.models.UsageLog]


class ProductDetailsResponse(BaseModel):
    """
    Provides detailed information about a specific product, including compatibility and usage data.
    """

    product: Hose


async def getProductDetails(productId: str) -> ProductDetailsResponse:
    """
    Provides detailed information about a specific product identified by their unique product ID.
    This will aid in specific compatibility checks and feature information.

    Args:
    productId (str): The unique identifier for the product

    Returns:
    ProductDetailsResponse: Provides detailed information about a specific product, including compatibility and usage data.

    Example:
    product_details = await getProductDetails("abcd-ef01-2345-ghij")
    print(product_details.product.length)  # Outputs: 15.0
    """
    hose = await prisma.models.Hose.prisma().find_unique(
        where={"id": productId},
        include={
            "HoseMeasurements": True,
            "HoseCompatibilities": True,
            "PurchaseOptions": True,
            "prisma.models.UsageLog": True,
        },
    )
    if hose is None:
        raise ValueError(f"Product with ID {productId} not found")
    return ProductDetailsResponse(product=hose)
