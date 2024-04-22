from datetime import datetime
from typing import List

from pydantic import BaseModel


class GetTipsRequest(BaseModel):
    """
    This model represents the request for fetching all hose care tips. No specific input parameters are required, aligning with the public accessibility of the route.
    """

    pass


class Tip(BaseModel):
    """
    Represents a single hose care tip including detailed information.
    """

    id: str
    title: str
    description: str
    createdAt: datetime


class GetTipsResponse(BaseModel):
    """
    This model encapsulates the response from retrieving hose care tips, outputting a list of tips.
    """

    tips: List[Tip]


async def listTips(request: GetTipsRequest) -> GetTipsResponse:
    """
    This route retrieves a list of all care tips from the Database Module. It returns an array of tips, each object containing tip details. The route can be accessed by anyone, including guests, as it's public.

    Args:
        request (GetTipsRequest): This model represents the request for fetching all hose care tips. No specific input parameters are required, aligning with the public accessibility of the route.

    Returns:
        GetTipsResponse: This model encapsulates the response from retrieving hose care tips, outputting a list of tips.

    Examples:
        request = GetTipsRequest()
        listTips(request)
        > GetTipsResponse(tips=[Tip(id='1', title='Proper Hose Storage', description='Store your hoses in a cool, dry place.', createdAt=datetime.now())])
    """
    tips_data = [
        {
            "id": "1",
            "title": "Proper Hose Storage",
            "description": "Store your hoses in a cool, dry place.",
            "createdAt": datetime.now(),
        },
        {
            "id": "2",
            "title": "Avoid Sunlight",
            "description": "Keep hoses away from direct sunlight to avoid degradation.",
            "createdAt": datetime.now(),
        },
    ]
    tips = [Tip(**tip) for tip in tips_data]
    return GetTipsResponse(tips=tips)
