from fastapi import APIRouter, HTTPException, status  # type: ignore
from uuid import UUID

from fastapi.responses import HTMLResponse

from app.api.schemas.shipment import (  # type: ignore
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)
from app.database.models import Shipment
from ..dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep

router = APIRouter(prefix="/shipment", tags=["Shipment"])


# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@router.get("/", response_model=ShipmentRead)
async def get_shipment_by_id(id: UUID, service: ShipmentServiceDep):  # type: ignore
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# * Tracking details of shipment
@router.get("/track")
async def get_tracking(id: UUID, service: ShipmentServiceDep):
    shipment = await service.get(id)

    return HTMLResponse(
        content=f"<body> <h1>Order #{shipment.id}: {shipment.status}</h1> </body>"
    )


# * Create new shipment
@router.post("/", response_model=ShipmentRead)
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,  # type: ignore
) -> Shipment:
    return await service.add(shipment, seller)


@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: DeliveryPartnerDep,
    service: ShipmentServiceDep,
):  # type: ignore
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    return await service.update(id, shipment_update, partner)


@router.get("/cancel", response_model=ShipmentRead)
async def cancel_shipment(
    id: UUID,
    seller: SellerDep,
    service: ShipmentServiceDep,
):  # type: ignore
    return await service.cancel(id, seller)
