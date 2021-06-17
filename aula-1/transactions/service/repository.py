import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config import CASSANDRA_HOSTS


logger = logging.getLogger()
transaction_repository = TransactionRepository


class TransactionRepository:
    def __init__(self):
        try:
            auth_provider = PlainTextAuthProvider(username="user", password="pass")
            cluster = Cluster(CASSANDRA_HOSTS, auth_provider=auth_provider)
            self.session = cluster.connect()
        except Exception as err:
            log.error(f'cassandra seems unavailable: {str(err)}')
            
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
        
        except Exception as err:
            log.error(f'failed to run statement: {str(err)}')            
            raise RepositoryError()

    
class RepositoryError(Exception):
    pass
