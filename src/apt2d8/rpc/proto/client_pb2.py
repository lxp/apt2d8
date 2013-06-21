# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import common_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='client.proto',
  package='apt2d8.client',
  serialized_pb='\n\x0c\x63lient.proto\x12\rapt2d8.client\x1a\x0c\x63ommon.proto\"\xa2\x01\n\x07Request\x12)\n\x04type\x18\x01 \x02(\x0e\x32\x1b.apt2d8.client.Request.Type\x12)\n\x05hosts\x18\x02 \x03(\x0b\x32\x1a.apt2d8.client.HostChanges\"A\n\x04Type\x12\t\n\x05HOSTS\x10\x00\x12\x0b\n\x07\x43HANGES\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\x0b\n\x07UPGRADE\x10\x03\x12\x08\n\x04QUIT\x10\x04\"7\n\rHostsResponse\x12&\n\x05hosts\x18\x01 \x03(\x0b\x32\x17.apt2d8.client.HostInfo\"<\n\x0f\x43hangesResponse\x12)\n\x05hosts\x18\x01 \x03(\x0b\x32\x1a.apt2d8.client.HostChanges\"\x10\n\x0eUpdateResponse\"\xb0\x01\n\x0fUpgradeResponse\x12!\n\x04host\x18\x01 \x02(\x0b\x32\x13.apt2d8.client.Host\x12\x35\n\x06status\x18\x02 \x02(\x0e\x32%.apt2d8.client.UpgradeResponse.Status\x12\x0e\n\x06stdout\x18\x03 \x01(\x0c\x12\x0e\n\x06stderr\x18\x04 \x01(\x0c\"#\n\x06Status\x12\x0c\n\x08\x46INISHED\x10\x00\x12\x0b\n\x07\x43ONSOLE\x10\x01\"\x12\n\x04Host\x12\n\n\x02id\x18\x01 \x02(\t\"\x9d\x02\n\x08HostInfo\x12!\n\x04host\x18\x01 \x02(\x0b\x32\x13.apt2d8.client.Host\x12\'\n\x07version\x18\x02 \x02(\x0b\x32\x16.apt2d8.common.Version\x12\x31\n\x0c\x64istribution\x18\x03 \x02(\x0b\x32\x1b.apt2d8.common.Distribution\x12%\n\x06kernel\x18\x04 \x01(\x0b\x32\x15.apt2d8.common.Kernel\x12\x10\n\x08hostname\x18\x05 \x01(\t\x12\x12\n\ndomainname\x18\x06 \x01(\t\x12\x0e\n\x06uptime\x18\x07 \x01(\x02\x12\x10\n\x08loadavg1\x18\x08 \x01(\x02\x12\x10\n\x08loadavg5\x18\t \x01(\x02\x12\x11\n\tloadavg15\x18\n \x01(\x02\"m\n\x0bHostChanges\x12!\n\x04host\x18\x01 \x02(\x0b\x32\x13.apt2d8.client.Host\x12&\n\x07\x63hanges\x18\x02 \x03(\x0b\x32\x15.apt2d8.common.Change\x12\x13\n\x0blast_update\x18\x03 \x01(\x04')



_REQUEST_TYPE = descriptor.EnumDescriptor(
  name='Type',
  full_name='apt2d8.client.Request.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='HOSTS', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='CHANGES', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='UPDATE', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='UPGRADE', index=3, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='QUIT', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=143,
  serialized_end=208,
)

_UPGRADERESPONSE_STATUS = descriptor.EnumDescriptor(
  name='Status',
  full_name='apt2d8.client.UpgradeResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='FINISHED', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='CONSOLE', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=489,
  serialized_end=524,
)


_REQUEST = descriptor.Descriptor(
  name='Request',
  full_name='apt2d8.client.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='type', full_name='apt2d8.client.Request.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hosts', full_name='apt2d8.client.Request.hosts', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REQUEST_TYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=46,
  serialized_end=208,
)


_HOSTSRESPONSE = descriptor.Descriptor(
  name='HostsResponse',
  full_name='apt2d8.client.HostsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='hosts', full_name='apt2d8.client.HostsResponse.hosts', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=210,
  serialized_end=265,
)


_CHANGESRESPONSE = descriptor.Descriptor(
  name='ChangesResponse',
  full_name='apt2d8.client.ChangesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='hosts', full_name='apt2d8.client.ChangesResponse.hosts', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=267,
  serialized_end=327,
)


