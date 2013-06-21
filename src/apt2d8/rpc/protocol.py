#
# This file is part of apt2d8.
#
# Copyright (C) 2013  David Gnedt
#
# apt2d8 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# apt2d8 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with apt2d8.  If not, see <http://www.gnu.org/licenses/>.
#

import struct

import rpcexception

class Protocol(object):
	def __init__(self, file_in, file_out):
		self.file_in = file_in
		self.file_out = file_out
	
	def read(self, msg_type):
		smsg_len = self.file_in.read(4)
		if len(smsg_len) < 4:
			raise rpcexception.ProtocolException('Protocol error')
		
		msg_len = struct.unpack('>L', smsg_len)[0]
		
		if msg_len < 0xffffffff:
			smsg = self.file_in.read(msg_len)
			msg = msg_type()
			msg.ParseFromString(smsg)
		else:
			raise rpcexception.RemoteException('Remote error')
		
		return msg
	
	def write(self, msg):
		try:
			smsg = msg.SerializeToString()
			smsg_len = len(smsg)
			packed_smsg_len = struct.pack('>L', smsg_len)
			self.file_out.write(packed_smsg_len + smsg)
			self.file_out.flush()
		except Exception as e:
			self.writeError()
			raise
	
	def writeError(self):
		packed_smsg_len = struct.pack('>L', 0xffffffff)
		self.file_out.write(packed_smsg_len)
		self.file_out.flush()

