from functools import wraps
from io import BytesIO
import logging
import time

from kafka import KafkaProducer, KafkaConsumer
from fastavro import reader, writer, parse_schema
from service.config import KAFKA_HOSTS, KAFKA_USER, KAFKA_PASSWORD


logger = logging.getLogger()


account_created_schema = parse_schema(
    {
        "doc": "A new account.",
        "name": "AccountCreated",
        "namespace": "accounts",
        "type": "record",
        "fields": [
            {"name": "username", "type": "string"},
            {"name": "event_timestamp", "type": "int"},
        ],
    }
)


message_sent_schema = parse_schema(
    {
        "doc": "A new message",
        "name": "MessageSent",
        "namespace": "messages",
        "type": "record",
        "fields": [
            {"name": "source_username", "type": "string"},
            {"name": "message", "type": "string"},
            {"name": "event_timestamp", "type": "int"},
        ],
    }
)


def error_handler(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)

        except Exception as err:
            logger.error(f"failed to send payload to kafka: {str(err)}")
            raise err

    return wrapper


class MessageClient:
    def __init__(self, hosts, user, password):
        auth = {
            "security_protocol": "SASL_SSL",
            "sasl_mechanism": "PLAIN",
            "sasl_plain_username": user,
            "sasl_plain_password": password,
        }

        while True:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=hosts,
                    api_version=(0, 10, 1),
                    **auth,
                )

                self.consumer = KafkaConsumer(
                    bootstrap_servers=hosts,
                    value_deserializer=self._deserialize,
                    group_id="???",
                    api_version=(0, 10, 1),
                    **auth,
                )
                break

            except Exception as err:
                logger.error(f"kafka must be available: {str(err)}")
                time.sleep(1)

    def _serialize(self, payload, schema):
        serialized = BytesIO()
        writer(serialized, schema, [payload])
        serialized.seek(0)
        return serialized.read()

    def _deserialize(self, payload):
        msg_reader = reader(BytesIO(payload))
        return [event for event in msg_reader][0]

    @error_handler
    def create_account(self, account_name):
        # fill here
        pass

    @error_handler
    def send_message(self, topic, payload):
        # fill here
        pass

    def receive_messages(self, topic):
        self.consumer.subscribe([topic])

        def handler(data):
            # fill here
            pass

        for msg in self.consumer:
            return handler(msg.value)


message_client = MessageClient(KAFKA_HOSTS, KAFKA_USER, KAFKA_PASSWORD)
