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

import logging
import requests
import threading
import time

CHECK_PERIOD = 60.0
TIMEOUT = 60.0

logger = logging.getLogger(__name__)

class SourceWatcherManager(object):
	watchers = {}
	interval = None
	stopped = None
	thread = None
	
	def __init__(self, interval=CHECK_PERIOD):
		self.interval = interval
	
	def _run(self):
		while not self.stopped.wait(self.interval):
			self._check()
	
	def _check(self):
		logger.debug('Checking sources')
		try:
			for watcher in self.watchers.itervalues():
				watcher._check()
		except RuntimeError:
			logger.debug('RuntimeError while checking sources')
	
	def get(self, watcher_type):
		return self.watchers[watcher_type]
	
	def register(self, watcher):
		watcher_type = watcher._getType()
		if watcher_type not in self.watchers:
			self.watchers[watcher_type] = watcher
	
	def start(self):
		if self.thread is None:
			logger.debug('Starting source watcher thread')
			self.stopped = threading.Event()
			self.thread = threading.Thread(target=self._run)
			self.thread.daemon = True
			self.thread.start()

class Source(object):
	hosts = None
	last_change = None
	last_update = None
	
	def __init__(self, hosts, last_change=None):
		self.hosts = hosts
		if last_change is not None:
			self.last_change = last_change
			self.last_update = time.time()

class SourceWatcher(object):
	sources = {}
	
	def _getType(self):
		return None
	
	def _check(self):
		now = time.time()
		for key, src in self.sources.iteritems():
			if src.last_change is None or src.last_update is None or now - src.last_update > TIMEOUT:
				last_change = self._checkSource(key)
				if src.last_change < last_change:
					# TODO: Implement notifier
					for h in src.hosts:
						h.update()
					
					logger.info('Change detected Old: %s, New: %s', time.asctime(time.localtime(src.last_change)), time.asctime(time.localtime(last_change)))
				else:
					logger.debug('No change')
				
				src.last_change = last_change
				src.last_update = now
	
	def _fetchHTTPLastModified(self, url):
		req = requests.head(url)
		if req.ok:
			if 'last-modified' in req.headers:
				return time.mktime(time.strptime(req.headers['last-modified'], '%a, %d %b %Y %H:%M:%S %Z'))
			else:
				return 0
		else:
			raise Exception()
	
	def _checkSource(self, key):
		pass
	
	def _register(self, host, key):
		if key in self.sources:
			self.sources[key].hosts.append(host)
		else:
			self.sources[key] = Source([host], self._checkSource(key))
	
	def _unregister(self, host, key):
		if key in self.sources:
			self.sources[key].hosts.remove(host)
			
			if len(self.sources[key].hosts) < 1:
				del self.sources[key]

class DebianSourceWatcher(SourceWatcher):
	def _getType(self):
		return 'deb'
	
	def _checkSource(self, (uri, dist, comp, arch)):
		logger.debug('Check URI %s, Dist: %s, Comp: %s, Arch: %s', uri, dist, comp, arch)
		if dist is None and comp is None:
			# TODO: Check if simple repositories work
			url = '%s/Packages' % uri
		else:
			url = '%s/dists/%s/%s/binary-%s/Packages' % (uri, dist, comp, arch)
		
		try:
			return self._fetchHTTPLastModified('%s.bz2' % url)
		except Exception:
			try:
				return self._fetchHTTPLastModified('%s.gz' % url)
			except Exception:
				try:
					return self._fetchHTTPLastModified(url)
				except Exception, e:
					logger.error('Error while fetching %s' % url)
	
	def register(self, host, type, uri, baseuri, dist, components, architectures):
		if type == 'deb':
			baseuri = self._getBaseUri(uri, baseuri)
			
			for comp in components:
				for arch in architectures:
					self._register(host, (baseuri, dist, comp, arch))
	
	def unregister(self, host, type, uri, baseuri, dist, components, architectures):
		if type == 'deb':
			baseuri = self._getBaseUri(uri, baseuri)
			
			for comp in components:
				for arch in architectures:
					self._unregister(host, (baseuri, dist, comp, arch))
	
	def _getBaseUri(self, uri, baseuri):
		if not baseuri:
			# TODO: Try to find base uri
			return uri
		else:
			return baseuri

manager = SourceWatcherManager()
manager.register(DebianSourceWatcher())

