#!/bin/bash

python -m grpc.tools.protoc --plugin=protoc-gen-docstring=protoc_gen_pydocstring/main.py --proto_path=. --python_out=. --docstring_out=. test/test.proto
