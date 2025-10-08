from random import randint
from pydantic import BaseModel, Field  # type: ignore
from enum import Enum


def random_destination():
    return randint(11000, 11999)


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25, ge=1)
    destination: int


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    events: list


class Order(BaseModel):
    price: int
    title: str
    description: str


class ShipmentCreate(BaseShipment):
    order: Order


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25, ge=1)
    destination: int | None = Field(default=None)
    status: ShipmentStatus
