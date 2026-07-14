import json

from confluent_kafka import Consumer

from app.config.settings import settings
from app.database.session import SessionLocal
from app.services.shipment_service import ShipmentService

service = ShipmentService()
consumer = Consumer(
    {
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": "shipment-consumer",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe(["shipment-events"])
print(consumer.list_topics().topics.keys())
print("Shipment Consumer Started...")

while True:
    msg = consumer.poll(1.0)
    print("Message recieved from Kafka")
    if msg is None:
        continue

    if msg.error():
        print(f" Kafka error: {msg.error()}")
        continue
    db = None
    try:
        db = SessionLocal()
        event = json.loads(msg.value().decode("utf-8"))

        if event["event_type"] == "SHIPMENT_CREATED":
            service.create_shipment(
                db=db,
                event=event,
            )
            print(f"✅ Saved {event['shipment_id']}")
        
        elif event["event_type"] == "SHIPMENT_STATUS_UPDATED":
            service.update_shipment_status(
                db=db,
                event=event,
            )
            print(f"✅ Updated {event['shipment_id']} to {event['status']}")

    except Exception as e:
        if db:
            db.rollback()
        print(f"❌ Failed to process event: {e}")

    finally:
        if db:
            db.close()

        