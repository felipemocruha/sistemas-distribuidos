from redis import Redis
from service.config import REDIS_HOST

cache = Cache(REDIS_HOST)


class Cache:
    def __init__(self, host):
        self.conn = Redis(host)

    def list_transactions(self):
        return conn.hgetall('transactions')

    def add_transaction(self, txn):
        return conn.hmset('transactions', txn['transaction_id'], txn)

    def update_transaction(self, txn_id, status):
        transaction = conn.hget('transactions', txn_id)
        transaction['status'] = status
        
        return self.add_transaction(transaction)
