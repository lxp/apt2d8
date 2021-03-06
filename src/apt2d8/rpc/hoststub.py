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

from proto import host_pb2 as pb
import protocol

class HostStub(object):
	def __init__(self, file_in, file_out):
		self.proto = protocol.Protocol(file_in, file_out)
	
	def getSystemInfo(self):
		msg = pb.Request()
		msg.type = pb.Request.SYSTEM_INFO
		self.proto.write(msg)
		return self.proto.read(pb.SystemInfoResponse)
	
	def doUpdate(self):
		msg = pb.Request()
		msg.type = pb.Request.UPDATE
		self.proto.write(msg)
		return self.proto.read(pb.UpdateResponse)
	
	def writeUpgradeRequest(self, changes):
		msg = pb.Request()
		msg.type = pb.Request.UPGRADE
		for package_name, operation, package_version in changes:
			change = msg.changes.add()
			change.package.name = package_name
			change.operation = operation
			if package_version is not None:
				change.package.candidate.version = package_version
		
		self.proto.write(msg)
	
	def readUpgradeResponse(self):
		return self.proto.read(pb.UpgradeResponse)
	
	def quit(self):
		msg = pb.Request()
		msg.type = pb.Request.QUIT
		self.proto.write(msg)

