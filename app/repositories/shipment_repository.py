from sqlalchemy.orm import Session

from app.models.shipment import Shipment

class ShipmentRepository:
    def create(
        self,
        db: Session,
        shipment: Shipment,
    ):
        db.add(shipment)
        db.commit()
        db.refresh(shipment)

        return shipment
    
    
    def get_by_shipment_id(
    self,
    db: Session,
    shipment_id: str,
    ):
        print(f"Searching for: {shipment_id}")

        shipment = (
            db.query(Shipment)
            .filter(Shipment.shipment_id == shipment_id)
            .first()
        )

        print(f"Found: {shipment}")

        return shipment
    
    def update_status(
        self,
        db: Session,
        shipment: Shipment,
        status: str,
    ):
        shipment.status = status 

        db.commit()
        db.refresh(shipment)

        return shipment