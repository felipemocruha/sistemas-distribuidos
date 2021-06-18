from concurrent.futures import ProcessPoolExecutor
import logging
import grpc

from antifraud_pb2 import AntifraudAssesmentRequest, ACCEPTED
from antifraud_pb2_grpc import AntifraudAPIStub
from service.config import ANTIFRAUD_HOST


logger = logging.getLogger()


class AntifraudInternalError(Exception):
    pass


class AntifraudClient:
    def __init__(self, host):
        self.host = host

    def _validate(self, transaction):
        try:
            channel = grpc.insecure_channel(self.host)
            stub = AntifraudAPIStub(channel)

            payload = AntifraudAssesmentRequest(
                value_in_cents=transaction['value_in_cents'],
                transaction_timestamp=transaction['transaction_timestamp'],
                latitude=transaction['latitude'],
                longitude=transaction['longitude'],
            )
            response = stub.AntifraudAssesment(payload)
            channel.close()

            if response.status == ACCEPTED:
                return 'accepted'
            else:
                return 'rejected'

        except Exception as err:
            logger.error(f'failed to contact antifraud service: {str(err)}')
            return 'rejected'

    def validate(self, transaction):
        with ProcessPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self._validate, transaction)
            return future.result()


antifraud_client = AntifraudClient(ANTIFRAUD_HOST)
