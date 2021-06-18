from io import BytesIO
import logging
import time

from kafka import KafkaConsumer, KafkaClient
from fastavro import reader, parse_schema
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
                self.consumer = KafkaConsumer(
                    bootstrap_servers=hosts,
                    value_deserializer=self._deserialize,
                    group_id='transactions',
                    api_version=(0, 10, 1),
                )
                self.consumer.subscribe(['transaction_created'])
                break

            except Exception as err:
                logging.error(f"kafka must be available: {str(err)}")
                time.sleep(1)

    def _deserialize(self, payload):
        txn_reader = reader(BytesIO(payload))
        return [event for event in txn_reader][0]

    def process_events(self, handler):
        for transaction in self.consumer:
            return handler(transaction.value)


transaction_client = TransactionClient(KAFKA_HOSTS)
