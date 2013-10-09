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

import fcntl
import logging
import os
import subprocess

from ..common import async
from ..common import config

WRAPPER_PATH = '%s/wrapper.py' % os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)

class PriviledgedExecution(object):
	def __init__(self, args, async_manager = None):
		self.cmd = ['sudo', WRAPPER_PATH]
		self.cmd.extend(args)
		logger.debug('Executing command: %s', self.cmd)
		
		self.async_manager = async_manager
		
		self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
		fl = fcntl.fcntl(self.proc.stdout.fileno(), fcntl.F_GETFL)
		fcntl.fcntl(self.proc.stdout.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
		fl = fcntl.fcntl(self.proc.stderr.fileno(), fcntl.F_GETFL)
		fcntl.fcntl(self.proc.stderr.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
	
	def __iter__(self):
		stdout = self.proc.stdout.fileno()
		stderr = self.proc.stderr.fileno()
		
		self.async_manager.register(stdout, async.POLLIN | async.POLLHUP | async.POLLERR)
		self.async_manager.register(stderr, async.POLLIN | async.POLLHUP | async.POLLERR)
		open_streams = 2
		
		while open_streams > 0:
			events = self.async_manager.poll()
			for fd, event in events:
				if event & async.POLLIN:
					data = os.read(fd, 1024)
					if data == '':
						self.async_manager.unregister(fd)
						open_streams -= 1
					else:
						if fd == stdout:
							yield (data, None)
						elif fd == stderr:
							yield (None, data)
				
				elif event & async.POLLHUP or event & async.POLLERR:
					self.async_manager.unregister(fd)
					open_streams -= 1
	
	def wait(self):
		if self.proc.wait() != 0:
			raise subprocess.CalledProcessError(self.proc.returncode, self.cmd)

def update():
	return PriviledgedExecution(['update'])

def upgrade(changes, async_manager):
	args = ['upgrade']
	for c in changes:
		if c.package.candidate is not None:
			args.append('%s=%s' % (c.package.name, c.package.candidate.version))
	
	return PriviledgedExecution(args, async_manager)

