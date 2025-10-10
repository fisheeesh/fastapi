from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.core.security import oauth2_scheme_seller, oauth2_scheme_delivery_partner
from app.database.models import DeliveryPartner, Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.uitls import decode_access_token

# ? Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ? Access token data dep
async def _get_access_token(
    token: str,
) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    return data


# ? Seller access token data
async def get_seller_access_token(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
) -> dict:
    return await _get_access_token(token)


# ? Delivery Partner access token data
async def get_delivery_partner_access_token(
    token: Annotated[str, Depends(oauth2_scheme_delivery_partner)],
) -> dict:
    return await _get_access_token(token)


# ? Logged In Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDep,
):
    seller = await session.get(Seller, UUID(token_data["user"]["id"]))

    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

    return seller


# ? Logged In Delivery Partner
async def get_current_delivery_partner(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
    session: SessionDep,
):
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))

    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

    return partner


# ? Shipment service dep
def get_shipment_service(session: SessionDep):  # type: ignore
    return ShipmentService(session)


# ? Seller service dep
def get_seller_service(session: SessionDep):  # type: ignore
    return SellerService(session)


# ? Seller Dep
SellerDep = Annotated[
    Seller,
    Depends(get_current_seller),
]

# ? Delivery Partner Dep
DeliveryPartnerDep = Annotated[
    DeliveryPartner,
    Depends(get_current_delivery_partner),
]


# ? Shipment service dep annotation
ShipmentServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]

# ? Seller service dep annotation
SellerServiceDep = Annotated[
    SellerService,
    Depends(get_seller_service),
]
