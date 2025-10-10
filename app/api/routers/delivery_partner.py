from fastapi import APIRouter, Depends, HTTPException, status

from app.database.redis import add_jti_to_blacklist

from ..schemas.delivery_partner import (
    DeliveryPartnerRead,
    DeliveryPartnerCreate,
    DeliveryPartnerUpdate,
)
from ..dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_delivery_partner_access_token,
)
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from typing import Annotated

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


# * Register a delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    seller: DeliveryPartnerCreate,
    service: DeliveryPartnerServiceDep,
):
    return await service.add(seller)


# * Login the delivery partner
@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "type": "jwt",
    }


# * Update delivery partner
@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    update = partner_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )
    return await service.update(partner.sqlmodel_update(update))


# * Logout delivery partner
@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
