from uuid import uuid4

from service.repository import transaction_repository
from service.antifraud import antifraud_client
from service.bff import notify_status
#from service.metrics import instrument_handler


def register_transaction(transaction):
    transaction['status'] = antifraud_client.validate(transaction)    
    transaction_repository.save(transaction)
    notify_status(transaction['id'], transaction['id'])
    
        
