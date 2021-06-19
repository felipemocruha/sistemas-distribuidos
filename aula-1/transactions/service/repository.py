import time
import logging
from cassandra.cluster import Cluster
from service.config import CASSANDRA_HOSTS


logger = logging.getLogger()


class TransactionRepository:
    def __init__(self, hosts):

        while True:
            try:
                cluster = Cluster(hosts)
                self.session = cluster.connect()

                self.session.execute(
                    """
                    CREATE KEYSPACE IF NOT EXISTS transactions
                    WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};
                    """
                )
                self.session.set_keyspace("transactions")

                self.session.execute(
                    """
                    CREATE TABLE IF NOT EXISTS transactions(
                    transaction_id text,
                    value_in_cents int,
                    description text,
                    customer_id text,
                    merchant_id text,
                    transaction_timestamp int,
                    event_timestamp int,
                    latitude float,
                    longitude float,
                    status text,
                    PRIMARY KEY (transaction_id)
                    )
                    """
                )
                logger.error("cassandra connection success")
                break

            except Exception as err:
                logger.error(f"cassandra seems unavailable: {str(err)}")
                time.sleep(1)

    def save(self, transaction):
        try:
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
                  longitude,
                  status
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
                  %(longitude)s,
                  %(status)s
                )
                """,
                transaction,
            )

        except Exception as err:
            logger.error(f"failed to run statement: {str(err)}")
            raise RepositoryError()


class RepositoryError(Exception):
    pass


transaction_repository = TransactionRepository(CASSANDRA_HOSTS)
