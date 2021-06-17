from io import BytesIO
import logging

from kafka import KafkaProducer
from fastavro import writer, parse_schema


logger = logging.getLogger()
transaction_client = TransactionClient(KAFKA_HOSTS)


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
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=hosts, value_serializer=self._serialize
            )
        except Exception as err:
            logging.error(f'kafka must be available: {str(err)}')
            exit(1)

    def _serialize(self, payload):
        serialized = BytesIO()
        writer(serialized, transaction_schema, [payload])
        return serialized

    def create(self, payload):
        try:
            return self.producer.send("transaction_created", payload)
        except Exception as err:
            logger.error(f'failed to send transaction to kafka: {str(err)}')            
