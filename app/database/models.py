from sqlmodel import Column, Field, Relationship, SQLModel  # type: ignore
from enum import Enum
from datetime import datetime
from pydantic import EmailStr  # type: ignore
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql

# * We created sql model to define the data in the table that is the fields
# * as our columns and our api schema


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4(),
            primary_key=True,
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    # * foreign key
    seller_id: UUID = Field(foreign_key="seller.id")
    # ? relationship -> backpopulates to reflect the changes between tables
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Seller(SQLModel, table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4(),
            primary_key=True,
        )
    )
    name: str
    email: EmailStr
    password_hash: str

    # ? relationship -> backpopulates to reflect the changes between tables
    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        # ? This will ensure when we access the shipments on the seller field,
        # ? it actually goes ahead and selects the data from the database
        # ? that is all the shipments with this seller id adn give use back the same that is the shipments
        sa_relationship_kwargs={"lazy": "selectin"},
    )
