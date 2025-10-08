from typing import Annotated

from fastapi import Depends  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService


# ? Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ? Shipment service dep
def get_shipment_service(session: SessionDep):  # type: ignore
    return ShipmentService(session)


# ? Seller service dep
def get_seller_service(session: SessionDep):  # type: ignore
    return SellerService(session)


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
