from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class PurchaseOptionDetail(BaseModel):
    """
    Detailed information about a purchase option.
    """

    platform: str
    price: float
    currency: str
    available: bool
    link: str


class ProductDetail(BaseModel):
    """
    Details of a single product, including associated purchase options.
    """

    id: str
    length: float
    diameter: float
    purchaseOptions: List[PurchaseOptionDetail]


class ProductsListResponse(BaseModel):
    """
    The response model providing a list of products, focusing on hoses with their purchase options.
    """

    products: List[ProductDetail]


async def listProducts(
    hose_diameter_min: Optional[float],
    hose_diameter_max: Optional[float],
    hose_length_min: Optional[float],
    hose_length_max: Optional[float],
) -> ProductsListResponse:
    """
    Retrieves a list of all products, focusing primarily on the available hoses. Useful for both users and administrators for browsing products.

    Args:
        hose_diameter_min (Optional[float]): Minimum diameter of hose to filter the products.
        hose_diameter_max (Optional[float]): Maximum diameter of hose to filter the products.
        hose_length_min (Optional[float]): Minimum length of hose to filter the products.
        hose_length_max (Optional[float]): Maximum length of hose to filter the products.

    Returns:
        ProductsListResponse: The response model providing a list of products, focusing on hoses with their purchase options.
    """
    query_conditions = {}
    if hose_diameter_min is not None:
        query_conditions["diameter"] = {"gte": hose_diameter_min}
    if hose_diameter_max is not None:
        query_conditions["diameter"] = query_conditions.get("diameter", {})
        query_conditions["diameter"]["lte"] = hose_diameter_max
    if hose_length_min is not None:
        query_conditions["length"] = {"gte": hose_length_min}
    if hose_length_max is not None:
        query_conditions["length"] = query_conditions.get("length", {})
        query_conditions["length"]["lte"] = hose_length_max
    hoses = await prisma.models.Hose.prisma().find_many(
        where=query_conditions, include={"PurchaseOptions": True}
    )
    products_list = []
    for hose in hoses:
        purchase_options = [
            PurchaseOptionDetail(
                platform=option.platform,
                price=option.price,
                currency=option.currency,
                available=option.available,
                link=option.link,
            )
            for option in hose.PurchaseOptions
        ]
        product_detail = ProductDetail(
            id=hose.id,
            length=hose.length,
            diameter=hose.diameter,
            purchaseOptions=purchase_options,
        )
        products_list.append(product_detail)
    response = ProductsListResponse(products=products_list)
    return response
