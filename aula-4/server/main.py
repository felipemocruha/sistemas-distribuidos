from threading import Thread
import bjoern

from service import create_app
from service.pubsub import message_client


app = create_app()


def run_consumer():
    while True:
        message_client.create_accounts("account_created")


if __name__ == '__main__':
    t = Thread(target=run_consumer)
    t.setDaemon(True)
    t.start()

    bjoern.run(app, "0.0.0.0", 5000)
