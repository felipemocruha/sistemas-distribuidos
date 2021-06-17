import futures
from antifraud_pb2_grpc import add_AntifraudAPIServicer_to_server
from service.handlers import AntifraudAPIServicer


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_AntifraudAPIServicer_to_server(
        AntifraudAPIServicer(), server
    )
    
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
