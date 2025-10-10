from datetime import datetime
from email.policy import default
from uuid import UUID

from pydantic import BaseModel  # type: ignore
from sqlmodel import Field, SQLModel  # type: ignore

from app.database.models import Seller, ShipmentEvent, ShipmentStatus

# * For api schema, we used it for data validation in the request body and the response data


class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class ShipmentRead(BaseShipment):
    id: UUID
    # seller: Seller
    timeline: list[ShipmentEvent]
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    location: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    description: str | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
