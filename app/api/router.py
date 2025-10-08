from fastapi import APIRouter, HTTPException, status  # type: ignore

from app.api.schemas.shipment import (  # type: ignore
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)
from app.database.models import Shipment
from app.database.session import SessionDep
from app.services.shipment import ShipmentService

router = APIRouter()


# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment_by_id(id: int, session: SessionDep):  # type: ignore
    shipment = await ShipmentService(session).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# * Accept with body
@router.post("/shipment")
async def submit_shipment(
    shipment: ShipmentCreate,
    session: SessionDep,  # type: ignore
) -> Shipment:
    return await ShipmentService(session).add(shipment)


# * with body
@router.patch("/shipment", response_model=ShipmentRead)
async def patch_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):  # type: ignore
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = await ShipmentService(session).update(id, shipment_update)

    return shipment


@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:  # type: ignore
    await ShipmentService(session).delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}
