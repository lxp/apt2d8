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

import hostmanager
from ..rpc import clientservice

class ClientServiceImpl(clientservice.ClientService):
	def getHosts(self, msg):
		response = self.HostsResponse()
		for name, h in hostmanager.manager.getHosts().iteritems():
			sysinfo = h.getSystemInfo()
			host = response.hosts.add()
			host.host.id = name
			host.version.major = sysinfo.version.major
			host.version.minor = sysinfo.version.minor
			host.version.patch = sysinfo.version.patch
			host.distribution.type = sysinfo.distribution.type
			host.distribution.architecture = sysinfo.distribution.architecture
			host.distribution.foreign_architectures.extend(sysinfo.distribution.foreign_architectures)
			host.distribution.id = sysinfo.distribution.id
			host.distribution.release = sysinfo.distribution.release
			host.distribution.codename = sysinfo.distribution.codename
			host.distribution.description = sysinfo.distribution.description
			host.kernel.ostype = sysinfo.kernel.ostype
			host.kernel.osrelease = sysinfo.kernel.osrelease
			host.kernel.version = sysinfo.kernel.version
			host.hostname = sysinfo.hostname
			host.domainname = sysinfo.domainname
			host.uptime = sysinfo.uptime
			host.loadavg1 = sysinfo.loadavg1
			host.loadavg5 = sysinfo.loadavg5
			host.loadavg15 = sysinfo.loadavg15
		
		return response
	
	def getChanges(self, msg):
		response = self.ChangesResponse()
		
		for req_host in msg.hosts:
			host = hostmanager.manager.getHost(req_host.host.id)
			resp_host = response.hosts.add()
			resp_host.host.id = req_host.host.id
			self._copyChangesToProto(host.getChanges(), resp_host.changes)
			resp_host.last_update = long(host.getLastUpdate())
		
		return response
	
	def _copyChangesToProto(self, changes, proto):
		for chg in changes:
			change = proto.add()
			change.package.name = chg.package.name
			self._copyVersionToProto(chg.package.installed, change.package.installed)
			self._copyVersionToProto(chg.package.candidate, change.package.candidate)
			change.operation = chg.operation
	
	def _copyVersionToProto(self, pkgver, proto):
		proto.version = pkgver.version
		proto.architecture = pkgver.architecture
		proto.origin = pkgver.origin
		proto.archive = pkgver.archive
		proto.component = pkgver.component
		proto.size = pkgver.size
		proto.installed_size = pkgver.installed_size
		proto.source_name = pkgver.source_name
		proto.source_version = pkgver.source_version
	
	def doUpdate(self, msg):
		response = self.UpdateResponse()
		
		# TODO: Update hosts
		
		return response
	
	def doUpgrade(self, msg):
		hosts = {}
		for req_host in msg.hosts:
			changes = []
			for req_change in req_host.changes:
				if req_change.package.candidate is None:
					ver = None
				else:
					ver = req_change.package.candidate.version
				
				changes.append((req_change.package.name, req_change.operation, ver))
			
			hosts[req_host.host.id] = changes
		
		for finished, host, dataout, dataerr in hostmanager.manager.upgradeHosts(hosts):
			response = self.UpgradeResponse()
			response.host.id = host
			if finished:
				response.status = self.UpgradeResponse.FINISHED
			else:
				response.status = self.UpgradeResponse.CONSOLE
				if dataout is not None:
					response.stdout = dataout
			
				if dataerr is not None:
					response.stderr = dataerr
			
			self.write(response)
	
	def quit(self, msg):
		self.stop()

