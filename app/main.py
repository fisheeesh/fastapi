from fastapi import FastAPI, HTTPException, Depends, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore
from app.database.session import creaed_db_tables, get_session, Shipment

from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate
from .db_helper import Database
from sqlmodel import Session # type: ignore
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan_hanlder(app: FastAPI):
    creaed_db_tables()
    yield


app = FastAPI(lifespan=lifespan_hanlder)

db = Database()


# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment_by_id(id: int, session: Session = Depends(get_session)):
    shipment = session.get(Shipment, id)

    
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# * Accept with body
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: Session = Depends(get_session)) -> dict[str, int]:
    new_id = db.create(shipment)
    return {"id": new_id}


# * with body
@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, shipment: ShipmentUpdate):
    updated_shipment = db.update(id, shipment)
    return updated_shipment


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
