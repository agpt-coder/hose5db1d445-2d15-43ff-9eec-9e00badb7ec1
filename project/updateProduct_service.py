import prisma
import prisma.models
from pydantic import BaseModel


class ProductDetails(BaseModel):
    """
    A detailed model for a product that includes specifications and attributes that can be updated.
    """

    name: str
    description: str
    price: float
    available: bool


class Product(BaseModel):
    """
    The complete product model reflecting its current (updated) state.
    """

    id: str
    name: str
    description: str
    price: float
    available: bool


class ProductUpdateResponse(BaseModel):
    """
    The response after updating a product showing the updated details of the product.
    """

    updatedProduct: Product


async def updateProduct(
    productId: str, productDetails: ProductDetails
) -> ProductUpdateResponse:
    """
    Allows updating the details of an existing product, necessary when modifications to product specifications are made or errors need correction.

    Args:
        productId (str): The unique identifier of the product to be updated. This is part of the URL path.
        productDetails (ProductDetails): The updated product details.

    Returns:
        ProductUpdateResponse: The response after updating a product showing the updated details of the product.
    """
    hose = await prisma.models.Hose.prisma().find_unique(where={"id": productId})
    if not hose:
        raise ValueError("Product not found")
    updated_hose = await prisma.models.Hose.prisma().update(
        where={"id": productId}, data={"length": productDetails.price}
    )
    updated_product = Product(
        id=updated_hose.id,
        name=productDetails.name,
        description=productDetails.description,
        price=productDetails.price,
        available=productDetails.available,
    )
    return ProductUpdateResponse(updatedProduct=updated_product)
