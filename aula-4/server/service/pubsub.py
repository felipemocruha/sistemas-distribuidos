from functools import wraps
from io import BytesIO
import logging
import sqlite3
import time

from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from fastavro import reader, writer, parse_schema

from service.config import KAFKA_HOSTS, KAFKA_USER, KAFKA_PASSWORD, DB_NAME
from service.db import DB


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
            logger.error(f"kafka error: {str(err)}")
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
                self.consumer = KafkaConsumer(
                    bootstrap_servers=hosts,
                    value_deserializer=self._deserialize,
                    group_id="???",
                    api_version=(0, 10, 1),
                    **auth,
                )

                self.client = KafkaAdminClient(
                    bootstrap_servers=hosts,
                    **auth,
                )
                break

            except Exception as err:
                logging.error(f"kafka must be available: {str(err)}")
                time.sleep(1)

    def _serialize(self, payload):
        serialized = BytesIO()
        writer(serialized, transaction_schema, [payload])
        serialized.seek(0)
        return serialized.read()

    def _deserialize(self, payload):
        msg_reader = reader(BytesIO(payload))
        return [event for event in msg_reader][0]

    def create_accounts(self, topic):
        self.consumer.subscribe([topic])

        @error_handler
        def create_account(data):
            username = data["username"].lower()
            created_at = data["event_timestamp"]

            try:
                topic = NewTopic(
                    name=f"{username}_message_inbox",
                    num_partitions=1,
                    replication_factor=3,
                )
                self.client.create_topics([topic], validate_only=False)
            except TopicAlreadyExistsError:
                pass

            database = DB(DB_NAME)
            try:
                database.create_account(username, created_at)
            except sqlite3.IntegrityError:
                pass

        for msg in self.consumer:
            return create_account(msg.value)


message_client = MessageClient(KAFKA_HOSTS, KAFKA_USER, KAFKA_PASSWORD)
