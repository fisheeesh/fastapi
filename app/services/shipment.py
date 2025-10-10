from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.database.models import Seller, Shipment, ShipmentStatus
from datetime import datetime, timedelta
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from .basae import BaseService


class ShipmentService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Shipment, session)

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
        await self._delete(self.get(id))
