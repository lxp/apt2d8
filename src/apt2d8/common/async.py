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

import select
from select import POLLIN, POLLPRI, POLLOUT, POLLERR, POLLHUP, POLLNVAL

class AsyncManager(object):
	FLAGS = [POLLIN, POLLPRI, POLLOUT, POLLERR, POLLHUP, POLLNVAL]
	RETURN = object()
	
	def __init__(self):
		self.p = select.poll()
		self.call_map = {}
	
	def register(self, fd, flags, callback = RETURN):
		for flag in self.FLAGS:
			if flags & flag:
				self._addMap(fd, flag, callback)
		
		self.p.register(fd, flags)
	
	def _addMap(self, fd, flag, callback):
		if fd in self.call_map:
			if flag in self.call_map[fd]:
				self.call_map[fd][flag].append(callback)
			else:
				self.call_map[fd][flag] = [callback]
		else:
			self.call_map[fd] = {}
			self.call_map[fd][flag] = [callback]
	
	def unregister(self, fd):
		self.p.unregister(fd)
		del self.call_map[fd]
	
	def poll(self, timeout=-1):
		events = self.p.poll(timeout)
		returnlist = []
		for fd, flag in events:
			if fd in self.call_map and flag in self.call_map[fd]:
				for call in self.call_map[fd][flag]:
					if call is self.RETURN:
						returnlist.append((fd, flag))
					else:
						call(fd, flag)
		
		return returnlist

