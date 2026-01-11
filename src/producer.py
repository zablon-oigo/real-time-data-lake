import json
import logging
from confluent_kafka import Producer
from src.config import Config

logger = logging.getLogger(__name__)

class KafkaProducerClient:
    def __init__(self):
        self.producer = Producer({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVER})

    def publish(self, topic: str, data: dict):
        try:
            self.producer.produce(
                topic=topic,
                value=json.dumps(data).encode("utf-8"),
                key=str(data.get("uuid"))  
            )
            self.producer.flush()
            logger.info(f"Event published -> {topic}")
        except Exception as e:
            logger.error(f"Kafka publish error: {e}")

kafka_producer = KafkaProducerClient()




