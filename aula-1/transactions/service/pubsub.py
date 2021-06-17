from io import BytesIO

from kafka import KafkaConsumer
from fastavro import reader, parse_schema
from config import KAFKA_HOSTS


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
        self.consumer = KafkaConsumer(
            bootstrap_servers=hosts, value_deserializer=self._deserialize, group_id='transactions'
        )

    def _deserialize(self, payload):
        txn_reader = reader(BytesIO(), transaction_schema)
        return [event for event in txn_reader]

    def process_events(handler):
        for transaction in self.consumer:
            return handler(transaction)

