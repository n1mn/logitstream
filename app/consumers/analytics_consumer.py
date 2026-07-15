import json

from confluent_kafka import Consumer

from app.config.settings import settings
from app.database.session import SessionLocal
from app.services.analytics_service import AnalyticsService

service = AnalyticsService()

consumer = Consumer(
    {
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": "analytics-consumer",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe(["shipment-events"])

print("Analytics Consumer Started...")

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print(msg.error())
        continue

    db = None

    try:
        db = SessionLocal()

        event = json.loads(
            msg.value().decode("utf-8")
        )

        service.process_event(
            db=db,
            event=event,
        )

        print(
            f"📊 Analytics Updated: {event['event_type']}"
        )

    except Exception as e:

        if db:
            db.rollback()

        print(f"❌ {e}")

    finally:

        if db:
            db.close()