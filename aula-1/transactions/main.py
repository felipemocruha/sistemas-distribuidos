from service import create_app
from service.pubsub import transaction_client


if __name__ == '__main__':
    transaction_client.process_events(register_transaction)
