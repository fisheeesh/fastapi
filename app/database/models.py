from sqlmodel import Field, SQLMOdel  # type: ignore
from enum import Enum
from datetime import datetime


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLMOdel):
    __tablename__ = "shipment"

    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
