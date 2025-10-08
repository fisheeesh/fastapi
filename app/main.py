from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep, creaed_db_tables

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_hanlder(app: FastAPI):
    creaed_db_tables()
    yield


app = FastAPI(lifespan=lifespan_hanlder)


# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment_by_id(id: int, session: SessionDep):  # type: ignore
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# * Accept with body
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:  # type: ignore
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


# * with body
@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):  # type: ignore
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:  # type: ignore
    session.delete(session.get(Shipment, id))

    session.commit()

    return {"detail": f"Shipment with id #{id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