_UPDATERESPONSE = descriptor.Descriptor(
  name='UpdateResponse',
  full_name='apt2d8.client.UpdateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=329,
  serialized_end=345,
)


_UPGRADERESPONSE = descriptor.Descriptor(
  name='UpgradeResponse',
  full_name='apt2d8.client.UpgradeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='host', full_name='apt2d8.client.UpgradeResponse.host', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='status', full_name='apt2d8.client.UpgradeResponse.status', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='stdout', full_name='apt2d8.client.UpgradeResponse.stdout', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='stderr', full_name='apt2d8.client.UpgradeResponse.stderr', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _UPGRADERESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=348,
  serialized_end=524,
)


_HOST = descriptor.Descriptor(
  name='Host',
  full_name='apt2d8.client.Host',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='apt2d8.client.Host.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=526,
  serialized_end=544,
)


_HOSTINFO = descriptor.Descriptor(
  name='HostInfo',
  full_name='apt2d8.client.HostInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='host', full_name='apt2d8.client.HostInfo.host', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='version', full_name='apt2d8.client.HostInfo.version', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='distribution', full_name='apt2d8.client.HostInfo.distribution', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='kernel', full_name='apt2d8.client.HostInfo.kernel', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hostname', full_name='apt2d8.client.HostInfo.hostname', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='domainname', full_name='apt2d8.client.HostInfo.domainname', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='uptime', full_name='apt2d8.client.HostInfo.uptime', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='loadavg1', full_name='apt2d8.client.HostInfo.loadavg1', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='loadavg5', full_name='apt2d8.client.HostInfo.loadavg5', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='loadavg15', full_name='apt2d8.client.HostInfo.loadavg15', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=547,
  serialized_end=832,
)


_HOSTCHANGES = descriptor.Descriptor(
  name='HostChanges',
  full_name='apt2d8.client.HostChanges',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='host', full_name='apt2d8.client.HostChanges.host', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='changes', full_name='apt2d8.client.HostChanges.changes', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='last_update', full_name='apt2d8.client.HostChanges.last_update', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=834,
  serialized_end=943,
)

_REQUEST.fields_by_name['type'].enum_type = _REQUEST_TYPE
_REQUEST.fields_by_name['hosts'].message_type = _HOSTCHANGES
_REQUEST_TYPE.containing_type = _REQUEST;
_HOSTSRESPONSE.fields_by_name['hosts'].message_type = _HOSTINFO
_CHANGESRESPONSE.fields_by_name['hosts'].message_type = _HOSTCHANGES
_UPGRADERESPONSE.fields_by_name['host'].message_type = _HOST
_UPGRADERESPONSE.fields_by_name['status'].enum_type = _UPGRADERESPONSE_STATUS
_UPGRADERESPONSE_STATUS.containing_type = _UPGRADERESPONSE;
_HOSTINFO.fields_by_name['host'].message_type = _HOST
_HOSTINFO.fields_by_name['version'].message_type = common_pb2._VERSION
_HOSTINFO.fields_by_name['distribution'].message_type = common_pb2._DISTRIBUTION
_HOSTINFO.fields_by_name['kernel'].message_type = common_pb2._KERNEL
_HOSTCHANGES.fields_by_name['host'].message_type = _HOST
_HOSTCHANGES.fields_by_name['changes'].message_type = common_pb2._CHANGE
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['HostsResponse'] = _HOSTSRESPONSE
DESCRIPTOR.message_types_by_name['ChangesResponse'] = _CHANGESRESPONSE
DESCRIPTOR.message_types_by_name['UpdateResponse'] = _UPDATERESPONSE
DESCRIPTOR.message_types_by_name['UpgradeResponse'] = _UPGRADERESPONSE
DESCRIPTOR.message_types_by_name['Host'] = _HOST
DESCRIPTOR.message_types_by_name['HostInfo'] = _HOSTINFO
DESCRIPTOR.message_types_by_name['HostChanges'] = _HOSTCHANGES

class Request(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUEST
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.Request)

class HostsResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HOSTSRESPONSE
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.HostsResponse)

class ChangesResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CHANGESRESPONSE
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.ChangesResponse)

class UpdateResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPDATERESPONSE
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.UpdateResponse)

class UpgradeResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPGRADERESPONSE
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.UpgradeResponse)

class Host(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HOST
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.Host)

class HostInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HOSTINFO
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.HostInfo)

class HostChanges(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HOSTCHANGES
  
  # @@protoc_insertion_point(class_scope:apt2d8.client.HostChanges)

# @@protoc_insertion_point(module_scope)
