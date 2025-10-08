from .routers import shipment, seller
from fastapi import APIRouter # type: ignore

master_router = APIRouter()

master_router.include_router(shipment.router)
master_router.include_router(seller.router)