"""
Usage:
    main.py create_account <account_name>
    main.py send_message <topic>
    main.py receive_messages
"""

from time import time
from docopt import docopt
from service.pubsub import message_client
from service.config import KAFKA_MESSAGE_TOPIC


if __name__ == "__main__":
    args = docopt(__doc__)

    if args["create_account"]:
        message_client.create_account(args["<account_name>"])

    elif args["send_message"]:
        payload = {
            "source_username": "",
            "message": "saaaaaalve",
            "event_timestamp": int(time()),
        }
        message_client.send_message(args["<topic>"], payload)

    elif args["receive_messages"]:
        while True:
            message_client.receive_messages(KAFKA_MESSAGE_TOPIC)
