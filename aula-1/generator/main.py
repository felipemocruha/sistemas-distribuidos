import requests
import logging
from uuid import uuid4
from random import choice, randint, random
from time import sleep
from config import BFF_HOST, REQUEST_INTERVAL


users = [str(uuid4()) for _ in range(100)]
logger = logging.getLogger()


def generate_transaction():
    return {
        'value_in_cents': randint(50, 1345454553),
        'description': "some purchase",
        'customer_id': choice(users),
        'merchant_id': choice(users),
        'transaction_timestamp': randint(1224409756, 1624079756),
        'latitude': randint(1, 100) * random(),
        'longitude': randint(1, 100) * random(),
     }


def main():
    while True:
        try:
            resp = requests.post(
                f"http://{BFF_HOST}/api/v1/transactions",
                json=generate_transaction(),
            )

        except Exception as err:
            logger.error(f"failed to create transaction: {str(err)}")

        sleep(REQUEST_INTERVAL)


if __name__ == "__main__":
    main()
