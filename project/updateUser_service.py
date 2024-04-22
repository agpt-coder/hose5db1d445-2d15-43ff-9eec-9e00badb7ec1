from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
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


class User(BaseModel):
    """
    Model representing a user, including all user-specific fields as defined in the database.
    """

    id: str
    email: str
    password: str
    createdAt: datetime
    updatedAt: datetime
    lastLogin: Optional[datetime] = None
    role: prisma.enums.UserRole
    HoseMeasurements: List[HoseMeasurement]
    HoseCompatibilityLogs: List[HoseCompatibility]
    UsageLogs: List[prisma.models.UsageLog]
    Questions: List[prisma.models.Question]
    prisma.models.Answer: List[
        prisma.models.Answer
    ]  # TODO(autogpt): Type annotation not supported for this statement. reportInvalidTypeForm


class UpdateUserResponse(BaseModel):
    """
    Response model that confirms the user details have been updated. Returns updated user information.
    """

    message: str
    user: User


async def updateUser(
    userId: str, email: str, name: str, role: Optional[str]
) -> UpdateUserResponse:
    """
    Updates the details of an existing user using their ID. Users can update their own information; admins can update any user's information.

    Args:
        userId (str): The ID of the user to update. This is required to fetch the correct user from the database.
        email (str): The new email address for the user.
        name (str): The full name of the user.
        role (Optional[str]): The user role, which can only be modified by administrators. Can be one of 'ADMINISTRATOR', 'STANDARD_USER', or 'GUEST'.

    Returns:
        UpdateUserResponse: Response model that confirms the user details have been updated. Returns updated user information.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return UpdateUserResponse(message="User not found", user=None)
    update_data = {"email": email, "name": name}
    if role is not None and user.role == "ADMINISTRATOR":
        update_data["role"] = role
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId}, data=update_data
    )
    return UpdateUserResponse(message="User updated successfully", user=updated_user)
