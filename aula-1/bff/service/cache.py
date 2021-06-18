import logging
import json

from redis import Redis
from service.config import REDIS_HOST


logger = logging.getLogger()


class Cache:
    def __init__(self, host):
        self.conn = Redis(host)

    def list_transactions(self):
        try:
            keys = self.conn.keys()
            return [json.loads(txn) for txn in self.conn.mget(keys)]
        except Exception as err:
            logger.error(f"failed to list transactions: {str(err)}")

    def add_transaction(self, txn):
        try:
            payload = json.dumps(txn)
            return self.conn.set(txn["transaction_id"], payload)

        except Exception as err:
            logger.error(f"failed to add transaction: {str(err)}")

    def update_transaction(self, txn_id, status):
        try:
            transaction = json.loads(self.conn.get(txn_id))
            transaction["status"] = status
            return self.add_transaction(transaction)

        except Exception as err:
            logger.error(f"failed to update transaction: {str(err)}")


cache = Cache(REDIS_HOST)
