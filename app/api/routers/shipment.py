from fastapi import APIRouter, HTTPException, status  # type: ignore

from app.api.schemas.shipment import (  # type: ignore
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)
from app.database.models import Shipment
from ..dependencies import SellerDep, ShipmentServiceDep

router = APIRouter(prefix="/shipment", tags=["Shipment"])


# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@router.get("/", response_model=ShipmentRead)
async def get_shipment_by_id(id: int, _: SellerDep, service: ShipmentServiceDep):  # type: ignore
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# * Accept with body
@router.post("/")
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,  # type: ignore
) -> Shipment:
    return await service.add(shipment)


# * with body
@router.patch("/", response_model=ShipmentRead)
async def patch_shipment(
    id: int,
    shipment_update: ShipmentUpdate,
    service: ShipmentServiceDep,
):  # type: ignore
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await service.update(id, shipment_update)

    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:  # type: ignore
    await service.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}
