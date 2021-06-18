from io import BytesIO
import logging
import time

from kafka import KafkaProducer, KafkaClient
from fastavro import writer, parse_schema
from service.config import KAFKA_HOSTS


logger = logging.getLogger()


transaction_schema = parse_schema(
    {
        "doc": "A new transaction.",
        "name": "TransactionCreated",
        "namespace": "transactions",
        "type": "record",
        "fields": [
            {"name": "transaction_id", "type": "string"},
            {"name": "value_in_cents", "type": "int"},
            {"name": "description", "type": "string"},
            {"name": "customer_id", "type": "string"},
            {"name": "merchant_id", "type": "string"},
            {"name": "transaction_timestamp", "type": "int"},
            {"name": "event_timestamp", "type": "int"},
            {"name": "latitude", "type": "float"},
            {"name": "longitude", "type": "float"},
        ],
    }
)


class TransactionClient:
    def __init__(self, hosts):

        while True:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=hosts,
                    value_serializer=self._serialize,
                    api_version=(0, 10, 1),
                )
                client = KafkaClient(bootstrap_servers=hosts)
                client.add_topic('transaction_created')
                break

            except Exception as err:
                logging.error(f"kafka must be available: {str(err)}")
                time.sleep(1)

    def _serialize(self, payload):
        serialized = BytesIO()
        writer(serialized, transaction_schema, [payload])
        serialized.seek(0)
        return serialized.read()

    def create(self, payload):
        try:
            response = self.producer.send("transaction_created", payload)
            return response

        except Exception as err:
            logger.error(f"failed to send transaction to kafka: {str(err)}")
            raise err


transaction_client = TransactionClient(KAFKA_HOSTS)
