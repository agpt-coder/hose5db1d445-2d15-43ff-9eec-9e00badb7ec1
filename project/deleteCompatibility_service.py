import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteCompatibilityResponse(BaseModel):
    """
    Confirms the deletion of a hose compatibility entry. Provides feedback on the outcome of the delete operation.
    """

    message: str


async def deleteCompatibility(compatibilityId: str) -> DeleteCompatibilityResponse:
    """
    Deletes a compatibility entry from the database using its ID. Ensures that only administrators can remove data to maintain data integrity. Response confirms deletion.

    Args:
        compatibilityId (str): The unique identifier for the hose compatibility entry to be deleted.

    Returns:
        DeleteCompatibilityResponse: Confirms the deletion of a hose compatibility entry. Provides feedback on the outcome of the delete operation.

    Example:
        compatibilityId = 'abc-123'
        deleteCompatibility(compatibilityId)
        > DeleteCompatibilityResponse(message='Compatibility entry deleted successfully.')
    """
    compatibility = await prisma.models.HoseCompatibility.prisma().find_unique(
        where={"id": compatibilityId}
    )
    if compatibility is None:
        return DeleteCompatibilityResponse(
            message=f"No compatibility entry found with ID: {compatibilityId}"
        )
    user = await prisma.models.User.prisma().find_unique(
        where={"id": compatibility.userId}
    )
    if user is None or user.role != prisma.enums.UserRole.ADMINISTRATOR:
        return DeleteCompatibilityResponse(
            message="Insufficient permissions to delete this entry."
        )
    await prisma.models.HoseCompatibility.prisma().delete(where={"id": compatibilityId})
    return DeleteCompatibilityResponse(
        message="Compatibility entry deleted successfully."
    )
