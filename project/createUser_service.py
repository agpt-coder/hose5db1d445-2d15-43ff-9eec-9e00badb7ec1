from typing import Optional

import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateUserResponseModel(BaseModel):
    """
    The response object returning after creating a user. Includes either the ID of the newly created user or error message details.
    """

    success: bool
    message: str
    user_id: Optional[str] = None


async def createUser(
    email: str, password: str, role: prisma.enums.UserRole
) -> CreateUserResponseModel:
    """
    Creates a new user, stores user details in the database. Expected response includes a success message with the user's ID or an error message if creation fails.

    Args:
        email (str): Email address of the new user, must be unique across the system.
        password (str): Password for the account creation. It should be stored encrypted.
        role (UserRole): Role of the user, determining access control levels. Default is STANDARD_USER.

    Returns:
        CreateUserResponseModel: The response object returning after creating a user. Includes either the ID of the newly created user or error message details.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return CreateUserResponseModel(
            success=False, message="A user with this email already exists."
        )
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        user = await prisma.models.User.prisma().create(
            data={
                "email": email,
                "password": hashed_password.decode("utf-8"),
                "role": role,
            }
        )
        return CreateUserResponseModel(
            success=True, message="User created successfully.", user_id=user.id
        )
    except Exception as e:
        return CreateUserResponseModel(
            success=False, message=f"Failed to create user: {str(e)}"
        )
