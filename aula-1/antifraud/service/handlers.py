import antifraud_pb2
from antifraud_pb2_grpc import AntifraudAPIServicer as IAntifraudAPIServicer

from service.models import antifraud_model
from config import APPROVED_THRESHOLD


class AntifraudAPIServicer(IAntifraudAPIServicer):
    def AntifraudAssesment(self, request, context):
        data = {
            'value_in_cents': request.value_in_cents,
            'transaction_timestamp': request.transaction_timestamp,
            'latitude': request.latitude,
            'longitude': request.longitude,
        }
        result = antifraud_model.approve(data)

        status = antifraud_pb2.ACCEPTED
        if result < APPROVED_THRESHOLD:
            status = antifraud_pb2.REJECTED

        return antifraud_pb2.AntifraudAssesmentResponse(status=status)
