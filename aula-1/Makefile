
proto:
	@python -m grpc_tools.protoc -Iproto\
	--python_out=antifraud \
	--python_out=transactions \
	--grpc_python_out=transactions \
	--grpc_python_out=antifraud \
	--proto_path=./proto/antifraud/v1 \
	antifraud.proto

.PHONY: proto
