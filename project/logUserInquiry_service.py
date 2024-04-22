from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserInquiryResponse(BaseModel):
    """
    This model provides feedback that the user's inquiry has been logged successfully. It includes the status of the request and any error or success messages.
    """

    success: bool
    message: str
    inquiryId: Optional[str] = None


async def logUserInquiry(
    userId: str, inquiryDetails: str, timestamp: Optional[datetime] = None
) -> UserInquiryResponse:
    """
    Logs user inquiries regarding product preferences and purchase history to the Database Module for future analytics and personalized user experiences. The body of the request should include user ID, inquiry details, and possibly the timestamp. This is protected to ensure data integrity and confidentiality.

    Args:
        userId (str): The unique identifier of the user making the inquiry.
        inquiryDetails (str): Detailed description of the user's inquiry regarding their product preferences or purchase history.
        timestamp (Optional[datetime]): Optional timestamp when the inquiry was made. If not provided, the server's current time could be used.

    Returns:
        UserInquiryResponse: This model provides feedback that the user's inquiry has been logged successfully. It includes the status of the request and any error or success messages.
    """
    if not timestamp:
        timestamp = datetime.now()
    try:
        inquiry = await prisma.models.Question.prisma().create(
            data={
                "content": inquiryDetails,
                "userId": userId,
                "createdAt": timestamp,
                "updatedAt": timestamp,
            }
        )
        return UserInquiryResponse(
            success=True, message="Inquiry logged successfully.", inquiryId=inquiry.id
        )
    except Exception as e:
        return UserInquiryResponse(success=False, message=str(e))
