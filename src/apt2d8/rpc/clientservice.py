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

from proto import client_pb2 as pb
import service

class ClientService(service.GenericService):
	HostsResponse = pb.HostsResponse
	ChangesResponse = pb.ChangesResponse
	UpdateResponse = pb.UpdateResponse
	UpgradeResponse = pb.UpgradeResponse
	
	def __init__(self, file_in, file_out):
		service.GenericService.__init__(self, file_in, file_out)
		self.call_map = {
			pb.Request.HOSTS:	self.getHosts,
			pb.Request.CHANGES:	self.getChanges,
			pb.Request.UPDATE:	self.doUpdate,
			pb.Request.UPGRADE:	self.doUpgrade,
			pb.Request.QUIT:	self.quit
		}
	
	def read(self):
		return service.GenericService.read(self, pb.Request)

