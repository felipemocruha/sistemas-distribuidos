from concurrent.futures import ThreadPoolExecutor
from antifraud_pb2_grpc import add_AntifraudAPIServicer_to_server
from service.handlers import AntifraudAPIServicer
from config import SERVER_HOST


if __name__ == '__main__':
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_AntifraudAPIServicer_to_server(
        AntifraudAPIServicer(), server
    )

    server.add_insecure_port(SERVER_HOST)
    server.start()
    server.wait_for_termination()
