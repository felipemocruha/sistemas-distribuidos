import logging
import grpc

from antifraud.v1.antifraud_pb2 import AntifraudAssesmentRequest, ACCEPTED
from antifraud_pb2_grpc import AntifraudAPIStub
from config import ANTIFRAUD_HOST


logger = logging.getLogger()
antifraud_client = AntifraudClient(ANTIFRAUD_HOST)


class AntifraudInternalError(Exception):
    pass


class AntifraudClient:
    def __init__(self, host):
        pass

    def validate(self, transaction):
        try:
            with grpc.insecure_channel(self.host) as channel:        
                stub = AntifraudAPIStub(channel)
                payload = AntifraudAssesmentRequest(
                    value_in_cents=transaction['value_in_cents'],
                    transaction_timestamp=transaction['transaction_timestamp'],
                    latitude=transaction['latitude'],
                    longitude=transaction['longitude'],
                )
                response = stub.AntifraudAssesment(payload)

                if response.status == ACCEPTED:
                    return 'accepted'
                else:
                    return 'rejected'

        except Exception as err:
            logger.error(f'failed to contact antifraud service: {str(err)}')
            return 'rejected'
