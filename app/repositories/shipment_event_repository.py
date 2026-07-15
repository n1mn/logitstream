from sqlalchemy.orm import Session

from app.models.shipment_event import ShipmentEvent


class ShipmentEventRepository:

    def create(
        self,
        db: Session,
        event: dict,
    ):
        shipment_event = ShipmentEvent(
            shipment_id=event["shipment_id"],
            event_type=event["event_type"],
            status=event["status"],
        )

        db.add(shipment_event)
        db.commit()
        db.refresh(shipment_event)

        return shipment_event