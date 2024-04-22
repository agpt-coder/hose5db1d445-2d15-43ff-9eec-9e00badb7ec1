import prisma
import prisma.models
from pydantic import BaseModel


class DeleteTipResponse(BaseModel):
    """
    Acknowledges the successful deletion of a care tip without exposing any data, as befitting the 204 No Content response.
    """

    pass


async def deleteTip(tipId: str) -> DeleteTipResponse:
    """
    Enables administrators to delete a care tip (Question entity) by tipId. It removes the tip from the Database Module and returns a success message with a 204 response code upon successful deletion.

    Args:
        tipId (str): The unique identifier (UUID) for the care tip to be deleted.

    Returns:
        DeleteTipResponse: Acknowledges the successful deletion of a care tip without exposing any data, as befitting the 204 No Content response.

    Example:
        try:
            response = await deleteTip('123e4567-e89b-12d3-a456-426614174000')
            print(response)  # Instance of DeleteTipResponse, representing a successful operation
        except Exception as e:
            print(str(e))
    """
    deleted_tip = await prisma.models.Question.prisma().delete(where={"id": tipId})
    if deleted_tip:
        return DeleteTipResponse()
    else:
        raise Exception("Failed to delete tip with ID: " + tipId)
