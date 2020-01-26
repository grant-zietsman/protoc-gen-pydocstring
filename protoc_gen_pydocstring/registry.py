from collections import namedtuple
from typing import Dict, Tuple

from google.protobuf.descriptor_pb2 import DescriptorProto, FileDescriptorProto


Descriptor = namedtuple('Descriptor', ['type', 'name', 'descriptor', 'parent'])
Registry = Dict[Tuple[int, ...], Descriptor]


(
    MESSAGE_TYPE,
    FIELD_TYPE,
) = range(2)


FIELD_INDEX = DescriptorProto.field.DESCRIPTOR.number
NESTED_TYPE_INDEX = DescriptorProto.nested_type.DESCRIPTOR.number
MESSAGE_TYPE_INDEX = FileDescriptorProto.message_type.DESCRIPTOR.number


def generate_protobuf_registry(proto_file: FileDescriptorProto) -> Registry:
    """Generates a registry of descriptors from the given protobuf file descriptor.

    Since protoc insertion points are only available for messages, nested messages and
    message fields; the registry only needs to include these descriptors.

    The descriptors are indexed by the descriptor path which is a list of integers
    that uniquely identify a descriptor based on its type and location in the protobuf.

    Attributes:
        proto_file: The protobuf descriptor file from which to generate the registry.

    Returns:
        A registry (dictionary) of descriptors indexed by the descriptor path.

    Example:
        Given the protobuf that follows

        message message_1 { ... }
        message message_2 { ... }
        message message_3 {
            message nested_1 { ... }
            message nested_2 {
                required string field_1 = 1;
                required string field_2 = 2;
                ...
                required string field_7 = 7;
            }
        }

        The path [ 4, 3, 3, 2, 2, 7 ] represents

        [
            4 -> indicates a message_type,
            3 -> specifies the third messsage (message_3),
                3 -> indicates a nested_type,
                2 -> specifies the second nested message (nested_2),
                    2 -> specifies a field,
                    7 -> specifies the seventh field (field_7),
        ]

        The indentation used here is to express the nesting.

    For more info, see SourceCodeInfo and Location in
    [descriptor.proto](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/descriptor.proto).
    """
    registry = {}

    def register_message(path: Tuple[int, ...],
                         message_name: str,
                         message_descriptor: DescriptorProto,
                         message_parent: Descriptor = None):
        """ Registers a message, its fields and nested messages.

        Attributes:
            path: Descriptor path of the message.
            message_name: Fully qualified name of the message.
            message_descriptor: Message descriptor.
            message_parent: Registered parent message.
        """
        # register the provided message
        registered_message = Descriptor(MESSAGE_TYPE, message_name, message_descriptor, message_parent)
        registry[path] = registered_message

        # register all the fields of the message descriptor
        for field_index, field_descriptor in enumerate(message_descriptor.field):
            field_path = path + (FIELD_INDEX, field_index)
            field_name = f"{message_name}.{field_descriptor.name}"
            registry[field_path] = Descriptor(FIELD_TYPE, field_name, field_descriptor, registered_message)

        # recursively register the nested messages of the message descriptor
        for nested_index, nested_message in enumerate(message_descriptor.nested_type):
            nested_path = path + (NESTED_TYPE_INDEX, nested_index)
            nested_name = f"{message_name}.{nested_message.name}"
            register_message(nested_path, nested_name, nested_message, registered_message)

    # register messages
    for message_index, message_descriptor in enumerate(proto_file.message_type):
        message_path = (MESSAGE_TYPE_INDEX, message_index)
        if proto_file.package:
            message_name = f"{proto_file.package}.{message_descriptor.name}"
        else:
            message_name = message_descriptor.name
        register_message(message_path, message_name, message_descriptor)

    return registry
