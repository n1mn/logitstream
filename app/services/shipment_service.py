import json 

from sqlalchemy.orm import Session

from app.models.shipment import Shipment
from app.repositories.shipment_repository import ShipmentRepository
from app.producers.kafka_producer import KafkaProducer
from app.repositories.shipment_event_repository import ShipmentEventRepository

from app.cache.redis_client import redis_client

class ShipmentService:
    def __init__(self):
        self.repository = ShipmentRepository()
        self.event_repository = ShipmentEventRepository()
        self.producer = KafkaProducer()
    
    def publish_shipment(self, shipment: dict):
        event = {
            "event_type": "SHIPMENT_CREATED",
            "shipment_id": shipment["shipment_id"],
            "status": "CREATED",
            "origin": shipment["origin"],
            "destination": shipment["destination"],
        }
        self.producer.publish_shipment(event)

    def create_shipment(
            self,
            db: Session,
            event: dict,
    ):
        shipment = Shipment(
            shipment_id=event["shipment_id"],
            status=event["status"],
            origin=event["origin"],
            destination=event["destination"],
        )

        shipment =self.repository.create(
            db=db,
            shipment=shipment,
        )
        self.event_repository.create(
            db=db,
            event=event,
        )
        return shipment
    
    def get_shipment(
    self,
    db: Session,
    shipment_id: str,
    ):
        cache_key = f"shipment:{shipment_id}"

        cached = redis_client.get(cache_key)

        if cached:
            print("🔥 Cache HIT")
            return json.loads(cached)

        print("💾 Cache MISS")

        shipment = self.repository.get_by_shipment_id(
            db=db,
            shipment_id=shipment_id,
        )

        if shipment is None:
            return None

        redis_client.set(
            cache_key,
            json.dumps(
                {
                    "shipment_id": shipment.shipment_id,
                    "status": shipment.status,
                    "origin": shipment.origin,
                    "destination": shipment.destination,
                }
            ),
        )

        return shipment
    
    def update_shipment_status(
            self,
            db,
            event: dict,
    ):
        shipment = self.repository.get_by_shipment_id(
            db=db, 
            shipment_id=event["shipment_id"]
        )
        if shipment is None:
           raise ValueError("Shipment not found")
        
        updated_shipment = self.repository.update_status(
            db=db, 
            shipment=shipment, 
            status=event["status"],
        )
        
        cache_key = f"shipment:{event['shipment_id']}"
        redis_client.delete(cache_key)

        self.event_repository.create(
            db=db, 
            event=event,
        )
        return updated_shipment
    
    def publish_status_update(
            self,
            shipment_id: str,
            status: str,
    ):
        event = {
            "event_type": "SHIPMENT_STATUS_UPDATED",
            "shipment_id": shipment_id,
            "status": status,
        }
        self.producer.publish_shipment(event)