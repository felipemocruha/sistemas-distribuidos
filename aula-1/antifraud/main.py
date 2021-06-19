from concurrent.futures import ThreadPoolExecutor
import grpc
import logging

from antifraud_pb2_grpc import add_AntifraudAPIServicer_to_server
from service.handlers import AntifraudAPIServicer
from config import SERVER_HOST


logger = logging.getLogger()


if __name__ == '__main__':
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_AntifraudAPIServicer_to_server(
        AntifraudAPIServicer(), server
    )

    server.add_insecure_port(SERVER_HOST)
    server.start()
    logger.error(f'server started at: {SERVER_HOST}')
    server.wait_for_termination()
