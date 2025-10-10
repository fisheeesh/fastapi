from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.database.models import Seller, Shipment, ShipmentStatus
from datetime import datetime, timedelta
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from .delivery_partner import DeliveryPartnerService
from .base import BaseService
from fastapi import HTTPException, status


class ShipmentService(BaseService):
    def __init__(self, session: AsyncSession, partner_service: DeliveryPartnerService):
        super().__init__(Shipment, session)
        self.partner_service = partner_service

    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
            # seller=seller
        )
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        return await self._add(new_shipment)

    async def update(
        self, id: UUID, shipment_update: ShipmentUpdate
    ) -> Shipment | None:
        shipment = await self.get(id)
        if shipment is None:
            return None
        shipment.sqlmodel_update(shipment_update)

        return await self._update(shipment)

    async def delete(self, id: UUID) -> None:
        shipment = await self.get(id)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
            )
        await self._delete(shipment)
