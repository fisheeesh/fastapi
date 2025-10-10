from datetime import datetime
from uuid import UUID

from pydantic import BaseModel  # type: ignore
from sqlmodel import Field, SQLModel  # type: ignore

from app.database.models import ShipmentStatus

# * For api schema, we used it for data validation in the request body and the response data


class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class ShipmentRead(BaseShipment):
    id: UUID
    status: ShipmentStatus
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
