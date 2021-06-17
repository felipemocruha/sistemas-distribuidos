from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config import CASSANDRA_HOSTS

transaction_repository = TransactionRepository


class TransactionRepository:
    def __init__(self):
        auth_provider = PlainTextAuthProvider(username="user", password="pass")
        cluster = Cluster(CASSANDRA_HOSTS, auth_provider=auth_provider)
        self.session = cluster.connect()

    def save(self, transaction):
        return self.session.execute(
            """
            INSERT INTO transactions(
              transaction_id,
              value_in_cents,
              description,
              customer_id,
              merchant_id,
              transaction_timestamp,
              event_timestamp,
              latitude,
              longitude
            )
            VALUES (
              %(transaction_id)s,
              %(value_in_cents)s,
              %(description)s,
              %(customer_id)s,
              %(merchant_id)s,
              %(transaction_timestamp)s,
              %(event_timestamp)s,
              %(latitude)s,
              %(longitude)s
            )
            """,
            transaction,
        )
