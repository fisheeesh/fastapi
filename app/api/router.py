from fastapi import APIRouter, HTTPException, status  # type: ignore

from app.api.schemas.shipment import (  # type: ignore
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)
from app.database.models import Shipment
from .dependencies import ServiceDep

# Remove dependencies=[ServiceDep] from here!
router = APIRouter(prefix="/shipment", tags=["Shipment"])


# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@router.get("/", response_model=ShipmentRead)
async def get_shipment_by_id(id: int, service: ServiceDep):  # type: ignore
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# * Accept with body
@router.post("/")
async def submit_shipment(
    shipment: ShipmentCreate,
    service: ServiceDep,  # type: ignore
) -> Shipment:
    return await service.add(shipment)


# * with body
@router.patch("/", response_model=ShipmentRead)
async def patch_shipment(
    id: int,
    shipment_update: ShipmentUpdate,
    service: ServiceDep,
):  # type: ignore
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = await service.update(id, shipment_update)

    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:  # type: ignore
    await service.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}
