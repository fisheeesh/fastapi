from typing import Optional
from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService
from app.services.notificatoin import NotificationService


class ShipmentEventService(BaseService):
    def __init__(self, session, tasks):
        super().__init__(ShipmentEvent, session)
        self.notification_service = NotificationService(tasks)

    async def add(
        self,
        shipment: Shipment,
        location: Optional[int] = None,
        status: Optional[ShipmentStatus] = None,
        description: Optional[str] = None,
    ) -> ShipmentEvent:
        if not location or not status:
            last_event = await self.get_latest_event(shipment)

            location = location if location else last_event.location
            status = status if status else last_event.status

        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=description
            if description
            else self._generate_description(
                status,
                location,
            ),
            shipment_id=shipment.id,
        )

        await self._notify(shipment, status)

        return await self._add(new_event)

    async def get_latest_event(self, shipment: Shipment):
        timeline = shipment.timeline

        if not timeline:
            raise ValueError("Shipment has no events in timeline")

        timeline.sort(key=lambda event: event.created_at)

        return timeline[-1]

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.delivered:
                return "successfully delivered"
            case ShipmentStatus.cancelled:
                return "cancelled by the seller"
            case _:  # * and ShipmentStatus.in_transit
                return f"scanned at {location}"

    async def _notify(self, shipment: Shipment, status: ShipmentStatus):
        if status == ShipmentStatus.in_transit:
            return

        subject: str
        context = {}
        template_name: str

        match status:
            case ShipmentStatus.placed:
                subject = "Your Order is Shipped 📦"
                context["id"] = shipment.id
                context["seller"] = shipment.seller.name  # type: ignore
                context["partner"] = shipment.delivery_partner.name  # type: ignore
                template_name = "mail_placed.html"

            case ShipmentStatus.out_for_delivery:
                subject = "Your Order is Arriving Soon 🛩️"
                template_name = "mail_out_for_delivery.html"

            case ShipmentStatus.delivered:
                subject = "Your Order is Delivered 🚚 "
                context["seller"] = shipment.seller.name  # type: ignore
                template_name = "mail_delivered.html"

            case ShipmentStatus.cancelled:
                subject = "Your Order is Cancelled ❌"
                template_name = "mail_cancelled.html"

        await self.notification_service.send_email_with_template(
            recipients=[shipment.client_contact_email],
            subject=subject,
            context=context,
            template_name=template_name,
        )
