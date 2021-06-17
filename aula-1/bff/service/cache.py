import logging
from redis import Redis
from service.config import REDIS_HOST


logger = logging.getLogger()
cache = Cache(REDIS_HOST)


class Cache:
    def __init__(self, host):
        self.conn = Redis(host)

    def list_transactions(self):
        try:
            return conn.hgetall("transactions")
        except Exception as err:
            logger.error(f"failed to list transactions: {str(err)}")

    def add_transaction(self, txn):
        try:
            return conn.hmset("transactions", txn["transaction_id"], txn)
        except Exception as err:
            logger.error(f"failed to add transaction: {str(err)}")

    def update_transaction(self, txn_id, status):
        try:
            transaction = conn.hget("transactions", txn_id)
            transaction["status"] = status

            return self.add_transaction(transaction)
        except Exception as err:
            logger.error(f"failed to update transaction: {str(err)}")
