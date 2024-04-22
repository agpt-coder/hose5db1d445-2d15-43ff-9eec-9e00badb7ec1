from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetUsersRequest(BaseModel):
    """
    Request model for retrieving all users. No inputs required for this endpoint as it just retrieves all users.
    """

    pass


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


class GetUsersResponse(BaseModel):
    """
    Response model for retrieving all users. Contains a list of user objects detailing each user's information.
    """

    users: List[User]


async def listUsers(request: GetUsersRequest) -> GetUsersResponse:
    """
    Retrieves a list of all users, returning an array of user data including all elements related to the user.
    Useful for admins to oversee the user base.

    Args:
        request (GetUsersRequest): Request model for retrieving all users. No inputs required for this endpoint as it just retrieves all users.

    Returns:
        GetUsersResponse: Response model for retrieving all users. Contains a list of user objects detailing each user's information.

    Example:
        request = GetUsersRequest()
        response = await listUsers(request)
        > GetUsersResponse(users=[User(id='1', email='example@example.com', ...), User(id='2', email='example2@example.com', ...)])
    """
    users = await prisma.models.User.prisma().find_many(
        include={
            "HoseMeasurements": True,
            "HoseCompatibilityLogs": True,
            "UsageLogs": True,
            "Questions": True,
            "Answers": True,
        }
    )
    return GetUsersResponse(users=users)
