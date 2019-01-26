SRC = src
PYTHON = pipenv run python

.PHONY: all
all: format proto lint test

.PHONY: test
test:
	pipenv run pytest --cov=$(SRC) --cov-report=html

.PHONY: format
format:
	pipenv run yapf -ir . && pipenv run isort -yrc

.PHONY: lint
lint:
	pipenv run mypy --strict $(SRC)


# proto
.SUFFIXES: .proto _pb2.py _pb2_grpc.py
PROTO_PATH = resources/protobuf
PROTOC = pipenv run python -m grpc_tools.protoc
PFLAGS = -I$(PROTO_PATH) --python_out=$(PROTO_PATH) --grpc_python_out=$(PROTO_PATH)

PROTO_OBJS = $(PROTO_PATH)/pair_pb2.py $(PROTO_PATH)/pair_pb2_grpc.py


.PHONY: proto
proto: $(PROTO_OBJS)

.proto_pb2.py:
	$(PROTOC) $(PFLAGS) $<

.proto_pb2_grpc.py:
	$(PROTOC) $(PFLAGS) $<
