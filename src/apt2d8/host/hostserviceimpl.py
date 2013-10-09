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

import apt
from aptsources import sourceslist
import subprocess

import privileged
from ..common import async
from ..common import config
from ..common import version
from ..rpc import hostservice

class HostServiceImpl(hostservice.HostService):
	def getSystemInfo(self, msg):
		response = self.SystemInfoResponse()
		response.version.major = version.major
		response.version.minor = version.minor
		response.version.patch = version.patch
		# TODO: Fill distribution
		# Check /etc/debian_version
		response.distribution.type = 'deb'
		response.distribution.architecture = subprocess.check_output(['dpkg', '--print-architecture']).rstrip('\n')
		response.distribution.foreign_architectures.extend(subprocess.check_output(['dpkg', '--print-foreign-architectures']).rstrip('\n').split('\n'))
		# Read /etc/lsb-release
		#response.distribution.id
		#response.distribution.release
		#response.distribution.codename
		#response.distribution.description
		response.kernel.ostype = self._readProc('sys/kernel/ostype')
		response.kernel.osrelease = self._readProc('sys/kernel/osrelease')
		response.kernel.version = self._readProc('sys/kernel/version')
		response.hostname = self._readProc('sys/kernel/hostname')
		response.domainname = self._readProc('sys/kernel/domainname')
		response.uptime = float(self._readProc('uptime').split(' ')[0])
		response.loadavg1, response.loadavg5, response.loadavg15 = (float(x) for x in self._readProc('loadavg').split(' ')[0:3])
		return response
	
	def _readProc(self, path):
		with open('%s/%s' % (config.PROC_PATH, path)) as f:
			return f.read().rstrip('\n')
	
	def doUpdate(self, msg):
		response = self.UpdateResponse()
		
		slist = sourceslist.SourcesList()
		self._copySourcesToProto(slist.list, response.sources)
		
		privileged.update().wait()
		
		cache = apt.Cache()
		cache.upgrade(dist_upgrade=True)
		self._copyChangesToProto(cache.get_changes(), response.changes)
		
		return response
	
	def _copySourcesToProto(self, sources, proto):
		sourcedict = {}
		for sentry in sources:
			if not sentry.invalid and not sentry.disabled and sentry.type == 'deb':
				lookup = (sentry.type, sentry.uri, sentry.dist)
				if lookup in sourcedict:
					source, compdict = sourcedict[lookup]
				else:
					source = proto.add()
					source.type = sentry.type
					source.uri = sentry.uri
					source.dist = sentry.dist
					compdict = {}
				
				for centry in sentry.comps:
					if centry not in compdict:
						comp = source.comps.add()
						comp.name = centry
						compdict[centry] = comp
				
				if sentry.template is not None and sentry.template.base_uri is not None:
					source.baseuri = sentry.template.base_uri
				
				sourcedict[lookup] = (source, compdict)
	
	def _copyChangesToProto(self, changes, proto):
		for pkg in changes:
			operation = self._getOperation(pkg)
			if operation is not None:
				change = proto.add()
				change.package.name = pkg.name
				self._copyVersionToProto(pkg.installed, change.package.installed)
				self._copyVersionToProto(pkg.candidate, change.package.candidate)
				change.operation = operation
	
	def _getOperation(self, pkg):
		if pkg.marked_install:
			return self.Change.INSTALL
		elif pkg.marked_reinstall:
			return self.Change.REINSTALL
		elif pkg.marked_upgrade:
			return self.Change.UPGRADE
		elif pkg.marked_downgrade:
			return self.Change.DOWNGRADE
		elif pkg.marked_delete:
			return self.Change.REMOVE
		elif pkg.marked_keep:
			return self.Change.KEEP
		else:
			return None
	
	def _copyVersionToProto(self, pkgver, proto):
		if pkgver is not None:
			proto.version = pkgver.version
			proto.architecture = pkgver.architecture
			if len(pkgver.origins) > 0:
				proto.origin = pkgver.origins[0].origin
				proto.archive = pkgver.origins[0].archive
				proto.component = pkgver.origins[0].component
			proto.size = pkgver.size
			proto.installed_size = pkgver.installed_size
			proto.source_name = pkgver.source_name
			proto.source_version = pkgver.source_version
	
	def doUpgrade(self, msg):
		async_manager = async.AsyncManager()
		async_manager.register(self.proto.file_in, async.POLLIN, self._readRequest)
		
		priv = privileged.upgrade(msg.changes, async_manager)
		
		for dataout, dataerr in priv:
			response = self.UpgradeResponse()
			response.status = self.UpgradeResponse.CONSOLE
			if dataout is not None:
				response.stdout = dataout
			
			if dataerr is not None:
				response.stderr = dataerr
			
			self.write(response)
		
		priv.wait()
		
		response = self.UpgradeResponse()
		response.status = self.UpgradeResponse.FINISHED
		return response
	
	def _readRequest(self, fd, flag):
		msg = self.read()
	
	def quit(self, msg):
		self.stop()

