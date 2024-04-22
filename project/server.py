import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import project.createCompatibility_service
import project.createMeasurement_service
import project.createProduct_service
import project.createTip_service
import project.createUser_service
import project.deleteCompatibility_service
import project.deleteMeasurement_service
import project.deleteProduct_service
import project.deleteTip_service
import project.deleteUser_service
import project.fetchCompatibilities_service
import project.getCompatibility_service
import project.getMeasurement_service
import project.getProductDetails_service
import project.getPurchasePlatforms_service
import project.getTip_service
import project.getUserDetails_service
import project.listMeasurements_service
import project.listProducts_service
import project.listTips_service
import project.listUsers_service
import project.logUserInquiry_service
import project.updateCompatibility_service
import project.updateMeasurement_service
import project.updateProduct_service
import project.updateTip_service
import project.updateUser_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hose", lifespan=lifespan, description="a really weird length of hose?"
)


@app.delete(
    "/measurements/{measurementId}",
    response_model=project.deleteMeasurement_service.DeleteMeasurementResponse,
)
async def api_delete_deleteMeasurement(
    measurementId: str,
) -> project.deleteMeasurement_service.DeleteMeasurementResponse | Response:
    """
    Deletes a specific measurement from the database by ID. This is generally accessed by administrators for managing data retention or correcting errors. Database Module carries out the deletion process. Responds with success status if deletion is successful.
    """
    try:
        res = await project.deleteMeasurement_service.deleteMeasurement(measurementId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete("/tips/{tipId}", response_model=project.deleteTip_service.DeleteTipResponse)
async def api_delete_deleteTip(
    tipId: str,
) -> project.deleteTip_service.DeleteTipResponse | Response:
    """
    Enables administrators to delete a care tip by tipId. It removes the tip from the Database Module and returns a success message with a 204 response code upon successful deletion.
    """
    try:
        res = await project.deleteTip_service.deleteTip(tipId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user-inquiries", response_model=project.logUserInquiry_service.UserInquiryResponse
)
async def api_post_logUserInquiry(
    userId: str, inquiryDetails: str, timestamp: Optional[datetime]
) -> project.logUserInquiry_service.UserInquiryResponse | Response:
    """
    Logs user inquiries regarding product preferences and purchase history to the Database Module for future analytics and personalized user experiences. The body of the request should include user ID, inquiry details, and possibly the timestamp. This is protected to ensure data integrity and confidentiality.
    """
    try:
        res = await project.logUserInquiry_service.logUserInquiry(
            userId, inquiryDetails, timestamp
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/products/{productId}",
    response_model=project.deleteProduct_service.DeleteProductResponse,
)
async def api_delete_deleteProduct(
    productId: str,
) -> project.deleteProduct_service.DeleteProductResponse | Response:
    """
    Permanently removes a product from the database to ensure up-to-date catalog maintenance. Restricted to admins to maintain control over the listed products.
    """
    try:
        res = await project.deleteProduct_service.deleteProduct(productId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/products/{productId}",
    response_model=project.updateProduct_service.ProductUpdateResponse,
)
async def api_put_updateProduct(
    productId: str, productDetails: project.updateProduct_service.ProductDetails
) -> project.updateProduct_service.ProductUpdateResponse | Response:
    """
    Allows updating the details of an existing product, necessary when modifications to product specifications are made or errors need correction.
    """
    try:
        res = await project.updateProduct_service.updateProduct(
            productId, productDetails
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/compatibilities/{compatibilityId}",
    response_model=project.getCompatibility_service.CompatibilityResponse,
)
async def api_get_getCompatibility(
    compatibilityId: str,
) -> project.getCompatibility_service.CompatibilityResponse | Response:
    """
    Fetches detailed information about a specific compatibility entry using its ID. It requests this information from the Database Module. The response contains detailed data regarding the selected compatibility.
    """
    try:
        res = await project.getCompatibility_service.getCompatibility(compatibilityId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/compatibilities",
    response_model=project.createCompatibility_service.CompatibilityCreationResponse,
)
async def api_post_createCompatibility(
    hoseId: str, userId: str, compatible: bool, attachment: str
) -> project.createCompatibility_service.CompatibilityCreationResponse | Response:
    """
    Creates a new compatibility entry. It uses the Database Module to store compatibility rules between hoses and attachments. Expected response should confirm the creation along with details of the new entry.
    """
    try:
        res = await project.createCompatibility_service.createCompatibility(
            hoseId, userId, compatible, attachment
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/measurements",
    response_model=project.listMeasurements_service.GetMeasurementsResponse,
)
async def api_get_listMeasurements(
    request: project.listMeasurements_service.GetMeasurementsRequest,
) -> project.listMeasurements_service.GetMeasurementsResponse | Response:
    """
    Retrieves a list of all hose measurements. This route queries the Database Module to fetch all measurement records and displays them, typically used in reporting or dashboard features. Returns an array of measurements.
    """
    try:
        res = await project.listMeasurements_service.listMeasurements(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/measurements/{measurementId}",
    response_model=project.updateMeasurement_service.UpdateMeasurementResponse,
)
async def api_put_updateMeasurement(
    measurementId: str, length: float, diameter: float
) -> project.updateMeasurement_service.UpdateMeasurementResponse | Response:
    """
    Updates a specific measurement record. This endpoint allows modifications to length or diameter values of an existing record based on provided data. Database Module implements the update. Expect a success or error message in response.
    """
    try:
        res = await project.updateMeasurement_service.updateMeasurement(
            measurementId, length, diameter
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponseModel)
async def api_post_createUser(
    email: str, password: str, role: prisma.enums.UserRole
) -> project.createUser_service.CreateUserResponseModel | Response:
    """
    Creates a new user, stores user details in the database. Expected response includes a success message with the user's ID or an error message if creation fails.
    """
    try:
        res = await project.createUser_service.createUser(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/compatibilities/{compatibilityId}",
    response_model=project.updateCompatibility_service.UpdateCompatibilityResponse,
)
async def api_put_updateCompatibility(
    compatibilityId: str,
    compatible: bool,
    attachment: str,
    checkedAt: Optional[datetime],
) -> project.updateCompatibility_service.UpdateCompatibilityResponse | Response:
    """
    Updates an existing compatibility entry based on its ID. It modifies data in the Database Module. Expected response should confirm the update and show the modified compatibility data.
    """
    try:
        res = await project.updateCompatibility_service.updateCompatibility(
            compatibilityId, compatible, attachment, checkedAt
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put("/tips/{tipId}", response_model=project.updateTip_service.UpdateTipResponse)
async def api_put_updateTip(
    tipId: str, tipTitle: str, tipContent: str, applicableProducts: List[str]
) -> project.updateTip_service.UpdateTipResponse | Response:
    """
    Allows administrators to update existing care tip details identified by tipId. The endpoint requires JSON body with updates, modifies the record in the Database Module, and returns the updated tip object.
    """
    try:
        res = await project.updateTip_service.updateTip(
            tipId, tipTitle, tipContent, applicableProducts
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/measurements",
    response_model=project.createMeasurement_service.MeasurementCreationResponse,
)
async def api_post_createMeasurement(
    hoseId: str, length: float, diameter: float, userId: str
) -> project.createMeasurement_service.MeasurementCreationResponse | Response:
    """
    Creates a new measurement record in the database. This route receives measurement data (length, diameter) from the User Interface Module, and stores it in the Database Module. Expect a response indicating successful creation or an error.
    """
    try:
        res = await project.createMeasurement_service.createMeasurement(
            hoseId, length, diameter, userId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: str,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Removes a user's record from the database. Only administrators have the ability to delete users to ensure proper control.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/purchase-platforms",
    response_model=project.getPurchasePlatforms_service.GetPurchasePlatformsResponse,
)
async def api_get_getPurchasePlatforms(
    product_id: str, user_location: Optional[str]
) -> project.getPurchasePlatforms_service.GetPurchasePlatformsResponse | Response:
    """
    Retrieves a list of available e-commerce platforms from which a user can purchase the specified product, including price comparisons. This endpoint consumes data from external e-commerce APIs, and the response will typically include platform name, price, and direct link to the purchase page.
    """
    try:
        res = await project.getPurchasePlatforms_service.getPurchasePlatforms(
            product_id, user_location
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/tips", response_model=project.listTips_service.GetTipsResponse)
async def api_get_listTips(
    request: project.listTips_service.GetTipsRequest,
) -> project.listTips_service.GetTipsResponse | Response:
    """
    This route retrieves a list of all care tips from the Database Module. It returns an array of tips, each object containing tip details. The route can be accessed by anyone, including guests, as it's public.
    """
    try:
        res = await project.listTips_service.listTips(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/tips/{tipId}", response_model=project.getTip_service.TipDetailsResponse)
async def api_get_getTip(
    tipId: str,
) -> project.getTip_service.TipDetailsResponse | Response:
    """
    Fetches detailed information about a specific care tip identified by tipId. This endpoint extracts the tip details from the Database Module and is accessible by standard users and administrators, ensuring guests cannot access specific care tip details.
    """
    try:
        res = await project.getTip_service.getTip(tipId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/products", response_model=project.listProducts_service.ProductsListResponse)
async def api_get_listProducts(
    hose_diameter_min: Optional[float],
    hose_diameter_max: Optional[float],
    hose_length_min: Optional[float],
    hose_length_max: Optional[float],
) -> project.listProducts_service.ProductsListResponse | Response:
    """
    Retrieves a list of all products, focusing primarily on the available hoses. Useful for both users and administrators for browsing products.
    """
    try:
        res = await project.listProducts_service.listProducts(
            hose_diameter_min, hose_diameter_max, hose_length_min, hose_length_max
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/measurements/{measurementId}",
    response_model=project.getMeasurement_service.MeasurementDetailsResponse,
)
async def api_get_getMeasurement(
    measurementId: str,
) -> project.getMeasurement_service.MeasurementDetailsResponse | Response:
    """
    Fetches specific measurement details using the measurement ID. It queries the Database Module for the record and presents the details. Useful for audits or detailed reviews. Returns a single measurement detail.
    """
    try:
        res = await project.getMeasurement_service.getMeasurement(measurementId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/compatibilities/{compatibilityId}",
    response_model=project.deleteCompatibility_service.DeleteCompatibilityResponse,
)
async def api_delete_deleteCompatibility(
    compatibilityId: str,
) -> project.deleteCompatibility_service.DeleteCompatibilityResponse | Response:
    """
    Deletes a compatibility entry from the database using its ID. Ensures that only administrators can remove data to maintain data integrity. Response confirms deletion.
    """
    try:
        res = await project.deleteCompatibility_service.deleteCompatibility(
            compatibilityId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/products", response_model=project.createProduct_service.CreateHoseResponse)
async def api_post_createProduct(
    length: float, diameter: float, features: List[str]
) -> project.createProduct_service.CreateHoseResponse | Response:
    """
    Creates a new product entry, specifically for entering new types of hoses into the system. This includes unique length and features. Expected response includes success status with newly created product ID.
    """
    try:
        res = await project.createProduct_service.createProduct(
            length, diameter, features
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/products/{productId}",
    response_model=project.getProductDetails_service.ProductDetailsResponse,
)
async def api_get_getProductDetails(
    productId: str,
) -> project.getProductDetails_service.ProductDetailsResponse | Response:
    """
    Provides detailed information about specific products identified by their unique product ID. This will aid in specific compatibility checks and feature information.
    """
    try:
        res = await project.getProductDetails_service.getProductDetails(productId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/{userId}", response_model=project.getUserDetails_service.UserDetailsResponse
)
async def api_get_getUserDetails(
    userId: str,
) -> project.getUserDetails_service.UserDetailsResponse | Response:
    """
    Fetches detailed information of a specific user by the user’s ID. This endpoint will return user details such as username, email, and role.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/compatibilities",
    response_model=project.fetchCompatibilities_service.GetCompatibilitiesResponse,
)
async def api_get_fetchCompatibilities(
    request: project.fetchCompatibilities_service.GetCompatibilitiesRequest,
) -> project.fetchCompatibilities_service.GetCompatibilitiesResponse | Response:
    """
    Retrieves all compatibility entries from the database. It queries the Database Module for a list of all existing compatibility rules. The response includes an array of compatibility data.
    """
    try:
        res = await project.fetchCompatibilities_service.fetchCompatibilities(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/tips", response_model=project.createTip_service.TipResponseModel)
async def api_post_createTip(
    description: str, hoseTypeId: str, additionalTips: List[str]
) -> project.createTip_service.TipResponseModel | Response:
    """
    This route allows administrators to create a new care tip. It accepts a JSON body with tip details, stores it in the Database Module, and returns the created tip object with a 201 response code.
    """
    try:
        res = await project.createTip_service.createTip(
            description, hoseTypeId, additionalTips
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.listUsers_service.GetUsersResponse)
async def api_get_listUsers(
    request: project.listUsers_service.GetUsersRequest,
) -> project.listUsers_service.GetUsersResponse | Response:
    """
    Retrieves a list of all users, returning an array of user data. Useful for admins to oversee user base.
    """
    try:
        res = await project.listUsers_service.listUsers(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}", response_model=project.updateUser_service.UpdateUserResponse
)
async def api_put_updateUser(
    userId: str, email: str, name: str, role: Optional[str]
) -> project.updateUser_service.UpdateUserResponse | Response:
    """
    Updates the details of an existing user using their ID. Users can update their own information; admins can update any user's information.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, email, name, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
