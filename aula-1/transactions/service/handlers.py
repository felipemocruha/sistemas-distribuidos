import logging
from uuid import uuid4

from service.repository import transaction_repository, RepositoryError
from service.antifraud import antifraud_client, AntifraudInternalError
from service.bff import notify_status, BFFStatusWebhookError


logger = logging.getLogger()


def register_transaction(transaction):
    try:
        transaction['status'] = antifraud_client.validate(transaction)
        transaction_repository.save(transaction)
        notify_status(transaction['id'], transaction['id'])
        
    except AntifraudInternalError:
        logger.error(f'failed to validate transaction: antifraud is unavailable')

    except RepositoryError:
        logger.error(f'failed to save transaction: database is unavailable')

    except BFFStatusWebhookError:
        logger.error(f'failed to notify bff: bff is unavailable')
        
