from pydantic import BaseModel

class ShipmentCreate(BaseModel):
    shipment_id: str
    origin: str
    destination: str
    
class ShipmentStatusUpdate(BaseModel):
    status: str