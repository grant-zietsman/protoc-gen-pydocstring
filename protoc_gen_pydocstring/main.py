#!/usr/bin/env python

import sys

from google.protobuf.compiler.plugin_pb2 import (CodeGeneratorRequest,
                                                 CodeGeneratorResponse)

from protoc_gen_pydocstring.parser import parse_locations
from protoc_gen_pydocstring.registry import generate_protobuf_registry


def main(input_file=sys.stdin, output_file=sys.stdout):

    # Esure we are getting a bytestream, and writing to a bytestream.
    if hasattr(input_file, 'buffer'):
        input_file = input_file.buffer
    if hasattr(output_file, 'buffer'):
        output_file = output_file.buffer

    request = CodeGeneratorRequest()
    request.ParseFromString(input_file.read())

    generated_files = []

    for proto_file in request.proto_file:
        # ignore protofiles that don't need to be generated
        if proto_file.name not in request.file_to_generate:
            continue

        source = proto_file.source_code_info

        # ignore empty sources files
        if not source.ByteSize():
            continue

        # create a descriptor registry
        registry = generate_protobuf_registry(proto_file)

        # parse the locations
        messages = parse_locations(source.location, registry)

        # output filename
        proto_file_out = proto_file.name.replace(".proto", "_pb2.py")

        # inject message docstrings
        for message in messages:
            generated_files.append(CodeGeneratorResponse.File(
                name=proto_file_out,
                insertion_point=f"class_scope:{message.name}",
                content=f',\n\'__doc__\' : """{message}""",'
            ))

    # generate and return response
    response = CodeGeneratorResponse(file=generated_files)
    output_file.write(response.SerializeToString())


if __name__ == '__main__':
    main()
