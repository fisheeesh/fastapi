from random import randint
from pydantic import BaseModel, Field  # type: ignore
from app.database.models import ShipmentStatus


def random_destination():
    return randint(11000, 11999)


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25, ge=1)


class ShipmentRead(BaseShipment):
    id: int
    status: ShipmentStatus


class Order(BaseModel):
    price: int
    title: str
    description: str


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25, ge=1)
    destination: int | None = Field(default=None)
    status: ShipmentStatus
