import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserDetailsResponse(BaseModel):
    """
    Provides the details of the user such as username, email, and role to authorized requesters. Ensures that sensitive data is only available under proper authorization.
    """

    username: str
    email: str
    role: prisma.enums.UserRole


async def getUserDetails(userId: str) -> UserDetailsResponse:
    """
    Fetches detailed information of a specific user by the user’s ID. This endpoint will return user details such as username, email, and role.

    Args:
        userId (str): Unique identifier of the user for whom the details are being fetched.

    Returns:
        UserDetailsResponse: Provides the details of the user such as username, email, and role to authorized requesters.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        raise ValueError("User not found")
    username = getattr(user, "username", user.email.split("@")[0])
    return UserDetailsResponse(username=username, email=user.email, role=user.role)
