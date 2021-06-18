from service.pubsub import transaction_client
from service.handlers import register_transaction


if __name__ == '__main__':
    while True:
        transaction_client.process_events(register_transaction)
