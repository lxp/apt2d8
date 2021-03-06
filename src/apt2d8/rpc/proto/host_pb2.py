# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import common_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='host.proto',
  package='apt2d8.host',
  serialized_pb='\n\nhost.proto\x12\x0b\x61pt2d8.host\x1a\x0c\x63ommon.proto\"\x96\x01\n\x07Request\x12\'\n\x04type\x18\x01 \x02(\x0e\x32\x19.apt2d8.host.Request.Type\x12&\n\x07\x63hanges\x18\x02 \x03(\x0b\x32\x15.apt2d8.common.Change\":\n\x04Type\x12\x0f\n\x0bSYSTEM_INFO\x10\x00\x12\n\n\x06UPDATE\x10\x01\x12\x0b\n\x07UPGRADE\x10\x02\x12\x08\n\x04QUIT\x10\x03\"\x84\x02\n\x12SystemInfoResponse\x12\'\n\x07version\x18\x01 \x02(\x0b\x32\x16.apt2d8.common.Version\x12\x31\n\x0c\x64istribution\x18\x02 \x02(\x0b\x32\x1b.apt2d8.common.Distribution\x12%\n\x06kernel\x18\x03 \x01(\x0b\x32\x15.apt2d8.common.Kernel\x12\x10\n\x08hostname\x18\x04 \x01(\t\x12\x12\n\ndomainname\x18\x05 \x01(\t\x12\x0e\n\x06uptime\x18\x06 \x01(\x02\x12\x10\n\x08loadavg1\x18\x07 \x01(\x02\x12\x10\n\x08loadavg5\x18\x08 \x01(\x02\x12\x11\n\tloadavg15\x18\t \x01(\x02\"`\n\x0eUpdateResponse\x12&\n\x07sources\x18\x01 \x03(\x0b\x32\x15.apt2d8.common.Source\x12&\n\x07\x63hanges\x18\x02 \x03(\x0b\x32\x15.apt2d8.common.Change\"\x8b\x01\n\x0fUpgradeResponse\x12\x33\n\x06status\x18\x01 \x02(\x0e\x32#.apt2d8.host.UpgradeResponse.Status\x12\x0e\n\x06stdout\x18\x02 \x01(\x0c\x12\x0e\n\x06stderr\x18\x03 \x01(\x0c\"#\n\x06Status\x12\x0c\n\x08\x46INISHED\x10\x00\x12\x0b\n\x07\x43ONSOLE\x10\x01')



_REQUEST_TYPE = descriptor.EnumDescriptor(
  name='Type',
  full_name='apt2d8.host.Request.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='SYSTEM_INFO', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='UPDATE', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='UPGRADE', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='QUIT', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=134,
  serialized_end=192,
)

_UPGRADERESPONSE_STATUS = descriptor.EnumDescriptor(
  name='Status',
  full_name='apt2d8.host.UpgradeResponse.Status',
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
  serialized_start=660,
  serialized_end=695,
)


_REQUEST = descriptor.Descriptor(
  name='Request',
  full_name='apt2d8.host.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='type', full_name='apt2d8.host.Request.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='changes', full_name='apt2d8.host.Request.changes', index=1,
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
  serialized_start=42,
  serialized_end=192,
)


_SYSTEMINFORESPONSE = descriptor.Descriptor(
  name='SystemInfoResponse',
  full_name='apt2d8.host.SystemInfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='version', full_name='apt2d8.host.SystemInfoResponse.version', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='distribution', full_name='apt2d8.host.SystemInfoResponse.distribution', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='kernel', full_name='apt2d8.host.SystemInfoResponse.kernel', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hostname', full_name='apt2d8.host.SystemInfoResponse.hostname', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='domainname', full_name='apt2d8.host.SystemInfoResponse.domainname', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='uptime', full_name='apt2d8.host.SystemInfoResponse.uptime', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='loadavg1', full_name='apt2d8.host.SystemInfoResponse.loadavg1', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='loadavg5', full_name='apt2d8.host.SystemInfoResponse.loadavg5', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='loadavg15', full_name='apt2d8.host.SystemInfoResponse.loadavg15', index=8,
      number=9, type=2, cpp_type=6, label=1,
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
  serialized_start=195,
  serialized_end=455,
)


_UPDATERESPONSE = descriptor.Descriptor(
  name='UpdateResponse',
  full_name='apt2d8.host.UpdateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='sources', full_name='apt2d8.host.UpdateResponse.sources', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='changes', full_name='apt2d8.host.UpdateResponse.changes', index=1,
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
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=457,
  serialized_end=553,
)


_UPGRADERESPONSE = descriptor.Descriptor(
  name='UpgradeResponse',
  full_name='apt2d8.host.UpgradeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='apt2d8.host.UpgradeResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='stdout', full_name='apt2d8.host.UpgradeResponse.stdout', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='stderr', full_name='apt2d8.host.UpgradeResponse.stderr', index=2,
      number=3, type=12, cpp_type=9, label=1,
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
  serialized_start=556,
  serialized_end=695,
)

_REQUEST.fields_by_name['type'].enum_type = _REQUEST_TYPE
_REQUEST.fields_by_name['changes'].message_type = common_pb2._CHANGE
_REQUEST_TYPE.containing_type = _REQUEST;
_SYSTEMINFORESPONSE.fields_by_name['version'].message_type = common_pb2._VERSION
_SYSTEMINFORESPONSE.fields_by_name['distribution'].message_type = common_pb2._DISTRIBUTION
_SYSTEMINFORESPONSE.fields_by_name['kernel'].message_type = common_pb2._KERNEL
_UPDATERESPONSE.fields_by_name['sources'].message_type = common_pb2._SOURCE
_UPDATERESPONSE.fields_by_name['changes'].message_type = common_pb2._CHANGE
_UPGRADERESPONSE.fields_by_name['status'].enum_type = _UPGRADERESPONSE_STATUS
_UPGRADERESPONSE_STATUS.containing_type = _UPGRADERESPONSE;
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['SystemInfoResponse'] = _SYSTEMINFORESPONSE
DESCRIPTOR.message_types_by_name['UpdateResponse'] = _UPDATERESPONSE
DESCRIPTOR.message_types_by_name['UpgradeResponse'] = _UPGRADERESPONSE

class Request(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUEST
  
  # @@protoc_insertion_point(class_scope:apt2d8.host.Request)

class SystemInfoResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SYSTEMINFORESPONSE
  
  # @@protoc_insertion_point(class_scope:apt2d8.host.SystemInfoResponse)

class UpdateResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPDATERESPONSE
  
  # @@protoc_insertion_point(class_scope:apt2d8.host.UpdateResponse)

class UpgradeResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPGRADERESPONSE
  
  # @@protoc_insertion_point(class_scope:apt2d8.host.UpgradeResponse)

# @@protoc_insertion_point(module_scope)
