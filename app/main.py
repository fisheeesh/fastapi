from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.database.models import ShipmentStatus, Shipment
from app.database.session import SessionDep, creaed_db_tables

from .api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

from app.api.router import router


@asynccontextmanager
async def lifespan_hanlder(app: FastAPI):
    creaed_db_tables()
    yield


app = FastAPI(lifespan=lifespan_hanlder)

app.include_router(router)

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
