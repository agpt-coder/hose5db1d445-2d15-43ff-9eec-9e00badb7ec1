import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    The API response indicating whether the deletion of the user was successful.
    """

    success: bool
    message: str


async def deleteUser(userId: str) -> DeleteUserResponse:
    """
    Removes a user's record from the database. Only administrators have the ability to delete users to ensure proper control.

    Args:
    userId (str): The unique identifier of the user to be deleted.

    Returns:
    DeleteUserResponse: The API response indicating whether the deletion of the user was successful.

    Example:
        deleteUser("0e12f87a-f06e-4d7d-b212-5c5e65a0b163")
        > DeleteUserResponse(success=True, message="User successfully deleted.")
    """
    try:
        user = await prisma.models.User.prisma().delete(where={"id": userId})
        return DeleteUserResponse(success=True, message="User successfully deleted.")
    except Exception as e:
        return DeleteUserResponse(success=False, message=str(e))
