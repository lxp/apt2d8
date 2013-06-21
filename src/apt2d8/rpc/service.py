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

import protocol

class GenericService(object):
	def __init__(self, file_in, file_out):
		self.proto = protocol.Protocol(file_in, file_out)
		self.call_map = {}
	
	def read(self, msg):
		return self.proto.read(msg)
	
	def write(self, msg):
		self.proto.write(msg)
	
	def writeError(self):
		self.proto.writeError()
	
	def run(self):
		self.running = True
		while self.running:
			msg = self.read()
			try:
				ret = self.call_map[msg.type](msg)
				if ret is not None:
					self.write(ret)
			except:
				self.writeError()
				raise
	
	def stop(self):
		self.running = False

