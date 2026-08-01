from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.schemas import ShipmentCreate, ShipmentStatusUpdate
from app.services.shipment_service import ShipmentService
from app.services.analytics_service import AnalyticsService

from app.metrics import api_requests_total
router = APIRouter()

service = ShipmentService()
analytics_service = AnalyticsService()

@router.post("/shipments")
def create_shipment(shipment: ShipmentCreate):

    api_requests_total.inc()
    service.publish_shipment(
        shipment.model_dump()
    )
    return {
        "message": "Shipment event published successfully"
    }

@router.get("/shipments/{shipment_id}")
def get_shipment(
    shipment_id: str,
    db: Session = Depends(get_db),
):  
    api_requests_total.inc()
    shipment = service.get_shipment(
        db = db,
        shipment_id = shipment_id,
    )
    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )
    return shipment

@router.patch("/shipments/{shipment_id}/status")
def update_status(
    shipment_id: str,
    shipment: ShipmentStatusUpdate,
):  
    api_requests_total.inc()
    service.publish_status_update(
        shipment_id=shipment_id,
        status=shipment.status,
    )

    return {
        "message": "shipment status update event published."  
    }

@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
):
    api_requests_total.inc()
    return analytics_service.get_metrics(db)
