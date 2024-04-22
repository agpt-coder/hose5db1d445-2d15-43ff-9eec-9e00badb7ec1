from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class PlatformInfo(BaseModel):
    """
    Encapsulates the purchasing detail for a given platform.
    """

    name: str
    price: float
    currency: str
    link: str


class GetPurchasePlatformsResponse(BaseModel):
    """
    Response model that provides a list of available e-commerce platforms with their corresponding price and purchase link for a specified product.
    """

    platforms: List[PlatformInfo]


async def getPurchasePlatforms(
    product_id: str, user_location: Optional[str]
) -> GetPurchasePlatformsResponse:
    """
    Retrieves a list of available e-commerce platforms from which a user can purchase the specified product, including price comparisons. This endpoint consumes data from external e-commerce APIs, and the response will typically include platform name, price, and direct link to the purchase page.

    Args:
        product_id (str): The unique identifier of the product for which the purchase information is requested.
        user_location (Optional[str]): The user's location to provide region-specific pricing and availability.

    Returns:
        GetPurchasePlatformsResponse: Response model that provides a list of available e-commerce platforms with their corresponding price and purchase link for a specified product.
    """
    platforms_data = await prisma.models.PurchaseOption.prisma().find_many(
        where={"hoseId": product_id, "available": True}
    )
    platform_infos = [
        PlatformInfo(
            name=platform.platform,
            price=platform.price,
            currency=platform.currency,
            link=platform.link,
        )
        for platform in platforms_data
    ]
    return GetPurchasePlatformsResponse(platforms=platform_infos)
