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

import base64
import binascii
import logging
import os
import paramiko
import sys
import time

import sourcewatcher
from ..common import config
from ..rpc import hoststub, rpcexception

SSH_PORT = 22

logger = logging.getLogger(__name__)

class HostState(object):
	NONE, CONNECTED, SYSTEMINFO, UPDATE, UPGRADE = range(5)

class HostException(Exception):
	pass

class HostKeyPolicy(paramiko.client.MissingHostKeyPolicy):
	def missing_host_key(self, client, hostname, key):
		raise HostException('Rejecting %s host key for %s: %s' % (key.get_name(), hostname, key.get_base64()))

class Host(object):
	client = None
	channel = None
	stub = None
	stderr = None
	logfile = None
	
	name = None
	host = None
	port = None
	hostkey = None
	username = None
	pkey = None
	
	state = HostState.NONE
	systeminfo = None
	last_connect = None
	sources = {}
	changes = None
	last_update = None
	
	def __init__(self, name, host, port, hostkey, username, pkey):
		self.name = name
		self.host = host
		self.port = port
		self.hostkey = hostkey
		self.username = username
		self.pkey = pkey
		
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(HostKeyPolicy())
		if hostkey is not None:
			keytype, key = self._parseHostkey(hostkey)
			self.client.get_host_keys().add(self._getHostkeyName(host, port), keytype, key)
		
		self.logfile = '%s/host.%s' % (config.LOG_PATH, name)
	
	def _getHostkeyName(self, host, port):
		if port == SSH_PORT:
			return host
		else:
			return '[%s]:%d' % (host, port)
	
	def _parseHostkey(self, line):
		fields = line.split(' ')
		if len(fields) < 2:
			# Bad number of fields
			return None
		keytype, key = fields[:2]
		
		# Decide what kind of key we're looking at and create an object
		# to hold it accordingly.
		try:
			if keytype == 'ssh-rsa':
				key = paramiko.RSAKey(data=base64.decodestring(key))
			elif keytype == 'ssh-dss':
				key = paramiko.DSSKey(data=base64.decodestring(key))
			else:
				key = None
		except binascii.Error, e:
			raise InvalidHostKey(line, e)
		
		return (keytype, key)
	
	def _connect(self):
		if self.state == HostState.NONE:
			logger.info('Connecting to host')
			self.last_connect = time.time()
			self.client.connect(self.host, port=self.port, username=self.username, pkey=self.pkey, allow_agent=False, look_for_keys=False)
			transport = self.client.get_transport()
			self.channel = transport.open_session()
			self.channel.exec_command('apt2d8-host')
			stdin = self.channel.makefile('wb')
			stdout = self.channel.makefile('rb')
			self.stderr = self.channel.makefile_stderr('rb')
			try:
				self.stub = hoststub.HostStub(stdout, stdin)
				self.state = HostState.CONNECTED
				self._systeminfo()
				logger.info('Successfully connected')
			except rpcexception.ProtocolException:
				self._handleError()
				raise
			except rpcexception.RemoteException:
				self._handleError()
				raise
		elif self.state == HostState.CONNECTED:
			pass
		else:
			raise HostException('Unexpected connection state')
	
	def _handleError(self):
		self._handleStderr()
		self.stub = None
		self.client.close()
		self.state = HostState.NONE
	
	def _handleStderr(self):
		for line in self.stderr:
			logger.error('stderr: %s', line.rstrip('\n'))
	
	def _systeminfo(self):
		if self.state == HostState.CONNECTED:
			try:
				self.state = HostState.SYSTEMINFO
				self.systeminfo = self.stub.getSystemInfo()
				self.state = HostState.CONNECTED
			except rpcexception.RemoteException:
				self._handleError()
				raise
		else:
			raise HostException('Unexpected connection state')
	
	def _update(self):
		if self.state == HostState.CONNECTED:
			logger.info('Starting host update')
			try:
				self.state = HostState.UPDATE
				start_time = time.time()
				resp = self.stub.doUpdate()
				
				srcwatcher = sourcewatcher.manager.get(self.systeminfo.distribution.type)
				archs = (self.systeminfo.distribution.architecture,) + tuple(self.systeminfo.distribution.foreign_architectures)
				old_sources = dict(self.sources)
				new_sources = {}
				for s in resp.sources:
					comps = (c.name for c in s.comps)
					key = (s.type, s.uri, s.baseuri, s.dist, comps)
					new_sources[key] = s
					if key not in old_sources:
						srcwatcher.register(self, s.type, s.uri, s.baseuri, s.dist, comps, archs)
					else:
						del old_sources[key]
				
				for key, s in old_sources.iteritems():
					srcwatcher.unregister(self, s.type, s.uri, s.baseuri, s.dist, (c.name for c in s.comps), archs)
				
				self.sources = new_sources
				
				self.changes = resp.changes
				self.last_update = start_time
				self.state = HostState.CONNECTED
				logger.info('Host update finished')
			except rpcexception.RemoteException:
				self._handleError()
				raise
		else:
			raise HostException('Unexpected connection state')
	
	def _startUpgrade(self, changes):
		if self.state == HostState.CONNECTED:
			logger.info('Starting host upgrade')
			try:
				self.state = HostState.UPGRADE
				self.stub.writeUpgradeRequest(changes)
				logger.info('Host upgrade finished')
			except rpcexception.RemoteException:
				self._handleError()
				raise
		else:
			raise HostException('Unexpected connection state')
	
	def _finishUpgrade(self):
		if self.state == HostState.UPGRADE:
			try:
				while True:
					response = self.stub.readUpgradeResponse()
					if response.status == response.FINISHED:
						break
					elif response.status == response.CONSOLE:
						yield (response.stdout, response.stderr)
				
				self.state = HostState.CONNECTED
				logger.info('Host upgrade finished')
			except rpcexception.RemoteException:
				self._handleError()
				raise
		else:
			raise HostException('Unexpected connection state')
	
	def _close(self):
		if self.state == HostState.CONNECTED:
			try:
				self.state = HostState.NONE
				self.stub.quit()
				self.stub = None
				self.client.close()
			except rpcexception.RemoteException:
				self._handleError()
				raise
		else:
			raise HostException('Unexpected connection state')
	
	def getName(self):
		return self.name
	
	def getSystemInfo(self):
		if self.systeminfo is None:
			self._connect()
			self._systeminfo()
			self._close()
		
		return self.systeminfo
	
	def getChanges(self):
		if self.last_update is None:
			self.update()
		
		return self.changes
	
	def getSources(self):
		if self.last_update is None:
			self.update()
		
		return self.sources
	
	def getLastUpdate(self):
		return self.last_update
	
	def update(self):
		self._connect()
		self._update()
		self._close()
		return self.changes
	
	def startUpgrade(self, changes):
		self._connect()
		self._startUpgrade(changes)
		return self.channel.fileno()
	
	def finishUpgrade(self):
		for msg in self._finishUpgrade():
			yield msg
		
		self._update()
		self._close()

