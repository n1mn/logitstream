import json

from confluent_kafka import Producer


def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(
            f"✅ Delivered to {msg.topic()} "
            f"[{msg.partition()}] @ offset {msg.offset()}"
        )


producer = Producer(
    {
        "bootstrap.servers": "localhost:9092",
    }
)

event = {
    "shipment_id": "SHIP-1001",
    "status": "CREATED",
    "origin": "Delhi",
    "destination": "Mumbai",
}

producer.produce(
    "shipment-events",
    json.dumps(event).encode("utf-8"),
    callback=delivery_report,
)

producer.flush()