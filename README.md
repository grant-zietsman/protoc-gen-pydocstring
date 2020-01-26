# PyDocString ProtocolBuffer Compiler Plugin

Plugin to generated python Docstrings from ProtocolBuffers.

## Note

This plugin is in very early development and as an alternative to [protoc-docs-plugin](https://github.com/googleapis/protoc-docs-plugin).

## Usage

```sh
protoc --proto_path=. --python_out=. --pydocstring_out=. my_protobuf.proto
```
