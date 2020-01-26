import warnings

from textwrap import dedent
from typing import List

from google.protobuf.descriptor_pb2 import SourceCodeInfo

from protoc_gen_pydocstring.descriptors import Field, Message
from protoc_gen_pydocstring.registry import Registry, MESSAGE_TYPE, FIELD_TYPE


Location = SourceCodeInfo.Location


def get_location_comment(location: Location) -> str:
    """Concatenate leading and trailing comments of the location descriptor."""
    leading = dedent(location.leading_comments)
    trailing = dedent(location.trailing_comments)
    return f"{leading}{trailing}"[:-1]


def parse_locations(locations: List[Location], registry: Registry) -> List[Message]:
    messages = {}
    for location in locations:
        # ignore locations that don't have comments
        if not location.leading_comments and not location.trailing_comments:
            continue

        # hashable path of the location
        path = tuple(location.path)

        # get the location comment
        comment = get_location_comment(location)

        try:
            entry = registry[path]
        except Exception:
            warnings.warn(f'Descriptor not found {path}.')
            continue

        if entry.type == MESSAGE_TYPE:
            message_name = entry.name
            message = messages.get(message_name, Message(message_name))
            message.comment = comment
        elif entry.type == FIELD_TYPE:
            message_name = entry.parent.name
            message = messages.get(message_name, Message(message_name))
            message.add_field(Field(entry.name, comment))
        else:
            raise Exception('Unkown descriptor type.')

        messages[message_name] = message

    return messages.values()
