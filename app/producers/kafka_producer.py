import json 

from confluent_kafka import Producer

from app.config.settings import settings

class KafkaProducer:

    def __init__(self):
        self.producer = Producer(
            {
                "bootstrap.servers": settings.kafka_bootstrap_servers,
            }
        )
    def publish_shipment(self, shipment: dict):

        self.producer.produce(
            topic="shipment-events",
            value=json.dumps(shipment).encode("utf-8"),
        )
        self.producer.flush()