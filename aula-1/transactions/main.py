import logging
from service.pubsub import transaction_client
from service.handlers import register_transaction


logger = logging.getLogger()


if __name__ == '__main__':
    logger.error("transactions service started")
    while True:
        transaction_client.process_events(register_transaction)
