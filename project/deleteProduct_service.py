import prisma
import prisma.models
from pydantic import BaseModel


class DeleteProductResponse(BaseModel):
    """
    Provides feedback on the deletion operation of a product. Mainly for communicating success or failure of the operation.
    """

    message: str


async def deleteProduct(productId: str) -> DeleteProductResponse:
    """
    Permanently removes a product from the database to ensure up-to-date catalog maintenance. Restricted to admins to maintain control over the listed products.

    Args:
        productId (str): The unique identifier for the product that needs to be deleted.

    Returns:
        DeleteProductResponse: Provides feedback on the deletion operation of a product. Mainly for communicating success or failure of the operation.

    Example:
        deleteProduct("some-product-id")
        > DeleteProductResponse(message='Product deleted successfully.')
    """
    deleted = await prisma.models.Hose.prisma().delete(where={"id": productId})
    if deleted:
        return DeleteProductResponse(message="Product deleted successfully.")
    else:
        return DeleteProductResponse(message="Failed to delete the product.")
