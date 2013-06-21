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

import ConfigParser
import logging
import os
import paramiko

import host
from ..common import async
from ..common import config

logger = logging.getLogger(__name__)

class HostManager(object):
	_keys = {}
	_hosts = {}
	
	def __init__(self):
		self.user_config = ConfigParser.SafeConfigParser()
		self.system_config = ConfigParser.SafeConfigParser()
	
	def _loadKeys(self, key_dir):
		logger.debug('Loading SSH keys from directory %s' % key_dir)
		self._keys.clear()
		for entry in os.listdir(key_dir):
			filename = os.path.join(key_dir, entry)
			if os.path.isfile(filename) and not entry.endswith('.pub'):
				key = None
				for pkey_class in (paramiko.RSAKey, paramiko.DSSKey):
					try:
						key = pkey_class.from_private_key_file(filename, None)
						break
					except paramiko.SSHException, e:
						pass
				
				self._keys[entry] = key
		
		logger.debug('Loaded %d SSH key(s)' % len(self._keys))
	
	def _loadConfig(self, user_config, system_config):
		logger.debug('Loading host configuration from %s and %s' % (user_config, system_config))
		self._hosts.clear()
		self.user_config.read(user_config)
		self.system_config.read(system_config)
		for s in self.user_config.sections():
			if self.system_config.has_section(s):
				hostkey = self.system_config.get(s, 'hostkey')
			else:
				hostkey = None
			
			h = self.user_config.get(s, 'host')
			
			logger.debug('Adding host %s with hostkey %s', h, hostkey)
			
			self._hosts[s] = host.Host(s, h, self.user_config.getint(s, 'port'), hostkey, self.user_config.get(s, 'user'), self._keys[self.user_config.get(s, 'pkey')])
	
	def loadKeys(self):
		self._loadKeys('%s/ssh' % config.USER_CONFIG_PATH)
	
	def loadConfig(self):
		self._loadConfig('%s/apt2d8.conf' % config.USER_CONFIG_PATH, '%s/apt2d8.conf' % config.SYSTEM_CONFIG_PATH)
	
	def getHost(self, name):
		return self._hosts[name]
	
	def getHosts(self):
		return self._hosts
	
	def updateHosts(self):
		logger.info('Starting initial host update')
		for h in self._hosts.itervalues():
			h.update()
		
		logger.info('Initial host update finished')
	
	def upgradeHosts(self, hosts):
		host_ids = {}
		fds = {}
		async_manager = async.AsyncManager()
		
		for host_id, changes in hosts.iteritems():
			host = self._hosts[host_id]
			fd = host.startUpgrade(changes)
			host_ids[fd] = host_id
			fds[fd] = iter(host.finishUpgrade())
			async_manager.register(fd, async.POLLIN)
		
		while len(fds) > 0:
			for fd, flag in async_manager.poll():
				if flag == async.POLLIN and fd in fds:
					try:
						dataout, dataerr = fds[fd].next()
						yield (False, host_ids[fd], dataout, dataerr)
					except StopIteration:
						async_manager.unregister(fd)
						yield (True, host_ids[fd], None, None)
						del host_ids[fd]
						del fds[fd]

manager = HostManager()

