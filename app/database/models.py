from sqlalchemy import ARRAY, INTEGER
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
    cancelled = "cancelled"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    estimated_delivery: datetime
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    timeline: list["ShipmentEvent"] = Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    # * foreign key
    seller_id: UUID = Field(foreign_key="seller.id")
    # ? relationship -> backpopulates to reflect the changes between tables
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    delivery_partner_id: UUID = Field(foreign_key="delivery_partner.id")
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None


class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_event"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    location: int
    status: ShipmentStatus
    description: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipment.id")
    shipment: Shipment = Relationship(
        back_populates="timeline",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class User(SQLModel):
    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)


class Seller(User, table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    address: str | None = Field(default=None)
    zip_code: int | None = Field(default=None)

    # ? relationship -> backpopulates to reflect the changes between tables
    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        # ? This will ensure when we access the shipments on the seller field,
        # ? it actually goes ahead and selects the data from the database
        # ? that is all the shipments with this seller id adn give use back the same that is the shipments
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(
            ARRAY(INTEGER),
        )
    )
    max_handling_capacity: int

    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
            or shipment.status != ShipmentStatus.cancelled
        ]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)
