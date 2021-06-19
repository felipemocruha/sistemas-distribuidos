
proto:
	@python -m grpc_tools.protoc -Iproto\
	--python_out=antifraud \
	--python_out=transactions \
	--grpc_python_out=transactions \
	--grpc_python_out=antifraud \
	--proto_path=./proto/antifraud/v1 \
	antifraud.proto

bff:
	cd bff && $(MAKE) docker

transactions:
	cd transactions && $(MAKE) docker

antifraud:
	cd antifraud && $(MAKE) docker

generator:
	cd generator && $(MAKE) docker

build: bff transactions antifraud generator

push: build
	cd bff && $(MAKE) push
	cd transactions && $(MAKE) push
	cd antifraud && $(MAKE) push
	cd generator && $(MAKE) push

.PHONY: proto bff transactions antifraud generator
